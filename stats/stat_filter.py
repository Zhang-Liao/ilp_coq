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


def load(f_good, f_label, f_pred):
    with open(f_label, "r") as f:
        labels = f.read().splitlines()
    labels = [l.strip() for l in labels]

    with open(f_good, "r") as f:
        goodss = f.read().splitlines()
    goodss = [l.strip().split("\t") for l in goodss]

    with open(f_pred, "r") as f:
        predss = f.read().splitlines()
    predss = [l.strip().split("\t") for l in predss]

    assert len(goodss) == len(labels)
    return labels, goodss, predss


def detail_stat(dict):
    for tac, stat in dict.items():
        # neg = stat["TN"] + stat["FN"]
        # all = neg + stat["TP"] + stat["FP"]

        # if neg == 0:
        #     dict[tac]["npv"] = 1
        # else:
        #     dict[tac]["npv"] = stat["TN"] / (stat["TN"] + stat["FN"])

        # dict[tac]["tn_div_all"] = stat["TN"] / all
        pred = [1] * (stat['TP'] + stat['FP']) + [0] * (stat['TN'] + stat['FN'])
        label = [1] * stat['TP'] + [0] * stat['FP'] + [0] * stat['TN'] + [1] * stat['FN']
        # truth = dict[tac]['TP'] + dict[tac]['TN']
        # false = stat["FP"] + stat["FN"]
        f1 = f1_score(label, pred, average='binary', zero_division = 1)
        dict[tac]['f1'] = f1
    return dict


def stat(f_good, f_label, f_pred):
    labels, goodss, predss = load(f_good, f_label, f_pred)

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
    tac_stats = detail_stat(tac_stats)
    stats = tac_stats.values()

    truth_neg = sum([s["TN"] for s in stats])
    false_neg = sum([s["FN"] for s in stats])
    all = sum([s["TN"] + s["TP"] + s["FN"] + s["FP"] for s in stats])
    neg_pred_v = truth_neg / (truth_neg + false_neg)
    tn_div_all = truth_neg / all

    log = {"npv": neg_pred_v, "tn_div_all": tn_div_all}
    log = log | tac_stats
    # for tac, stat in tac_stats.ite
    out_dir = os.path.dirname(f_good)
    with open(os.path.join(out_dir, "stat_filter.json"), "w") as w:
        json.dump(log, w, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns false positive and false negative."
    )
    parser.add_argument("--good", type=str)
    parser.add_argument("--pred", type=str)
    parser.add_argument("--label", type=str)
    args = parser.parse_args()
    stat(args.good, args.label, args.pred)
