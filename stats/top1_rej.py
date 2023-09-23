import json
import os
import sys


sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def count_rej(preds, tac):
    rej = []
    for p in preds:
        if p == tac:
            break
        else:
            rej.append(p)
    return rej


def count_train_label(f):
    train_label = {}
    with open(f, "r") as r:
        for tac in r:
            if utils.not_lemma(tac):
                tac = tac.strip()
                if tac not in train_label.keys():
                    train_label[tac] = 1
                else:
                    train_label[tac] += 1
    return train_label


f_filter_stat2 = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test2/filter/09-11-2023-09:53:00/good/stat_filter.json"
f_filter_stat1 = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test2/filter/09-17-2023-15:27:19/good/stat_filter.json"
tac = "simpl"
f_pred = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test2.eval"
f_train_label = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/train2.label"

rej_stat = {"tac": tac, "filter1": f_filter_stat1, "filter2": f_filter_stat2}
out = f"stats/log/{tac}_rej_rev.json"

with open(f_filter_stat1, "r") as r:
    filter_stat1 = json.load(r)

with open(f_filter_stat2, "r") as r:
    filter_stat2 = json.load(r)

with open(f_pred, "r") as r:
    preds1 = r.readlines()
    preds1 = [l.strip().split("\t") for l in preds1]


tac_stat1 = filter_stat1[tac]["top1"]["id"]
tac_stat2 = filter_stat2[tac]["top1"]["id"]

for id in tac_stat1:
    if id not in tac_stat2:
        pred1 = preds1[id]
        rej_stat[id] = count_rej(pred1, tac)

train_label = count_train_label(f_train_label)
occuer = 0
rej_tacs = 0
for id, rejs in rej_stat.items():
    if id not in ["tac", "filter1", "filter2"]:
        for rej in rejs:
            occuer += train_label[rej]
            rej_tacs += 1
occuer = occuer / rej_tacs

rej_stat["avg_rej_occ"] = occuer

with open(out, "w") as w:
    json.dump(rej_stat, w)
