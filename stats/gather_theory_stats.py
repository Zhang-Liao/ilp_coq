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


def check_miss(stats):
    for pos in stats.keys():
        for neg in stats[pos].keys():
            for split, st in stats[pos][neg].items():
                if st == []:
                    print("miss: pos", pos, "neg", neg, "split", split)


def update_theory_stat(i, f1s, file, root, theory):
    reader = open(os.path.join(root, file), "r")
    stat = json.load(reader)
    f1 = stat["f1"]
    # print(f1)
    splits = root.split("/")
    if ("anonym" in splits) & ("rel" in splits):
        f1s["anonym_rel"][theory][i] = f1
    elif ("origin" in splits) & ("rel" in splits):
        f1s["origin_rel"][theory][i] = f1
    elif ("origin" in splits) & ("prop" in splits):
        f1s["origin_prop"][theory][i] = f1
    else:
        raise FileNotFoundError("stat_filter exist in unexpected path")


def update_theory_stats(dir, i, stat, theory):
    for root, _, files in os.walk(dir):
        for f in files:
            if f.endswith("stat_filter.json"):
                f1 = update_theory_stat(i, stat["f1"], f, root, theory)


stat = {"acc": init_stat(), "f1": init_stat()}
for i in range(num_of_test):
    stat_i = f"data/json/origin_feat/tune/MSets/test_theory/train{i}"
    for theory in utils.THEORIES:
        dir = os.path.join(stat_i, theory)
        update_theory_stats(dir, i, stat, theory)

# check_miss(stat)
with open("theory_stat.json", "w") as w:
    json.dump(stat, w)
# print(stat)
