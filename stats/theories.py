import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def dat_line(l):
    return utils.not_lemma(l) & (l.strip() != "")


theories = [
    "data/json/origin_feat/merge/theories/Classes.json",
    "data/json/origin_feat/merge/plugins/ssr.json",
    "data/json/origin_feat/merge/theories/Lists.json",
    "data/json/origin_feat/merge/theories/QArith.json",
    "data/json/origin_feat/merge/theories/Numbers.json",
    # "data/json/origin_feat/merge/plugins/funind.json",
    # "data/json/origin_feat/merge/theories/Program.json",
    # "data/json/origin_feat/merge/plugins/rtauto.json",
    # "data/json/origin_feat/merge/theories/Strings.json",
    # "data/json/origin_feat/merge/plugins/omega.json",
]

stat = {}
total = 0
for theory in theories:
    f = open(theory, "r")
    dat = f.readlines()
    dat = [l for l in dat if dat_line(l)]
    num = len(dat)
    stat[theory] = num
    total += num
print(json.dumps(stat, indent=4))
print("total", total)
