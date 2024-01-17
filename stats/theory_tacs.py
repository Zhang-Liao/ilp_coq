import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def stat_theory(file):
    tacs = {}
    r = open(file, "r")
    dat = r.readlines()
    size = 0
    for l in dat:
        if utils.not_lemma(l):
            t = json.loads(l)["tac"]
            if t not in tacs.keys():
                tacs[t] = 1
            else:
                tacs[t] += 1
            size += 1
    tacs = sorted(tacs.items(), key=lambda x: x[1], reverse=True)[:20]
    return dict({'size' :size, 'tacs': dict(tacs)})


dir = "data/json/ortho/feat/merge"
out = "theory_ortho_tac.json"
subdirs = [os.path.join(dir, 'theories'), os.path.join(dir, 'plugins')]
tacs = {}
for subdir in subdirs:
    for file in os.listdir(subdir):
        if file.endswith(".json"):        
            theory = os.path.basename(file)[:-5]
            path = os.path.join(subdir, file)
            tacs[theory] = stat_theory(path)

with open(out, "w") as w:
    json.dump(tacs, w, indent=4)
