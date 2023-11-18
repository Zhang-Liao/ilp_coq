import json
import os
import warnings

import argparse
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue
from pyswip import Prolog
import shutil

from lib import utils
from stats import acc
from stats import stat_ilp_pred


def read_clauses(clause_file, all_predc, prolog):
    prolog.consult(clause_file)
    prolog.consult(all_predc)
    return prolog


def read_exg_paths(example_dir):
    exg_paths = {}
    pl_suffix = ".pl"
    for filename in os.listdir(example_dir):
        if filename.endswith(pl_suffix):
            try:
                exg = int(filename.removesuffix(pl_suffix))
            except:
                continue
            exg_paths[exg] = os.path.join(example_dir, filename)
    return exg_paths


def mk_pred(i, exg_paths, prolog, good):
    pred = set()
    prolog.consult(exg_paths[i])
    raw_pred = list(prolog.query(f"tac({i}, Tac)"))
    for soln in raw_pred:
        pred.add(soln["Tac"])
    good.put(pred)
    # except:


def pred_row(i, exg_paths, prolog):
    good = Queue()
    child = Process(
        target=mk_pred,
        args=(
            i,
            exg_paths,
            prolog,
            good,
        ),
    )
    child.start()
    child.join(timeout=5)
    child.terminate()
    if child.exitcode == None:
        pred = []
    else:
        pred = good.get()
    return pred


def ilp_pred(exg_paths, prolog, label_f):
    preds = []
    i = 0
    with open(label_f, "r") as f:
        for r in f:
            r = r.strip()
            if utils.not_lemma(r):
                pred = pred_row(i, exg_paths, prolog)
                pred = [str(p, encoding="utf-8") for p in pred]
                pred = "\t".join(pred)
                preds.append(pred)
            else:
                preds.append(r)
            i += 1
            if i % 100 == 0:
                print(i, datetime.now().strftime("%m-%d-%Y-%H:%M:%S"))
                # return preds_mat
    return preds


def out_stat_ilp(ilp_pred, out_theory, clause, label, info):
    theory = out_theory.split("/")[-1]
    out_dir = os.path.join(out_theory, info)
    pred_dir = os.path.join(out_dir, "ilp_pred")
    # if os.path.exists(pred_dir):
    #     shutil.rmtree(pred_dir)
    #     warnings.warn("remove the existed statistic in " + pred_dir)
    if not os.path.exists(pred_dir):
        os.makedirs(pred_dir)
    shutil.copy(clause, out_dir)
    ilp_pred_f = os.path.join(pred_dir, os.path.basename(theory) + ".eval")
    with open(ilp_pred_f, "w") as w:
        for pred in ilp_pred:
            w.write(pred + "\n")
    print('ilp_pred_f', ilp_pred_f)
    stat_ilp_pred.stat_ilp(ilp_pred_f, label)

    log = {
        "clause": clause,
    }
    with open(os.path.join(out_dir, "log.json"), "w") as w:
        json.dump(log, w, indent=4)


parser = argparse.ArgumentParser()
parser.add_argument("--clause", type=str)
parser.add_argument("--out_theory", type=str, default=None)
parser.add_argument("--test", type=str)
parser.add_argument("--label", type=str)
parser.add_argument("--all_predc", type=str)
parser.add_argument("--info", type=str, help="specify the output dir")

opts = parser.parse_args()


exg_paths = read_exg_paths(opts.test)
prolog = read_clauses(opts.clause, opts.all_predc, Prolog())
preds = ilp_pred(exg_paths, prolog, opts.label)
out_stat_ilp(preds, opts.out_theory, opts.clause, opts.label, opts.info)
