import json

import numpy as np
import scipy.stats as stats


def conf(l):
    conf = stats.norm.interval(0.95, loc=np.mean(l, axis=0), scale=stats.sem(l))
    return conf


def init_l(k):
    l = []
    for i in range(k):
        l.append([])
    return init_l


tacs = [
    "auto",
    "intros",
    "simpl",
    "reflexivity",
    "assumption",
    "trivial",
    "intro",
    "split",
    "intuition",
    "discriminate",
    "order",
    "ring",
    "left",
    "auto with zarith",
    "right",
    "auto with sets",
    "red",
    "eauto",
    "symmetry",
    "intro H",
    "lia",
]
K = 20
tacs = tacs[:K]
init = dict(zip(tacs, [[] for _ in range(K)]))
# print(init)

prop = [
    "data/json/origin_feat/rand_train_test/test0/filter/09-11-2023-09:33:08/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test1/filter/09-11-2023-09:36:14/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test2/filter/09-11-2023-09:37:09/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test3/filter/09-11-2023-09:42:51/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test4/filter/09-11-2023-09:37:26/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test5/filter/09-11-2023-09:25:35/good/stat_filter.json",
]
rel1 = [
    "data/json/origin_feat/rand_train_test/test0/filter/09-11-2023-09:48:04/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test1/filter/09-11-2023-09:56:25/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test2/filter/09-11-2023-09:53:00/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test3/filter/09-11-2023-09:57:23/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test4/filter/09-11-2023-09:54:13/good/stat_filter.json",
    "data/json/origin_feat/rand_train_test/test5/filter/09-11-2023-09:42:22/good/stat_filter.json"
]
rel2 = []
rel3 = []


def verify():
    ()

def load_npvs(fs, npvs):
    for f in fs:
        with open(f, "r") as r:
            stat = json.load(r)
            for t in tacs:
                npvs[t].append(stat[t]["npv"])
    return npvs


prop_dct = load_npvs(prop, init.copy())

for tac, npv in prop_dct.items():
    prop_dct[tac] = conf(npv)


rel1_dct = load_npvs(rel1, init.copy())

for tac, npv in rel1_dct.items():
    rel1_dct[tac] = conf(npv)

print(prop_dct)
print(rel1_dct)
