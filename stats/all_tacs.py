import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/merge"
out = "/home/zhangliao/ilp_out_coq/ilp_out_coq/ortho_tac.json"
subdirs = [os.path.join(dir, 'theories'), os.path.join(dir, 'plugins')]
tacs = {}
for subdir in subdirs:
    for file in os.listdir(subdir):
        if file.endswith(".json"):        
            r = open(os.path.join(dir, subdir, file), "r")
            dat = r.readlines()
            for l in dat:
                if utils.not_lemma(l):
                    t = json.loads(l)["tac"]
                    if t not in tacs.keys():
                        tacs[t] = 1
                    else:
                        tacs[t] += 1
tacs = dict(sorted(tacs.items(), key=lambda x: x[1], reverse=True))

with open(out, "w") as w:
    json.dump(tacs, w)