import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

import json

label_file = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/1000.label"
neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/1000_neg.json'

def exg_row_ids_map():
    mp = []
    with open(label_file, 'r') as reader:
        row_id = 0
        for l in reader:
            l = l.strip()
            if utils.not_lemma(l):
                mp.append(row_id)
            row_id += 1
    return mp

def map_exg_row_ids(dict, mp):
    new_dict = {}
    for tac, poss in dict.items():
        new_poss = []
        for pos in poss:
            new_poss.append({
                'pos' : mp[pos['pos'][0]],
                'neg' : [mp[n] for n in pos['neg']]})
        new_dict[tac] = new_poss
    return new_dict


with open(neg_file, 'r') as r:
    dict = json.load(r)

mp = exg_row_ids_map()
dict = map_exg_row_ids(dict, mp)
out = "new_neg.json"
with open(out, 'w') as w:
    json.dump(dict, w)
