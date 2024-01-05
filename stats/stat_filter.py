#!/bin/env python3
import os
import sys
import json

import argparse
import re

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def init_tac_stat():
    return {"TP": 0, "FP": 0, "FN": 0, 'TN': 0, "rule": {}}


def init_rule_stat():
    return {"TP": 0, "FP": 0, "FN": 0, "TN": 0}


def init_stat(rule_ids):
    stat = {"tactic": {}}
    for tac, ids in rule_ids.items():
        stat["tactic"][tac] = init_tac_stat()
        for id in ids:
            stat["tactic"][tac]["rule"][id] = init_rule_stat()
    return stat


def update_dic(dic, default, key, subkey):
    if key not in dic.keys():
        dic[key] = default
    else:
        dic[key][subkey] += 1


def mk_rule_ids_dic(dat):
    dic = {}
    for r in dat:
        r = r.strip()
        hd = re.match(
            r"tac\(A,\"(?P<tac>.*)\",(?P<i>[0-9]+)\).*",
            r,
        )
        if hd != None:
            hd = hd.groupdict()
            tac = str(hd["tac"])
            i = int(hd["i"])
            if tac not in dic.keys():
                dic[tac] = set([i])
            else:
                dic[tac].add(i)
    return dic


def round_f(acc):
    return round(acc * 100, 5)


def load(f_good, f_label, f_pred, f_rule):
    with open(f_label, "r") as f:
        labels = f.read().splitlines()
    labels = [l.strip() for l in labels]

    with open(f_good, "r") as f:
        goodss = f.read().splitlines()
    goodss = [json.loads(l) for l in goodss]

    with open(f_pred, "r") as f:
        predss = f.read().splitlines()
    predss = [l.strip().split("\t") for l in predss]

    with open(f_rule, "r") as f:
        rules = f.readlines()
    rules = [l.strip() for l in rules]
    assert len(goodss) == len(labels)
    return labels, goodss, predss, rules


def cal_f1(tp, fp, fn):
    denomin = 2 * tp + fp + fn
    if denomin == 0:
        f1 = 0
    else:
        f1 = (2 * tp) / denomin
    return round(f1, 7)


def update_tp(all_tp, all_fp, all_fn, tp, fp, fn):
    all_tp += tp
    all_fp += fp
    all_fn += fn
    return all_tp, all_fp, all_fn


def init_tp():
    return 0, 0, 0


def cal_precision(rules):
    for r, stat in rules.items():
        if r not in ["TP", "FP", "FN", "TN"]:
            pos = stat["TP"] + stat["FP"]
            if pos == 0:
                stat["precision"] = 0
            else:
                stat["precision"] = round(stat["TP"] / pos, 7)


def cal_f1_precision(stat):
    all_tp, all_fp, all_fn = init_tp()
    for tac, tac_stat in stat["tactic"].items():
        tp = tac_stat["TP"]
        fp = tac_stat["FP"]
        fn = tac_stat["FN"]
        all_tp, all_fp, all_fn = update_tp(all_tp, all_fp, all_fn, tp, fp, fn)
        cal_precision(tac_stat["rule"])
        tac_stat["f1"] = cal_f1(tp, fp, fn)
    ilp_stat = {
        "TP": all_tp,
        "FP": all_fp,
        "FN": all_fn,
        "f1": cal_f1(all_tp, all_fp, all_fn),
    }
    new_dict = ilp_stat | stat
    return new_dict


def update_rule_id_stat(stat, goods, bads, good_key, bad_key):
    for good in goods:
        stat[good][good_key] += 1

    for bad in bads:
        stat[bad][bad_key] += 1


def clean_stat(stat):
    tac_to_clean = []
    for tac, values in stat.items():
        if values["TP"] + values["FP"] + values["FN"] == 0:
            tac_to_clean.append(tac)

    for tac in tac_to_clean:
        del stat[tac]


def stat_one_pred(p, stats, goods, label, rule_ids):
    # print(stats.keys())
    # exit()
    if p not in stats.keys():
        stats[p] = init_tac_stat()

    if p in goods.keys():
        is_good = True
        good_ids = goods[p]
    else:
        is_good = False
        good_ids = []

    is_correct = p == label
    if is_good & is_correct:
        ids = rule_ids[p]
        bad_ids = ids.difference(good_ids)
        stats[p]["TP"] += 1
        update_rule_id_stat(
            stats[p]["rule"],
            good_ids,
            bad_ids,
            "TP",
            "FN",
        )
    elif is_good & (not is_correct):
        ids = rule_ids[p]
        bad_ids = ids.difference(good_ids)
        stats[p]["FP"] += 1
        update_rule_id_stat(
            stats[p]["rule"],
            good_ids,
            bad_ids,
            "FP",
            "TN",
        )
    elif (not is_good) & is_correct:
        if p in rule_ids.keys():
            good_ids = []
            bad_ids = rule_ids[p]
        else:
            good_ids = []
            bad_ids = []
        stats[p]["FN"] += 1
        update_rule_id_stat(
            stats[p]["rule"],
            good_ids,
            bad_ids,
            "TP",
            "FN",
        )

    if (list(goods.keys()) == []) & (p != label):
        stats[p]["TN"] += 1        


def stat_ilp_stat_ml(goodss, labels, predss, rule_ids, out):
    tac_stats = init_stat(rule_ids)
    for goods, label, preds in zip(goodss, labels, predss):
        if utils.not_lemma(label):
            preds = preds[:20]
            for p in preds:
                stat_one_pred(p, tac_stats["tactic"], goods, label, rule_ids)
    items = tac_stats["tactic"].items()
    tac_stats["tactic"] = dict(
        sorted(items, key=lambda x: x[1]["TP"] + x[1]["FP"] + x[1]["FN"], reverse=True)
    )
    clean_stat(tac_stats["tactic"])
    tac_stats = cal_f1_precision(tac_stats)

    with open(os.path.join(out, "stat_filter.json"), "w") as w:
        json.dump(tac_stats, w)


def init_dat(f_good, f_label, f_pred, f_rule):
    labels, goodss, predss, rules = load(f_good, f_label, f_pred, f_rule)
    rule_ids = mk_rule_ids_dic(rules)
    out = os.path.dirname(f_good)
    return labels, goodss, predss, rule_ids, out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns false positive and false negative."
    )
    parser.add_argument("--good", type=str)
    parser.add_argument("--pred", type=str)
    parser.add_argument("--label", type=str)
    parser.add_argument("--rule", type=str)
    args = parser.parse_args()

    labels, goodss, predss, rule_ids, out = init_dat(
        args.good, args.label, args.pred, args.rule
    )
    stat_ilp_stat_ml(labels, goodss, predss, rule_ids, out)
