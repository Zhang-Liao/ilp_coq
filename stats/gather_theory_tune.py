import json
import os
import re
import sys

import numpy as np
import warnings


sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

precs = [0, 6, 12, 18, 24, 30]

KINDS = ["anonym_feat", "anonym_repr", "origin_repr", "origin_feat"]
POS = [1, 2, 4, 8, 16, 32]
NEG = [0, 1, 2, 4, 8, 16, 32, 64]
METRIC = 'f1'

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
    ilp_reader = open(os.path.join(root, ilp_stat_f), "r")

    file_stat = json.load(ilp_reader)
    f1 = file_stat[METRIC]
    splits = root.split("/")
    # print(splits)
    if ("anonym" in splits) & ("feat" in splits) & (not 'repr' in splits):
        stat["f1"]["anonym_feat"][theory][pos][neg][prec] = f1
    elif ("anonym" in splits) & ("repr" in splits):
        # print('anonym repr', f1)
        stat["f1"]["anonym_repr"][theory][pos][neg][prec] = f1
    elif ("origin" in splits) & ("feat" in splits) & (not 'repr' in splits):
        stat["f1"]["origin_feat"][theory][pos][neg][prec] = f1
    elif ("origin" in splits) & ("repr" in splits):
        stat["f1"]["origin_repr"][theory][pos][neg][prec] = f1
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
                if (prec in precs) & (pos in  POS) & (neg in NEG):
                    update_theory_stat(stat, f, root, theory, pos, neg, prec)


theories = ["valid/valid"]

ilp_stat = {
    "f1": init_stat(theories),
}

for theory in theories:
    knn_stat = init_knn_stat(theory)
    dirc = f"data/json/feat/tune/Structures/test_theory/{theory}"
    update_theory_stats(dirc, ilp_stat, theory)
# print(ilp_stat['f1']['anonym_repr'])

with open("tune_valid.json", "w") as w:
    json.dump(ilp_stat, w)
