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


def detail_ilp_stat_ml(dict):
    all_tp = 0
    all_tn = 0
    all_fp = 0
    all_fn = 0
    for tac, stat in dict.items():
        # neg = stat["TN"] + stat["FN"]
        # all = neg + stat["TP"] + stat["FP"]

        # if neg == 0:
        #     dict[tac]["npv"] = 1
        # else:
        #     dict[tac]["npv"] = stat["TN"] / (stat["TN"] + stat["FN"])

        # dict[tac]["tn_div_all"] = stat["TN"] / all
        tp = stat["TP"]
        tn = stat["TN"]
        fp = stat["FP"]
        fn = stat["FN"]
        all_tp += tp
        all_tn += tn
        all_fp += fp
        all_fn += fn
        pred = [1] * (tp + fp) + [0] * (tn + fn)
        label = [1] * tp + [0] * fp + [0] * tn + [1] * fn
        f1 = f1_score(label, pred, average="binary", zero_division=1)
        dict[tac]["f1"] = f1
        if fp + fn == 0:
            dict[tac]["filter_acc"] = 1
        else:
            dict[tac]["filter_acc"] = (tp + tn) / (tp + tn + fp + fn)
    new_dict = {}
    new_dict["filter_acc"] = (all_tp + all_tn) / (all_fp + all_fn)
    new_dict["TP"] = all_tp
    new_dict["TN"] = all_tn
    new_dict["FP"] = all_fp
    new_dict["FN"] = all_fn
    new_dict["tac"] = dict
    return new_dict


# def stat_top1(reorders, labels, stat):
#     i = 0
#     for pred, label in zip(reorders, labels):
#         if (utils.not_lemma(label)) & (pred != []) & (pred[0] == label):
#             if "top1" not in stat[label].keys():
#                 stat[label]["top1"] = [i]
#             else:
#                 stat[label]["top1"].append(i)
#         i += 1

#     for _, tac_stat in stat.items():
#         if "top1" in tac_stat.keys():
#             tac_stat["top1"] = {"num": len(tac_stat["top1"]), "id": tac_stat["top1"]}
#     return stat


def stat_ilp(predss, label):
    n_preds = 0
    n_corr = 0
    for preds, l in zip(predss, label):
        if l in preds:
            n_corr += 1
        n_preds += len(preds)
    if n_corr == 0:
        score = 0
    else:
        score = n_preds / n_corr
    return n_preds, n_corr, score


def stat_ilp_stat_ml(f_good, f_label, f_pred, f_reorder):
    labels, goodss, predss, reorders = load(f_good, f_label, f_pred, f_reorder)

    tac_stats = {}
    for goods, label, preds in zip(goodss, labels, predss):
        if utils.not_lemma(label):
            preds = preds[:10]
            for p in preds:
                if p not in tac_stats.keys():
                    tac_stats[p] = {"num": 1, "TP": 0, "TN": 0, "FP": 0, "FN": 0}
                else:
                    tac_stats[p]["num"] += 1

                is_good = p in goods
                is_correct = p == label
                if is_good & is_correct:
                    tac_stats[p]["TP"] += 1
                elif is_good & (not is_correct):
                    tac_stats[p]["FP"] += 1
                elif (not is_good) & (not is_correct):
                    tac_stats[p]["TN"] += 1
                else:
                    tac_stats[p]["FN"] += 1

    items = tac_stats.items()
    tac_stats = dict(sorted(items, key=lambda x: x[1]["num"], reverse=True))
    tac_stats = detail_ilp_stat_ml(tac_stats)
    n_preds, n_corr, score = stat_ilp(predss, labels)
    tac_stats["ilp_pred"] = n_preds
    tac_stats["ilp_corr"] = n_corr
    tac_stats["ilp_score"] = score
    # log = top1_stat | tac_stats
    # for tac, stat in tac_stats.ite
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
    args = parser.parse_args()
    stat_ilp_stat_ml(args.good, args.label, args.pred, args.reorder)
