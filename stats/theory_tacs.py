import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def stat_theory(theory):
    tacs = {}
    for root, _, files in os.walk(theory):
        for f in files:
            if f.endswith(".json"):
                r = open(os.path.join(root, f), "r")
                dat = r.readlines()
                for l in dat:
                    if utils.not_lemma(l):
                        t = json.loads(l)["tac"]
                        if t not in tacs.keys():
                            tacs[t] = 0
                        else:
                            tacs[t] += 1
    tacs = sorted(tacs.items(), key=lambda x: x[1], reverse=True)[:30]
    # tacs = list(tacs.items())[:30]
    # print(tacs)
    return dict(tacs)


dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg"
out = "/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/theory_tac.json"


tacs = {}
theories = utils.THEORIES + ["theories/MSets"]
for theory in theories:
    curr_dir = os.path.join(dir, theory)
    # tacs[theory] = {}
    tacs[theory] = stat_theory(curr_dir)

# print(tacs)

# tacs = dict(sorted(tacs.items(), key=lambda x: x[1], reverse=True))

with open(out, "w") as w:
    json.dump(tacs, w, indent=4)
