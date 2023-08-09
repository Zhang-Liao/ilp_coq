import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting
import json
from sklearn.neighbors import KNeighborsClassifier

dat_file = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/five_pos_neg/dat.json"

dummy_tac = 'keep the idx the same before removing #lemma'

def row_negs(dat, i, tac):
    # print(len(dat))
    n = 10
    negs = []
    n_row = len(dat)
    before = i - 1
    after = i + 1
    while (len(negs) < n) & ((before >= 0) | (after < n_row)):
        if before >= 0:
            if dat[before]['tac'] != tac:
                negs.append(before)
        if after < n_row:
            if (dat[after]['tac'] != tac):
                negs.append(after)
        before = before - 1
        after = after + 1
    return negs

def read():
    dat = []
    with open(dat_file, 'r') as r:
        content = r.readlines()
        for l in content:
            l = l.strip()
            if global_setting.lemma_delimiter not in l:
                dat.append(json.loads(l))
            else:
                dat.append({'tac' : dummy_tac})
    return dat

def rows_negs(dat):
    negs_dict = {}
    i = 0
    for r in dat:
        tac = r['tac']
        if tac != dummy_tac:
            negs = row_negs(dat, i, tac)
            if tac not in negs_dict.keys():
                negs_dict[tac] = [{'pos':[i], 'neg':negs}]
            else:
                negs_dict[tac].append({'pos':[i], 'neg':negs})
        i = i + 1
    return negs_dict

dat = read()
negs = rows_negs(dat)
dir = os.path.dirname(dat_file)
out = os.path.join(dir, "file_dist_neg.json")
with open(out, 'w') as w:
    json.dump(negs, w)