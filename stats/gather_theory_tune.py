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


def init_stat(theory):
    stat = {}
    pos = [2, 4, 8, 16, 32]
    neg = [1, 2, 4, 8, 16, 32]
    for kind in predc_kinds:
        stat[kind] = {}
        stat[kind][theory] = {}
        for p in pos:
            stat[kind][theory][p] = {}
            for n in neg:
                stat[kind][theory][p][n] = {}
    return stat


def init_knn_stat(theory):
    stat = {}
    stat[theory] = {}
    return stat


def update_theory_stat(stat, ilp_stat_f, root, theory, pos, neg):
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
        stat["f1"]["anonym_rel"][theory][pos][neg] = f1
        stat["f1_no_ignored_tac"]["anonym_rel"][theory][pos][neg] = f1_no_ign
        # stat["acc"]["anonym_rel"][theory][pos][neg] = acc
    elif ("origin" in splits) & ("rel" in splits):
        stat["f1"]["origin_rel"][theory][pos][neg] = f1
        stat["f1_no_ignored_tac"]["origin_rel"][theory][pos][neg] = f1_no_ign
        # stat["acc"]["origin_rel"][theory][pos][neg] = acc

    elif ("origin" in splits) & ("prop" in splits):
        stat["f1"]["origin_prop"][theory][pos][neg] = f1
        stat["f1_no_ignored_tac"]["origin_prop"][theory][pos][neg] = f1_no_ign
        # stat["acc"]["origin_prop"][theory][pos][neg] = acc
    else:
        raise FileNotFoundError("stat_filter exist in unexpected path")


def update_theory_stats(dir, stat, theory):
    for root, _, files in os.walk(dir):
        for f in files:
            path = os.path.join(root, f)
            info = re.match(
                r".*p(?P<pos>[0-9]+)n(?P<neg>[0-9]+).*/stat_filter.json", path
            )
            if info != None:
                info = info.groupdict()
                pos = int(info["pos"])
                neg = int(info["neg"])
                # if f.endswith("stat_filter.json"):
                update_theory_stat(stat, f, root, theory, pos, neg)


def update_knn(dir, theory, stat):
    file = os.path.join(dir, f"{theory}_stat.json")
    reader = open(file, "r")
    knn_stat = json.load(reader)
    stat[theory] = knn_stat["accs"]


theory = "theories/Lists"
ilp_stat = {
    "acc": init_stat(theory),
    "f1": init_stat(theory),
    "f1_no_ignored_tac": init_stat(theory),
}
knn_stat = init_knn_stat(theory)
dir = f"data/json/origin_feat/tune/QArith/test_theory/{theory}"
# dir = os.path.join(stat_i, theory)
# update_knn(dir, theory, knn_stat)
update_theory_stats(dir, ilp_stat, theory)

with open("List_stat_no_split.json", "w") as w:
    json.dump(ilp_stat, w)

# with open("knn_List.json", "w") as w:
#     json.dump(knn_stat, w)
