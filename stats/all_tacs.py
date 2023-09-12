import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

labels = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split'
out = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/all_tac.json'

tacs = {}
for i in range(10):
    file = os.path.join(labels, f'split{i}.label')
    with open(file, 'r') as r :
        for t in r:
            if utils.not_lemma(t):
                t = t.strip()
                if t not in tacs.keys():
                    tacs[t] = 0
                else:
                    tacs[t] += 1
    # print(tacs)

tacs = dict(sorted(tacs.items(), key = lambda x : x[1], reverse = True))

with open(out, 'w') as w:
    json.dump(tacs, w, indent=4)