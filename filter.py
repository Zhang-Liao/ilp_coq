import json
import os

from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue
from pyswip import Prolog

from lib import utils
from statis import acc


def read_clauses(clause_dir, prolog):
    rule_suffix = '_rule.pl'
    for filename in os.listdir(clause_dir):
        if filename.endswith(rule_suffix):
            prolog.consult(os.path.join(clause_dir, filename))
    return prolog

def read_exg_paths(example_dir):
    exg_paths = {}
    pl_suffix = '.pl'
    for filename in os.listdir(example_dir):
        if filename.endswith(pl_suffix):
            # Ensure the name of the file only contains intergers.
            try:
                exg = int(filename.removesuffix(pl_suffix))
            except:
                continue
            exg_paths[exg] = os.path.join(example_dir, filename)
    return exg_paths

def filter_tac(i, tac, exg_paths, prolog, good):
    # Why passing Prolog from filter_row cause warnings?
    # prolog = Prolog()
    # prolog.assertz('style_check(-singleton)') error ?
    prolog.consult(exg_paths[i])
    try:
        print(f'tac({i}, \"{tac}\")')
        good.put(bool(list(prolog.query(f'tac({i}, \"{tac}\")'))))
    except:
        # TODO: better solution instead of ignoring the error.
        # Clause may contain predicates that not in the example. Now, I
        # treat it as failure and continue. Add all predicates initially
        # seems cause warnings in Prolog.
        good.put(False)

def filter_row(i, r, exg_paths, prolog):
    new_preds = []
    preds = r.split('\t')
    for pred in preds:
        good = Queue()
        child = Process(target=filter_tac, args=(i, pred, exg_paths, prolog, good,))
        child.start()
        child.join()
        if good.get():
            new_preds.append(pred)
    print(new_preds)
    return new_preds


def filter(exg_paths, prolog, pred_file):
    preds_mat = []
    i = 0
    with open(pred_file, 'r') as f:
        for r in f:
            r = r.strip()
            if utils.not_lemma(r) :
                preds = filter_row(i, r, exg_paths, prolog)
                preds = '\t'.join(preds)
                preds_mat.append(preds)
            else:
                preds_mat.append(r)
            i += 1
            if i % 100 == 0:
                print(i, datetime.now().strftime("%m-%d-%Y-%H:%M:%S"))
                # return preds_mat
    return preds_mat

def out(pred_mat, pred_file, clause_dir, label):
    now = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    out_dir = os.path.join(os.path.dirname(pred_file), f'filter/{now}')
    os.makedirs(out_dir)
    out = os.path.join(out_dir, os.path.basename(pred_file))
    with open(out, 'w') as w:
        for preds in pred_mat:
            w.write(preds + '\n')
    acc.acc(out, label)
    log = {
        'clause_dir': clause_dir,
    }
    with open(os.path.join(out_dir, 'log.json'), 'w') as w:
        json.dump(log, w, indent=4)

clause_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/filter'
pred_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/filter/test.eval'

example_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/filter'
label = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split/split8.label'
exg_paths = read_exg_paths(example_dir)
prolog = read_clauses(clause_dir, Prolog())
preds = filter(exg_paths, prolog, pred_file)
# out(preds, pred_file, clause_dir, label)