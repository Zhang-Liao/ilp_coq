import json
import os
import re
import sys

import numpy as np
import warnings


sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

num_of_test = 10
precs = [0, 0.05, 0.10, 0.15, 0.2]
KINDS = ["anonym_rel", "anonym_prop", "origin_prop", "origin_rel"]
POS = [2, 4, 8, 16, 32]
NEG = [1, 2, 4, 8, 16, 32]


def init_stat(theories):
    stat = {}
    for kind in KINDS:
        stat[kind] = {}
        for theory in theories:
            stat[kind][theory] = {}
            for p in POS:
                stat[kind][theory][p] = {}
                for n in NEG:
                    stat[kind][theory][p][n] = {}
                    for prec in precs:
                        prec = int(prec * 100)
                        stat[kind][theory][p][n][prec] = {}
    return stat


def init_aver_f1():
    stat = {}
    for kind in KINDS:
        stat[kind] = {}
        for p in POS:
            stat[kind][p] = {}
            for n in NEG:
                stat[kind][p][n] = []
    return stat


def init_knn_stat(theory):
    stat = {}
    stat[theory] = {}
    return stat


def are_elements_nearby(lst, elem1, elem2):
    for i in range(len(lst) - 1):
        if lst[i] == elem1 and lst[i + 1] == elem2:
            return True
    return False


def good_prec(splits, prec):
    if prec == 0:
        return splits[-1] == "good"
    else:
        return str(int(100 * prec)) in splits


def update_theory_stat(stat, ilp_stat_f, root, theory, pos, neg, prec):
    theory_name = theory.split("/")[-1]
    path_splits = root.split("/")
    test_dir = "/".join(path_splits[:-1])
    reorder_f = os.path.join(test_dir, f"reorder/{theory_name}_stat.json")
    ilp_reader = open(os.path.join(root, ilp_stat_f), "r")

    file_stat = json.load(ilp_reader)
    # reorder_stat = json.load(reorder_reader)
    f1 = file_stat["f1"]
    f1_no_ign = file_stat["f1_no_ignored_tac"]
    # acc = reorder_stat["accs"]
    # print(f1)
    splits = root.split("/")
    if ("anonym_id" in splits) & ("rel" in splits):
        stat["f1"]["anonym_rel"][theory][pos][neg][prec] = f1
        stat["f1_no_ignored_tac"]["anonym_rel"][theory][pos][neg][prec] = f1_no_ign
        # stat["acc"]["anonym_rel"][theory][pos][neg] = acc
    elif ("anonym_noarity" in splits) & ("prop" in splits):
        stat["f1"]["anonym_prop"][theory][pos][neg][prec] = f1
        stat["f1_no_ignored_tac"]["anonym_prop"][theory][pos][neg][prec] = f1_no_ign
        # stat["acc"]["anonym_prop"][theory][pos][neg] = acc
    elif ("origin" in splits) & ("rel" in splits):
        stat["f1"]["origin_rel"][theory][pos][neg][prec] = f1
        stat["f1_no_ignored_tac"]["origin_rel"][theory][pos][neg][prec] = f1_no_ign
        # stat["acc"]["origin_rel"][theory][pos][neg] = acc
    elif ("origin" in splits) & ("prop" in splits):
        stat["f1"]["origin_prop"][theory][pos][neg][prec] = f1
        stat["f1_no_ignored_tac"]["origin_prop"][theory][pos][neg][prec] = f1_no_ign
        # stat["acc"]["origin_prop"][theory][pos][neg] = acc
    else:
        warnings.warn("skip " + os.path.join(root, ilp_stat_f))


def update_theory_stats(dir, stat, theory):
    for root, _, files in os.walk(dir):
        for f in files:
            path = os.path.join(root, f)
            info = re.match(
                r".*p(?P<pos>[0-9]+)n(?P<neg>[0-9]+).*/good/(?P<prec>[0-9]+)/stat_filter.json",
                path,
            )
            if info != None:
                info = info.groupdict()
                pos = int(info["pos"])
                neg = int(info["neg"])
                prec = int(info["prec"])
                update_theory_stat(stat, f, root, theory, pos, neg, prec)


def update_knn(dir, theory, stat):
    file = os.path.join(dir, f"{theory}_stat.json")
    reader = open(file, "r")
    knn_stat = json.load(reader)
    stat[theory] = knn_stat["accs"]


def cal_aver_f1(stat, key):
    aver_f1 = init_aver_f1()
    for kind, kind_stat in stat[key].items():
        for theory_stat in kind_stat.values():
            for pos, pos_stat in theory_stat.items():
                for neg, f1 in pos_stat.items():
                    aver_f1[kind][pos][neg].append(f1)

    for kind, kind_stat in aver_f1.items():
        for pos, pos_stat in kind_stat.items():
            for neg, f1s in pos_stat.items():
                aver_f1[kind][pos][neg] = np.average(f1s)

    for kind in stat[key].keys():
        stat[key][kind]["aver"] = aver_f1[kind]


theories = ["theories/Lists"]
# theories = ["plugins/setoid_ring"]
# theories = ["theories/Init"]

ilp_stat = {
    # "acc": init_stat(theories),
    "f1": init_stat(theories),
    "f1_no_ignored_tac": init_stat(theories),
}
# print(ilp_stat)
for theory in theories:
    knn_stat = init_knn_stat(theory)
    dir = f"data/json/origin_feat/tune/QArith/test_theory/{theory}"
    # dir = os.path.join(stat_i, theory)
    # update_knn(dir, theory, knn_stat)
    update_theory_stats(dir, ilp_stat, theory)


# cal_aver_f1(ilp_stat, "f1")
# cal_aver_f1(ilp_stat, "f1_no_ignored_tac")

with open("QArith_tune_debug.json", "w") as w:
    json.dump(ilp_stat, w)

# with open("knn_List.json", "w") as w:
#     json.dump(knn_stat, w)
