import json
import os
import re
import sys

import warnings

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

THEORIES = [
    'plugins/rtauto', 
    'theories/FSets', 
    'theories/Wellfounded',
    'plugins/funind',
    'plugins/btauto',
    'plugins/nsatz',
    'theories/MSets'
]

predc_kinds = ["anonym_feat", "origin_repr", "origin_feat", "anonym_repr"]

params = {
    "anonym_feat": ["p1n32", "0"],
    "anonym_repr": ["p16n1", "0"],
    "origin_repr": ["p1n1", "0"],
    "origin_feat": ["p1n1", "0"],
}


def init_stat():
    stat = {}
    for kind in predc_kinds:
        stat[kind] = {}
        for t in THEORIES:
            stat[kind][t] = {}
    return stat


def init_knn_stat():
    stat = {}
    for t in THEORIES:
        stat[t] = {}
    return stat


def params_in_path(splits, kind):
    param = params[kind]
    return all(map(lambda x: x in splits, param))


def get_acc(stat_dir, theory):
    good_dir = os.path.dirname(stat_dir)
    theory_dir = os.path.dirname(good_dir)
    assert os.path.basename(good_dir) == "good"
    theory_name = os.path.basename(theory)
    stat_f = os.path.join(theory_dir, f"reorder/{theory_name}_stat.json")
    reader = open(stat_f, "r")
    stat = json.load(reader)
    return stat["acc"]


def update_theory_stat(stat, ilp_stat_f, root, theory):
    ilp_reader = open(os.path.join(root, ilp_stat_f), "r")

    file_stat = json.load(ilp_reader)
    f1 = file_stat["f1"]

    splits = root.split("/")
    if ("valid" in splits) & ("anonym" in splits) & ("feat" in splits) & (not 'repr' in splits):
        if params_in_path(splits, "anonym_feat"):
            stat["f1"]["anonym_feat"][theory] = f1
            stat["acc"]["anonym_feat"][theory] = get_acc(root, theory)
    elif ("valid" in splits) & ("anonym" in splits) & ("repr" in splits):
        if params_in_path(splits, "anonym_repr"):
            stat["f1"]["anonym_repr"][theory] = f1
            stat["acc"]["anonym_repr"][theory] = get_acc(root, theory)
    elif ("valid" in splits) & ("origin" in splits) & ("feat" in splits) & (not 'repr' in splits) :
        if params_in_path(splits, 'origin_feat'):
            stat["f1"]["origin_feat"][theory] = f1
            stat["acc"]["origin_feat"][theory] = get_acc(root, theory)
    elif ("valid" in splits) & ("origin" in splits) & ("repr" in splits):
        if params_in_path(splits, 'origin_repr'):
            stat["f1"]["origin_repr"][theory] = f1
            stat["acc"]["origin_repr"][theory] = get_acc(root, theory)
    else:
        warnings.warn("skip " + os.path.join(root, ilp_stat_f))


def update_theory_stats(dir, stat, theory):
    for root, _, files in os.walk(dir):
        for f in files:
            if f.endswith("stat_filter.json"):
                update_theory_stat(stat, f, root, theory)


ilp_stat = {"acc": init_stat(), "f1": init_stat()}

test_dir = "data/json/feat/tune/Structures/test_theory"
for theory in THEORIES:
    dir = os.path.join(test_dir, theory)
    update_theory_stats(dir, ilp_stat, theory)

ilp_stat = params | ilp_stat
with open("test.json", "w") as w:
    json.dump(ilp_stat, w)
