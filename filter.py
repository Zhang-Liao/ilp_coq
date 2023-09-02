import json
import os

from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue
from pyswip import Prolog

from lib import utils
from statis import acc


def read_clauses(clause_file, prolog):
    prolog.consult(clause_file)
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
        # print(f'tac({i}, \"{tac}\")')
        good.put(bool(list(prolog.query(f'tac({i}, \"{tac}\")'))))
    except:
        # TODO: better solution instead of ignoring the error.
        # Clause may contain predicates that not in the example. Now, I
        # treat it as failure and continue. Add all predicates initially
        # seems cause warnings in Prolog.
        good.put(False)

def filter_row(i, r, exg_paths, prolog):
    good_preds = []
    bad_preds = []
    preds = r.split('\t')
    for pred in preds:
        good = Queue()
        safe_pred = utils.safe_tac(pred)
        child = Process(target=filter_tac, args=(i, safe_pred, exg_paths, prolog, good,))
        child.start()
        child.join()
        if good.get():
            good_preds.append(pred)
        else:
            bad_preds.append(pred)
    new_preds = good_preds + bad_preds
    # print(new_preds)
    return good_preds, new_preds


def filter(exg_paths, prolog, pred_file):
    good_pred_mat = []
    reordered_mat = []
    i = 0
    with open(pred_file, 'r') as f:
        for r in f:
            r = r.strip()
            if utils.not_lemma(r) :
                good_preds, reordered = filter_row(i, r, exg_paths, prolog)
                good_preds = '\t'.join(good_preds)
                reordered = '\t'.join(reordered)
                good_pred_mat.append(good_preds)
                reordered_mat.append(reordered)
            else:
                good_pred_mat.append(r)
                reordered_mat.append(r)
            i += 1
            if i % 100 == 0:
                print(i, datetime.now().strftime("%m-%d-%Y-%H:%M:%S"))
                # return preds_mat
    return good_pred_mat, reordered_mat

def out(good_preds, reordered_preds, pred_file, clause, label):
    now = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    out_dir = os.path.join(os.path.dirname(pred_file), f'filter/{now}')
    good_dir = os.path.join(out_dir, 'good')
    os.makedirs(good_dir)
    good = os.path.join(good_dir, os.path.basename(pred_file))
    with open(good, 'w') as w:
        for preds in good_preds:
            w.write(preds + '\n')
    acc.acc(good, label)

    reordered_dir = os.path.join(out_dir, 'reorder')
    os.makedirs(reordered_dir)
    reordered = os.path.join(reordered_dir, os.path.basename(pred_file))
    with open(reordered, 'w') as w:
        for preds in reordered_preds:
            w.write(preds + '\n')
    acc.acc(reordered, label)

    log = {
        'clause': clause,
    }
    with open(os.path.join(out_dir, 'log.json'), 'w') as w:
        json.dump(log, w, indent=4)

clause_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto/alltac_rule.pl'
pred_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split/06-27-2023-10:26:47/split8.eval'
example_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split8/test_predc'
label = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split/split8.label'
# label = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split8/test_predc_3/5.label'
exg_paths = read_exg_paths(example_dir)
prolog = read_clauses(clause_file, Prolog())
good_preds, reordered_preds = filter(exg_paths, prolog, pred_file)
out(good_preds, reordered_preds, pred_file, clause_file, label)