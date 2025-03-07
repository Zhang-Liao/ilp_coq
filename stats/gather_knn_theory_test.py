import json
import os
import re
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

THEORIES = [
    "plugins/rtauto",
    "theories/FSets",
    "theories/Wellfounded",
    "plugins/funind",
    "plugins/btauto",
    "plugins/nsatz",
    "theories/MSets",
]


def init_knn_stat():
    stat = {}
    for t in THEORIES:
        stat[t] = {}
    return stat


def update_knn(dir, theory, stat):
    file = os.path.join(dir, f"{theory}_stat.json")
    reader = open(file, "r")
    knn_stat = json.load(reader)
    stat[theory] = knn_stat["acc"]


knn_stat = init_knn_stat()
stat_i = f"data/json/feat/tune/Structures/test_theory/"
for theory in THEORIES:
    dir = os.path.join(stat_i, theory)
    update_knn(stat_i, theory, knn_stat)

with open("knn_theory_stat.json", "w") as w:
    json.dump(knn_stat, w)
