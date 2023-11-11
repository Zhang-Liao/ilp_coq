import json
import os
import re
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

num_of_test = 10
# test_dir = "data/json/origin_feat/tune/MSets/"
# param = ""
# anonym = "origin"
# predc_kind = ""
# assert anonym in ["origin", "anonym"]
predc_kinds = ["anonym_rel", "origin_prop", "origin_rel"]


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


def update_theory_stat(i, stat, ilp_stat_f, root, theory):
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
    if ("anonym" in splits) & ("rel" in splits):
        stat["f1"]["anonym_rel"][theory][i] = f1
        stat["f1_no_ignored_tac"]["anonym_rel"][theory][i] = f1_no_ign
        stat["acc"]["anonym_rel"][theory][i] = acc
    elif ("origin" in splits) & ("rel" in splits):
        stat["f1"]["origin_rel"][theory][i] = f1
        stat["f1_no_ignored_tac"]["origin_rel"][theory][i] = f1_no_ign
        stat["acc"]["origin_rel"][theory][i] = acc

    elif ("origin" in splits) & ("prop" in splits):
        stat["f1"]["origin_prop"][theory][i] = f1
        stat["f1_no_ignored_tac"]["origin_prop"][theory][i] = f1_no_ign
        stat["acc"]["origin_prop"][theory][i] = acc
    else:
        raise FileNotFoundError("stat_filter exist in unexpected path")


def update_theory_stats(dir, i, stat, theory):
    for root, _, files in os.walk(dir):
        for f in files:
            if f.endswith("stat_filter.json"):
                update_theory_stat(i, stat, f, root, theory)


def update_knn(dir, theory, stat):
    file = os.path.join(dir, f"{theory}_stat.json")
    reader = open(file, "r")
    knn_stat = json.load(reader)
    stat[theory][i] = knn_stat["accs"]


ilp_stat = {"acc": init_stat(), "f1": init_stat(), "f1_no_ignored_tac": init_stat()}

knn_stat = init_knn_stat()
for i in range(num_of_test):
    stat_i = f"data/json/origin_feat/tune/QArith/test_theory/train{i}"
    for theory in utils.THEORIES:
        dir = os.path.join(stat_i, theory)
        update_knn(stat_i, theory, knn_stat)
        update_theory_stats(dir, i, ilp_stat, theory)

with open("theory_stat.json", "w") as w:
    json.dump(ilp_stat, w)

with open("knn_theory_stat.json", "w") as w:
    json.dump(knn_stat, w)
