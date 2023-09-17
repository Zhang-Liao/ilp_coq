import json
import os

import argparse
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue
from pyswip import Prolog
import shutil

from lib import utils
from stats import acc
from stats import stat_filter

def read_clauses(clause_file, all_predc, prolog):
    prolog.consult(clause_file)
    prolog.consult(all_predc)
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
        # print(f'tac({i}, \"{tac}\")')
    good.put(bool(list(prolog.query(f'tac({i}, \"{tac}\")'))))
    # except:
        # TODO: better solution instead of ignoring the error.
        # Clause may contain predicates that not in the example. Now, I
        # treat it as failure and continue. Add all predicates initially
        # seems cause warnings in Prolog.

def filter_row(i, r, exg_paths, prolog):
    good_preds = []
    bad_preds = []
    preds = r.split('\t')[:10]
    for pred in preds:
        good = Queue()
        safe_pred = utils.safe_tac(pred)
        child = Process(target=filter_tac, args=(i, safe_pred, exg_paths, prolog, good,))
        child.start()
        child.join(timeout = 5)
        child.terminate()
        if child.exitcode == None:
            good_preds.append(pred)
        else:
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

def out(good_preds, reordered_preds, f_pred, clause, label):
    now = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    out_dir = os.path.join(f_pred[:-5], f'filter/{now}')
    good_dir = os.path.join(out_dir, 'good')    
    os.makedirs(good_dir)
    shutil.copy(clause, out_dir)
    good = os.path.join(good_dir, os.path.basename(f_pred))
    with open(good, 'w') as w:
        for preds in good_preds:
            w.write(preds + '\n')
    acc.acc(good, label)

    reordered_dir = os.path.join(out_dir, 'reorder')
    os.makedirs(reordered_dir)
    reordered = os.path.join(reordered_dir, os.path.basename(f_pred))
    with open(reordered, 'w') as w:
        for preds in reordered_preds:
            w.write(preds + '\n')
    acc.acc(reordered, label)

    stat_filter.stat(good, label, f_pred)

    log = {
        'clause': clause,
    }
    with open(os.path.join(out_dir, 'log.json'), 'w') as w:
        json.dump(log, w, indent=4)
    

parser = argparse.ArgumentParser()
parser.add_argument("--clause", type=str)
parser.add_argument("--pred", type=str)
parser.add_argument("--test", type=str)
parser.add_argument("--label", type=str)
parser.add_argument("--all_predc", type=str)
opts = parser.parse_args()

assert(opts.pred.endswith('.eval'))

exg_paths = read_exg_paths(opts.test)
prolog = read_clauses(opts.clause, opts.all_predc, Prolog())
good_preds, reordered_preds = filter(exg_paths, prolog, opts.pred)
out(good_preds, reordered_preds, opts.pred, opts.clause, opts.label)