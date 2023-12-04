import json
import os
import sys

import argparse

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils
from stats import stat_filter


def load(f_good, f_label, f_pred):
    with open(f_label, "r") as f:
        labels = f.read().splitlines()
    labels = [l.strip() for l in labels]

    with open(f_good, "r") as f:
        goodss = f.read().splitlines()
    goodss = [json.loads(l) for l in goodss]

    with open(f_pred, "r") as f:
        predss = f.read().splitlines()
    predss = [l.strip().split("\t") for l in predss]

    assert len(goodss) == len(labels)
    return labels, goodss, predss


def init_rules(stat):
    rules = {}
    for tac in stat.keys():
        rules[tac] = set()
    return rules


def filter_rules(f_stat, precision):
    reader = open(f_stat, "r")
    stat = json.load(reader)
    good_rules = init_rules(stat["tactic"])
    for tac, tac_stat in stat["tactic"].items():
        for rule, rule_stat in tac_stat["rule"].items():
            if rule_stat["precision"] >= precision:
                good_rules[tac].add(int(rule))
    return good_rules


def filter_goods(goods, tac_ids):
    new_goods = {}
    for tac, acc_ids in goods.items():
        if tac in tac_ids.keys():
            new_acc_ids = tac_ids[tac].intersection(set(acc_ids))
            # print("tac_ids[tac]", tac_ids[tac])
            # print("set(acc_ids)", set(acc_ids))
            # exit()
            if new_acc_ids != set():
                new_goods[tac] = new_acc_ids
    return new_goods


def filter_goodss(goodss, tac_ids):
    new_goodss = []
    for goods in goodss:
        if isinstance(goods, str):
            new_goodss.append(goods)
        else:
            new_goodss.append(filter_goods(goods, tac_ids))
    # print(new_goodss[:100])
    return new_goodss


def mk_stat(stat_f, good_f, pred_f, label_f, prec):
    rules = filter_rules(stat_f, prec)
    labels, goodss, predss = load(good_f, label_f, pred_f)
    goodss = filter_goodss(goodss, rules)
    subdir = str(int(100 * prec))
    out = os.path.join(os.path.dirname(good_f), subdir)
    if not os.path.exists(out):
        os.mkdir(out)
    stat_filter.stat_ilp_stat_ml(goodss, labels, predss, rules, out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns false positive and false negative."
    )
    parser.add_argument("--stat", type=str)
    parser.add_argument("--good", type=str)
    parser.add_argument("--pred", type=str)
    parser.add_argument("--label", type=str)
    parser.add_argument("--precision", type=float)
    args = parser.parse_args()
    mk_stat(args.stat, args.good, args.pred, args.label, args.precision)
