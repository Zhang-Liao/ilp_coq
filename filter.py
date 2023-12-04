import json
import os
import warnings

import argparse
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue
from pyswip import Prolog
import re
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
    pl_suffix = ".pl"
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
    prolog.consult(exg_paths[i])
    query = list(prolog.query(f'tac({i},"{tac}",X)'))
    pos_ids = sorted(set([int(p["X"]) for p in query]))
    good.put(pos_ids)


def filter_row(i, row, exg_paths, prolog):
    accept_dic = {}
    preds = row.split("\t")[:20]
    for pred in preds:
        good = Queue()
        safe_pred = utils.safe_tac(pred)
        child = Process(
            target=filter_tac,
            args=(
                i,
                safe_pred,
                exg_paths,
                prolog,
                good,
            ),
        )
        child.start()
        child.join(timeout=5)
        child.terminate()
        # not over the time limit
        if child.exitcode != None:
            accepts = good.get()
            if accepts != []:
                accept_dic[pred] = accepts
    # print(new_preds)
    return accept_dic


def filter_stat_ml(exg_paths, prolog, pred_file):
    accept_dics = []
    i = 0
    with open(pred_file, "r") as f:
        for r in f:
            r = r.strip()
            if utils.not_lemma(r):
                accept_dic = filter_row(i, r, exg_paths, prolog)
                accept_dics.append(accept_dic)
            else:
                accept_dics.append(r)
            i += 1
            if i % 100 == 0:
                print(i, datetime.now().strftime("%m-%d-%Y-%H:%M:%S"))
                # return preds_mat
    return accept_dics


def out_stat_ml(accept_dics, f_pred, f_rule, label, info):
    out_dir = os.path.join(f_pred[:-5], info)
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
        warnings.warn("remove the existed statistic in " + out_dir)
    good_dir = os.path.join(out_dir, "good")
    if not os.path.exists(good_dir):
        os.makedirs(good_dir)
    shutil.copy(f_rule, out_dir)
    good = os.path.join(good_dir, os.path.basename(f_pred))
    with open(good, "w") as w:
        for accept in accept_dics:
            w.write(json.dumps(accept) + "\n")

    labels, goodss, predss, rule_ids, _ = stat_filter.init_dat(
        good, label, f_pred, f_rule
    )

    stat_filter.stat_ilp_stat_ml(goodss, labels, predss, rule_ids, good_dir)


# def out_stat_ml(_, f_pred, f_rule, label, info):
#     out_dir = os.path.join(f_pred[:-5], info)
#     good_dir = os.path.join(out_dir, "good")
#     good = os.path.join(good_dir, os.path.basename(f_pred))

#     labels, goodss, predss, rule_ids, _ = stat_filter.init_dat(
#         good, label, f_pred, f_rule
#     )

#     stat_filter.stat_ilp_stat_ml(goodss, labels, predss, rule_ids, good_dir)


parser = argparse.ArgumentParser()
parser.add_argument("--clause", type=str)
parser.add_argument("--pred", type=str, default=None)
parser.add_argument("--test", type=str)
parser.add_argument("--label", type=str)
parser.add_argument("--bk", type=str)
parser.add_argument("--info", type=str, help="specify the output dir")

opts = parser.parse_args()


exg_paths = read_exg_paths(opts.test)
prolog = read_clauses(opts.clause, opts.bk, Prolog())
assert opts.pred.endswith(".eval")
accept_dics = filter_stat_ml(exg_paths, prolog, opts.pred)
out_stat_ml(accept_dics, opts.pred, opts.clause, opts.label, opts.info)
# out_stat_ml([], opts.pred, opts.clause, opts.label, opts.info)
