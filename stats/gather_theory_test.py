import json
import os
import re
import sys

import warnings

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

# THEORIES = ["theories/NArith", "theories/Arith", "theories/Sets", "theories/MSets"]

num_of_test = 10
predc_kinds = ["anonym_rel", "origin_prop", "origin_rel", "anonym_prop"]
params = {
    "anonym_rel": "p16n16",
    "anonym_prop": "p4n2",
    "origin_prop": "p4n32",
    "origin_rel": "p16n16",
}


def init_stat():
    stat = {}
    for kind in predc_kinds:
        stat[kind] = {}
        for t in utils.THEORIES:
            stat[kind][t] = {}
    return stat


def init_knn_stat():
    stat = {}
    for t in utils.THEORIES:
        stat[t] = {}
    return stat


def update_theory_stat(stat, ilp_stat_f, root, theory):
    theory_name = theory.split("/")[-1]
    path_splits = root.split("/")
    test_dir = "/".join(path_splits[:-1])
    reorder_f = os.path.join(test_dir, f"reorder/{theory_name}_stat.json")
    ilp_reader = open(os.path.join(root, ilp_stat_f), "r")
    reorder_reader = open(reorder_f, "r")

    file_stat = json.load(ilp_reader)
    reorder_stat = json.load(reorder_reader)
    f1 = file_stat["f1"]
    f1_no_ign = file_stat["f1_no_ignored_tac"]
    acc = reorder_stat["accs"]
    # print(f1)
    splits = root.split("/")
    if ("anonym_noarity" in splits) & ("rel20" in splits):
        if params["anonym_rel"] in splits:
            stat["f1"]["anonym_rel"][theory] = f1
            stat["f1_no_ignored_tac"]["anonym_rel"][theory] = f1_no_ign
            stat["acc"]["anonym_rel"][theory] = acc
    elif ("anonym_noarity" in splits) & ("prop" in splits):
        if params["anonym_prop"] in splits:
            stat["f1"]["anonym_prop"][theory] = f1
            stat["f1_no_ignored_tac"]["anonym_prop"][theory] = f1_no_ign
            stat["acc"]["anonym_prop"][theory] = acc
    elif ("origin" in splits) & ("rel20" in splits):
        if params["origin_rel"] in splits:
            stat["f1"]["origin_rel"][theory] = f1
            stat["f1_no_ignored_tac"]["origin_rel"][theory] = f1_no_ign
            stat["acc"]["origin_rel"][theory] = acc
    elif ("origin" in splits) & ("prop" in splits):
        if params["origin_prop"] in splits:
            stat["f1"]["origin_prop"][theory] = f1
            stat["f1_no_ignored_tac"]["origin_prop"][theory] = f1_no_ign
            stat["acc"]["origin_prop"][theory] = acc
    else:
        warnings.warn("skip " + os.path.join(root, ilp_stat_f))


def update_theory_stats(dir, stat, theory):
    for root, _, files in os.walk(dir):
        for f in files:
            if f.endswith("stat_filter.json"):
                update_theory_stat(stat, f, root, theory)


def update_knn(dir, theory, stat):
    file = os.path.join(dir, f"{theory}_stat.json")
    reader = open(file, "r")
    knn_stat = json.load(reader)
    stat[theory] = knn_stat["accs"]


ilp_stat = {"acc": init_stat(), "f1": init_stat(), "f1_no_ignored_tac": init_stat()}
info = {"info": "mode 20"}

knn_stat = init_knn_stat()
test_dir = f"data/json/origin_feat/tune/QArith/test_theory/"
for theory in utils.THEORIES:
    dir = os.path.join(test_dir, theory)
    update_knn(test_dir, theory, knn_stat)
    update_theory_stats(dir, ilp_stat, theory)

ilp_stat = info | params | ilp_stat
with open("QArith_noarity_test.json", "w") as w:
    json.dump(ilp_stat, w)

# with open("knn_theory_stat.json", "w") as w:
#     json.dump(knn_stat, w)
