import json
import os
import re
import sys

import stat_filter

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

num_of_test = 1
predc_kinds = ["anonym_rel", "origin_prop", "origin_rel"]


def update_theory_stats(dir, pred, label, theory):
    name = theory.split("/")[-1]
    for root, _, _ in os.walk(dir):
        good_stat = os.path.join(root, f"good/{name}_stat.json")
        # print(good_stat)
        if os.path.exists(good_stat):
            print("stat", good_stat)
            reorder = os.path.join(root, f"reorder/{name}.eval")
            good = os.path.join(root, f"good/{name}.eval")
            stat_filter.stat_ilp_stat_ml(good, label, pred, reorder, False)
        # for f in files:
        #     if f.endswith("stat_filter.json"):
        #         update_theory_stat(i, stat["f1"], f, root, theory)


merge_dir = "data/json/origin_feat/merge"
for i in range(num_of_test):
    # stat_i = f"data/json/origin_feat/tune/MSets/test_theory/train{i}"
    stat_i = f"data/json/origin_feat/tune/QArith/test_theory/"
    # for theory in utils.THEORIES:
    for theory in ["theories/Lists"]:
        pred = os.path.join(merge_dir, theory + ".eval")
        label = os.path.join(merge_dir, theory + ".label")
        dir = os.path.join(stat_i, theory)
        update_theory_stats(dir, pred, label, theory)
