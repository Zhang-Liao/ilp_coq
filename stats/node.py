import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/predicate/origin"
num = 0
predc = set()
dat = utils.load_dataset_no_lemma(dir)
for _, l in dat:
    l = json.loads(l)
    num += len(l["hyps"])
    num += len(l["goal"])
    for p in l["hyps"]:
        predc.add('hyps' + p[0])
    for p in l["goal"]:
        predc.add('goal' + p[0])

print('len(predc)', len(predc))
print('node number', num)