import json
import os
import re
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

num_of_test = 10
predc_kinds = ["anonym_rel", "origin_prop", "origin_rel"]


def init_stat():
    stat = {}
    for kind in predc_kinds:
        stat[kind] = {}
    return stat


def update_stat(i, stat, f_stat, root):
    path_splits = root.split("/")
    test_dir = "/".join(path_splits[:-1])
    reorder_f = os.path.join(test_dir, f"reorder/valid{i}_stat.json")
    reader = open(os.path.join(root, f_stat), "r")
    ilp_stat = json.load(reader)
    f1 = ilp_stat["f1"]
    f1_no_ign = ilp_stat["f1_no_ignored_tac"]
    # ???
    reorder_reader = open(reorder_f, "r")
    reorder_stat = json.load(reorder_reader)
    acc = reorder_stat["accs"]
    splits = root.split("/")
    if ("anonym" in splits) & ("rel" in splits):
        stat["f1"]["anonym_rel"][i] = f1
        stat["f1_no_ignored_tac"]["anonym_rel"][i] = f1_no_ign
        stat["acc"]["anonym_rel"][i] = acc
    elif ("origin" in splits) & ("rel" in splits):
        stat["f1"]["origin_rel"][i] = f1
        stat["f1_no_ignored_tac"]["origin_rel"][i] = f1_no_ign
        stat["acc"]["origin_rel"][i] = acc
    elif ("origin" in splits) & ("prop" in splits):
        stat["f1"]["origin_prop"][i] = f1
        stat["f1_no_ignored_tac"]["origin_prop"][i] = f1_no_ign
        stat["acc"]["origin_prop"][i] = acc
    else:
        raise FileNotFoundError("stat_filter exist in unexpected path")


def update_stats(dir, i, stat):
    for root, _, files in os.walk(dir):
        for f in files:
            if f.endswith("stat_filter.json"):
                f1 = update_stat(i, stat, f, root)


stat = {"acc": init_stat(), "f1": init_stat(), "f1_no_ignored_tac": init_stat()}
for i in range(num_of_test):
    dir = f"data/json/origin_feat/rand_lines/valid{i}"
    update_stats(dir, i, stat)

# check_miss(stat)
with open("split_test_stat.json", "w") as w:
    json.dump(stat, w)
# print(stat)
