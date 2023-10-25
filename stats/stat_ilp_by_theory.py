import json
import os
import re
import sys

import stat_filter

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


def update_theory_stat(i, all_stat, file, root, theory):
    reader = open(os.path.join(root, file), "r")
    stat = json.load(reader)
    f1 = stat["f1"]
    f1_no_ign = stat["f1_no_ignored_tac"]

    splits = root.split("/")
    if ("anonym" in splits) & ("rel" in splits):
        all_stat["f1"]["anonym_rel"][theory][i] = f1
        all_stat["f1_no_ignored_tac"]["anonym_rel"][theory][i] = f1_no_ign
    elif ("origin" in splits) & ("rel" in splits):
        all_stat["f1"]["origin_rel"][theory][i] = f1
        all_stat["f1_no_ignored_tac"]["origin_rel"][theory][i] = f1_no_ign
    elif ("origin" in splits) & ("prop" in splits):
        all_stat["f1"]["origin_prop"][theory][i] = f1
        all_stat["f1_no_ignored_tac"]["origin_prop"][theory][i] = f1_no_ign

    else:
        raise FileNotFoundError("stat_filter exist in unexpected path")


def update_theory_stats(dir, i, pred, label, theory):
    name = theory.split("/")[-1]
    for root, _, _ in os.walk(dir):
        good_stat = os.path.join(root, f"good/{name}_stat.json")
        print(good_stat)
        if os.path.exists(good_stat):
            print("exist")
            reorder = os.path.join(root, f"reorder/{name}.eval")
            good = os.path.join(root, f"good/{name}.eval")
            stat_filter.stat_ilp_stat_ml(good, label, pred, reorder, False)
        # for f in files:
        #     if f.endswith("stat_filter.json"):
        #         update_theory_stat(i, stat["f1"], f, root, theory)


stat = {"acc": init_stat(), "f1": init_stat()}
merge_dir = "data/json/origin_feat/merge"
for i in range(num_of_test):
    stat_i = f"data/json/origin_feat/tune/MSets/test_theory/train{i}"
    for theory in utils.THEORIES:
        pred = os.path.join(merge_dir, theory + ".eval")
        label = os.path.join(merge_dir, theory + ".label")
        dir = os.path.join(stat_i, theory)
        update_theory_stats(dir, i, pred, label, theory)
