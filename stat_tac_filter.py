import json
import os

import argparse
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue
from pyswip import Prolog

from lib import utils

PL_SUFFIX = ".pl"


def read_all_predc(all_predc, prolog):
    prolog.consult(all_predc)
    return prolog


def load_clauses(dir):
    cls = []
    for filename in os.listdir(dir):
        if filename.endswith(PL_SUFFIX):
            cls.append(os.path.join(dir, filename))
    cls.sort()
    return cls


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


def check_cls(i, tac, prolog, cls, good):
    prolog.consult(cls)
    good.put(bool(list(prolog.query(f'tac({i}, "{tac}")'))))


def check_clss(i, tac, exg_paths, prolog, queue, clss):
    prolog.consult(exg_paths[i])
    acc = []
    rej = []
    for j in range(len(clss)):
        good = Queue()
        child = Process(
            target=check_cls,
            args=(i, tac, prolog, clss[j], good),
        )
        child.start()
        if good.get() == None:
            acc.append(j)
        else:
            rej.append(j)
    queue.put((acc, rej))


def filter_row(i, tac, exg_paths, prolog, clss):
    queue = Queue()
    child = Process(
        target=check_clss,
        args=(i, utils.safe_tac(tac), exg_paths, prolog, queue, clss),
    )
    child.start()
    child.join(timeout=5)
    child.terminate()
    if child.exitcode == None:
        acc, rej = [], [clss]
    else:
        acc, rej = queue.get()
    return acc, rej


def filter(exg_paths, prolog, f_pred, cls, f_label, tac):
    stats = {}
    i = 0
    with open(f_pred, "r") as r_preds, open(f_label, "r") as r_labels:
        preds = r_preds.readlines()
        labels = r_labels.readlines()
    for pred, label in zip(preds, labels):
        pred = pred.strip()
        label = label.strip()
        if (utils.not_lemma(pred)) & (tac in pred):
            acc, rej = filter_row(i, pred, exg_paths, prolog, cls)
            if tac == label:
                stats[i] = {"TN": [], "TP": acc, "FN": rej, "FP": []}
            else:
                stats[i] = {"TN": rej, "TP": [], "FN": [], "FP": acc}
        i += 1
        print(i)
        print(stats)
        if i % 100 == 0:
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
prolog = read_all_predc(opts.all_predc, Prolog())
cls = load_clauses(opts.clause)

stats = filter(exg_paths, prolog, opts.pred, cls, opts.label, opts.tac)
print(stats)
