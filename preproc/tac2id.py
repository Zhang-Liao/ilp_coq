import os

from lib import utils

import json

def build(dir):
    tacs = set()
    for root, _, _ in os.walk(dir):
        for i in range(10):
            f = os.path.join(root, 'split'+str(i)+'.json')
            with open(f, 'r') as reader:
                for l in reader:
                    l = l.strip()
                    if utils.not_lemma(l):
                        l = json.loads(l)
                        tacs.add(utils.safe_tac(l['tac']))
        break
    ids = list(range(0, len(tacs)))
    tacs = sorted(list(tacs))
    tac_ids = zip(list(tacs), ids)
    return dict(tac_ids)
    # print(tac_map)

dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split'
tac_dict = build(dir)
w = open(os.path.join(dir, 'tac2id.json'), 'w') 
json.dump(tac_dict, w)