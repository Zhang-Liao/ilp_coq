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
        for t in utils.THEORIES:
            stat[kind][t] = {}
    return stat


def check_miss(stats):
    for pos in stats.keys():
        for neg in stats[pos].keys():
            for split, st in stats[pos][neg].items():
                if st == []:
                    print("miss: pos", pos, "neg", neg, "split", split)


def update_stat(i, stat, file, root, theory):
    reader = open(os.path.join(root, file), "r")
    file_stat = json.load(reader)
    f1 = file_stat["f1"]
    f1_no_ign = file_stat["f1_no_ignored_tac"]
    # print(f1)
    splits = root.split("/")
    if ("anonym" in splits) & ("rel" in splits):
        try:
            stat["f1"]["anonym_rel"][theory][i] = f1
            stat["f1_no_ignored_tac"]["anonym_rel"][theory][i] = f1_no_ign
        except:
            print("fail in", os.path.join(root, file))
            exit()
    elif ("origin" in splits) & ("rel" in splits):
        stat["f1"]["origin_rel"][theory][i] = f1
        stat["f1_no_ignored_tac"]["origin_rel"][theory][i] = f1_no_ign
    elif ("origin" in splits) & ("prop" in splits):
        stat["f1"]["origin_prop"][theory][i] = f1
        stat["f1_no_ignored_tac"]["origin_prop"][theory][i] = f1_no_ign
    else:
        raise FileNotFoundError("stat_filter exist in unexpected path")


def update_stats(dir, i, stat):
    for root, _, files in os.walk(dir):
        for f in files:
            if f.endswith("stat_filter.json"):
                f1 = update_stat(i, stat, f, root, theory)


stat = {"acc": init_stat(), "f1": init_stat(), "f1_no_ignored_tac": init_stat()}
for i in range(num_of_test):
    dir = f"data/json/origin_feat/rand_lines/valid{i}"
    update_stats(dir, i, stat)

# check_miss(stat)
with open("split_test_stat.json", "w") as w:
    json.dump(stat, w)
# print(stat)
