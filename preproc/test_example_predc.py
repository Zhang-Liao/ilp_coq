import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

from lib import utils

test = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split8.json'
out_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split8/test_predc'

def init_out(i):
    out = os.path.join(out_dir, f'{i}.pl')
    if os.path.exists(out):
        os.remove(out)
    return out

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

with open(test, 'r') as r:
    row_i = 0
    for l in r:
        l = l.strip()
        if utils.notlemma(l):
            l = json.loads(l)
            out = init_out(row_i)
            with open(out, 'a') as w:
                w.write(':-style_check(-discontiguous).\n')
                utils.pr_goal_predc(row_i, l['goal'], w)
                utils.pr_hyps_predc(row_i, l['hyps'], w)
        row_i += 1
