#!/bin/env python3
import os
import sys
import json

import argparse
from sklearn.metrics import f1_score

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def round_f(acc):
    return round(acc * 100, 5)


def load(f_pred, f_label, f_good):
    with open(f_label, "r") as f:
        labels = f.read().splitlines()
    labels = [l.strip() for l in labels]

    with open(f_pred, "r") as f:
        preds = f.read().splitlines()
    preds = [l.strip().split("\t") for l in preds]

    with open(f_good, "r") as f:
        goods = f.read().splitlines()
    goods = [l.strip().split("\t") for l in goods]
    assert (len(preds) == len(labels)) & (len(goods) == len(labels))
    return preds, labels, goods


def cal_f1(tp, fp, fn):
    pred = [1] * (tp + fp) + [0] * fn
    label = [1] * tp + [0] * fp + +[1] * fn
    return f1_score(label, pred, average="binary", zero_division=1)


def update_tp(all_tp, all_fp, all_fn, tp, fp, fn):
    all_tp += tp
    all_fp += fp
    all_fn += fn
    return all_tp, all_fp, all_fn


def init_tp():
    return 0, 0, 0


def stat_ilp(dic):
    all_tp, all_fp, all_fn = init_tp()
    no_ign_tp, no_ign_fp, no_ign_fn = init_tp()
    for tac, stat in dic.items():
        tp = stat["TP"]
        fp = stat["FP"]
        fn = stat["FN"]
        all_tp, all_fp, all_fn = update_tp(all_tp, all_fp, all_fn, tp, fp, fn)
        if tac not in utils.IGNORED_TACS:
            no_ign_tp, no_ign_fp, no_ign_fn = update_tp(
                no_ign_tp, no_ign_fp, no_ign_fn, tp, fp, fn
            )

        dic[tac]["f1"] = cal_f1(tp, fp, fn)

    ilp_stat = {
        "TP": all_tp,
        "FP": all_fp,
        "FN": all_fn,
        "f1": cal_f1(all_tp, all_fp, all_fn),
        "f1_no_ignored_tac": cal_f1(no_ign_tp, no_ign_fp, no_ign_fn),
    }
    new_dict = ilp_stat | dic
    return new_dict


def stat_one_pred(stats, good, label):
    for tac in good:
        if tac not in stats.keys():
            stats[tac] = {"num": 1, "TP": 0, "FP": 0, "FN": 0}
        else:
            stats[tac]["num"] += 1
        if tac == label:
            stats[tac]["TP"] += 1
        else:
            stats[tac]["FP"] += 1
    if label not in good:
        stats[label]["FN"] += 1

    return stats


def stat_ilp(f_pred, f_label):
    preds, labels = load(f_pred, f_label)

    tac_stats = {}
    for label, pred in zip(labels, preds):
        if utils.not_lemma(label):
            tac_stats = stat_one_pred(tac_stats, pred, label)
    items = tac_stats.items()
    tac_stats = dict(sorted(items, key=lambda x: x[1]["num"], reverse=True))
    tac_stats = stat_ilp(tac_stats)

    out_dir = os.path.dirname(f_pred)
    with open(os.path.join(out_dir, "stat_ilp_pred.json"), "w") as w:
        json.dump(tac_stats, w)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns false positive and false negative."
    )
    parser.add_argument("--pred", type=str)
    parser.add_argument("--label", type=str)

    args = parser.parse_args()
    stat_ilp(args.pred, args.label)
