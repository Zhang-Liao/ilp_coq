import json
import os
import re
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


def mk_rule_dic(file):
    reader = open(file, "r")
    dic = {}
    for r in reader:
        if r == ":- style_check(-singleton).\n":
            continue
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
                dic[tac] = {}

        if r.endswith("."):
            dic[tac][i] = r
    return dic


def init_rules(stat):
    rules = {}
    for tac in stat.keys():
        rules[tac] = set()
    return rules


def pr_rules(file, rule_dic):
    with open(file, "w") as w:
        w.write(":- style_check(-singleton).\n")
        for tac, tac_rules in rule_dic.items():
            for i, rule in tac_rules.items():
                # for i in range(len(rules)):
                w.write(f'tac(A,"{tac}",{i}) :-\n')
                w.write(f"    {rule}\n")


def keep_good_rules(rule_dic, good_ids):
    good_rules = {}
    for tac, tac_rules in rule_dic.items():
        for i, rule in tac_rules.items():
            if tac in good_ids.keys():
                if i in good_ids[tac]:
                    if tac not in good_rules.keys():
                        good_rules[tac] = {}
                    good_rules[tac][i] = rule
    return good_rules


def filter_rules(stat_f, precision, rule_dic):
    reader = open(stat_f, "r")
    stat = json.load(reader)
    good_ids = init_rules(stat["tactic"])
    for tac, tac_stat in stat["tactic"].items():
        for rule, rule_stat in tac_stat["rule"].items():
            if rule_stat["precision"] >= precision:
                good_ids[tac].add(int(rule))
    good_rules = keep_good_rules(rule_dic, good_ids)
    return good_ids, good_rules


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


def mk_stat(stat_f, good_f, pred_f, label_f, prec, rule_f):
    rule_dic = mk_rule_dic(rule_f)
    rule_ids, rules = filter_rules(stat_f, prec, rule_dic)
    labels, goodss, predss = load(good_f, label_f, pred_f)
    goodss = filter_goodss(goodss, rule_ids)
    subdir = str(int(100 * prec))
    out = os.path.join(os.path.dirname(good_f), subdir)
    if not os.path.exists(out):
        os.mkdir(out)
    stat_filter.stat_ilp_stat_ml(goodss, labels, predss, rule_ids, out)
    pr_rules(os.path.join(out, "alltac_rule.pl"), rules)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns false positive and false negative."
    )
    parser.add_argument("--stat", type=str)
    parser.add_argument("--good", type=str)
    parser.add_argument("--pred", type=str)
    parser.add_argument("--label", type=str)
    parser.add_argument("--precision", type=float)
    parser.add_argument("--rule", type=str)
    args = parser.parse_args()
    mk_stat(args.stat, args.good, args.pred, args.label, args.precision, args.rule)
