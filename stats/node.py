import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/predicate/origin"
num = 0
dat = utils.load_dataset_no_lemma(dir)
for _, l in dat:
    l = json.loads(l)
    num += len(l["hyps"])
    num += len(l["goal"])

print(num)