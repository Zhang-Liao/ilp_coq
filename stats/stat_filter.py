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


def load(f_good, f_label, f_pred, f_reorder):
    with open(f_label, "r") as f:
        labels = f.read().splitlines()
    labels = [l.strip() for l in labels]

    with open(f_good, "r") as f:
        goodss = f.read().splitlines()
    goodss = [l.strip().split("\t") for l in goodss]

    with open(f_pred, "r") as f:
        predss = f.read().splitlines()
    predss = [l.strip().split("\t") for l in predss]

    with open(f_reorder, "r") as f:
        reorders = f.read().splitlines()
    reorders = [l.strip().split("\t") for l in reorders]

    assert (len(goodss) == len(labels)) & (len(reorders) == len(labels))
    return labels, goodss, predss, reorders


def cal_f1(tp, fp, tn, fn):
    pred = [1] * (tp + fp) + [0] * (tn + fn)
    label = [1] * tp + [0] * fp + [0] * tn + [1] * fn
    return f1_score(label, pred, average="binary", zero_division=1)


def update_tp(all_tp, all_tn, all_fp, all_fn, tp, tn, fp, fn):
    all_tp += tp
    all_tn += tn
    all_fp += fp
    all_fn += fn
    return all_tp, all_tn, all_fp, all_fn


def init_tp():
    return 0, 0, 0, 0


def stat_ilp(dic):
    all_tp, all_tn, all_fp, all_fn = init_tp()
    no_ign_tp, no_ign_tn, no_ign_fp, no_ign_fn = init_tp()
    for tac, stat in dic.items():
        tp = stat["TP"]
        tn = stat["TN"]
        fp = stat["FP"]
        fn = stat["FN"]
        all_tp, all_tn, all_fp, all_fn = update_tp(
            all_tp, all_tn, all_fp, all_fn, tp, tn, fp, fn
        )
        if tac not in utils.IGNORED_TACS:
            no_ign_tp, no_ign_tn, no_ign_fp, no_ign_fn = update_tp(
                no_ign_tp, no_ign_tn, no_ign_fp, no_ign_fn, tp, tn, fp, fn
            )

        dic[tac]["f1"] = cal_f1(tp, fp, tn, fn)

    ilp_stat = {
        "TP": all_tp,
        "TN": all_tn,
        "FP": all_fp,
        "FN": all_fn,
        "f1": cal_f1(all_tp, all_fp, all_tn, all_fn),
        "f1_without_ignored_tac": cal_f1(no_ign_tp, no_ign_fp, no_ign_tn, no_ign_fn),
    }
    new_dict = ilp_stat | dic
    return new_dict


def stat_one_pred(p, stats, goods, label):
    if p not in stats.keys():
        stats[p] = {"num": 1, "TP": 0, "TN": 0, "FP": 0, "FN": 0}
    else:
        stats[p]["num"] += 1

    is_good = p in goods
    is_correct = p == label
    if is_good & is_correct:
        stats[p]["TP"] += 1
    elif is_good & (not is_correct):
        stats[p]["FP"] += 1
    elif (not is_good) & (not is_correct):
        stats[p]["TN"] += 1
    else:
        stats[p]["FN"] += 1
    return stats


def stat_ilp_stat_ml(f_good, f_label, f_pred, f_reorder, common):
    labels, goodss, predss, reorders = load(f_good, f_label, f_pred, f_reorder)

    tac_stats = {}
    for goods, label, preds in zip(goodss, labels, predss):
        if utils.not_lemma(label):
            preds = preds[:20]
            for p in preds:
                if common:
                    if p in utils.COMMON_TAC:
                        tac_stats = stat_one_pred(p, tac_stats, goods, label)
                else:
                    tac_stats = stat_one_pred(p, tac_stats, goods, label)
    items = tac_stats.items()
    tac_stats = dict(sorted(items, key=lambda x: x[1]["num"], reverse=True))
    tac_stats = stat_ilp(tac_stats)

    out_dir = os.path.dirname(f_good)
    with open(os.path.join(out_dir, "stat_filter.json"), "w") as w:
        json.dump(tac_stats, w)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns false positive and false negative."
    )
    parser.add_argument("--good", type=str)
    parser.add_argument("--reorder", type=str)
    parser.add_argument("--pred", type=str)
    parser.add_argument("--label", type=str)
    parser.add_argument("--only_common", action="store_true")
    args = parser.parse_args()
    stat_ilp_stat_ml(args.good, args.label, args.pred, args.reorder, args.only_common)
