import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))

import argparse
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue
from pyswip import Prolog

from lib import utils

PL_SUFFIX = ".pl"


def read_clauses(clause_file, all_predc, prolog):
    prolog.consult(clause_file)
    prolog.consult(all_predc)
    return prolog


def all_cls_ids(cls):
    with open(cls, "r") as r:
        dat = r.readlines()
        dat = [r for r in dat if r.startswith("tac")]
    return set(range(len(dat)))


def read_exg_paths(example_dir):
    exg_paths = {}
    for filename in os.listdir(example_dir):
        if filename.endswith(PL_SUFFIX):
            # Ensure the name of the file only contains intergers.
            try:
                exg = int(filename.removesuffix(PL_SUFFIX))
            except:
                continue
            exg_paths[exg] = os.path.join(example_dir, filename)
    return exg_paths


def check_cls(i, tac, exg_paths, prolog, queue):
    prolog.consult(exg_paths[i])
    soln = prolog.query(f'tac({i}, "{tac}", TacId)')
    # print(f'tac({i}, "{tac}", TacId)')
    # exit(0)
    acc = [s["TacId"] for s in soln]
    # queue.put(bool(list(prolog.query(f'tac({i}, "{tac}")'))))
    queue.put(set(acc))
    return queue


def filter_row(i, tac, exg_paths, prolog):
    queue = Queue()
    child = Process(
        target=check_cls,
        args=(i, utils.safe_tac(tac), exg_paths, prolog, queue),
    )
    child.start()
    child.join(timeout=5)
    child.terminate()
    # exit()
    if child.exitcode == None:
        acc = []
    else:
        acc = list(queue.get())
    return acc


def filter(exg_paths, prolog, f_pred, f_label, tac, all_cls):
    stats = {}
    i = 0
    with open(f_pred, "r") as r_preds, open(f_label, "r") as r_labels:
        preds = r_preds.readlines()
        labels = r_labels.readlines()
    for pred, label in zip(preds, labels):
        pred = pred.strip()
        label = label.strip()
        if (utils.not_lemma(pred)) & (tac in pred):
            acc = filter_row(i, tac, exg_paths, prolog)
            # rej = all_cls.difference(acc)
            if tac == label:
                if acc == []:
                    stats[i] = "FN"
                else:
                    stats[i] = {"TP": acc}
            else:
                if acc == []:
                    stats[i] = "TN"
                else:
                    stats[i] = {"FP": acc}
        i += 1
        if i % 1000 == 0:
            print(i, datetime.now().strftime("%m-%d-%Y-%H:%M:%S"))
    return stats


parser = argparse.ArgumentParser()
parser.add_argument("--clause", type=str)
parser.add_argument("--pred", type=str)
parser.add_argument("--test", type=str)
parser.add_argument("--label", type=str)
parser.add_argument("--all_predc", type=str)
parser.add_argument("--tac", type=str)

opts = parser.parse_args()

assert opts.pred.endswith(".eval")

exg_paths = read_exg_paths(opts.test)
prolog = read_clauses(opts.clause, opts.all_predc, Prolog())
all_cls = all_cls_ids(opts.clause)
stats = filter(exg_paths, prolog, opts.pred, opts.label, opts.tac, all_cls)
out = os.path.splitext(opts.clause)[0] + "_stat.json"

with open(out, "w") as w:
    json.dump(stats, w, indent=4)
# print(stats)
