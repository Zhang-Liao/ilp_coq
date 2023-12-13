import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

consts = [
    "Coq.Init.Logic.False",
    "Coq.Init.Logic.True",
    "Coq.Init.Logic.and",
    "Coq.Init.Logic.iff",
    "Coq.Init.Logic.or",
    "Coq.Init.Logic.not",
    "Coq.Init.Logic.eq",
    "Coq.Init.Datatypes.true",
    "Coq.Init.Datatypes.false",
    "Coq.Init.Datatypes.andb",
    "Coq.Init.Datatypes.orb",
    "Coq.Init.Datatypes.implb",
    "Coq.Init.Datatypes.negb",
    "Coq.Init.Datatypes.xorb",
]

dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/predicate/anonym"
out = "/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/basic_const.json"
dic = dict(zip(consts, len(consts) * [0]))

dat = utils.load_dataset_no_lemma(dir)
for _, l in dat:
    l = json.loads(l)
    for prec in l["hyps"]:
        id = prec[1]
        if id in consts:
            dic[id] += 1
    for prec in l["goal"]:
        id = prec[1]
        if id in consts:
            dic[id] += 1

dic = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
# print(dic)
with open(out, "w") as w:
    json.dump(dic, w, indent=4)
