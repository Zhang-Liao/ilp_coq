import json
import os

import argparse

from lib import utils

def init_out(i, out_dir):
    out = os.path.join(out_dir, f'{i}.pl')
    if os.path.exists(out):
        os.remove(out)
    return out

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=str)
parser.add_argument("--out", type=str)
opts = parser.parse_args()

if not os.path.exists(opts.out):
    os.makedirs(opts.out)

with open(opts.test, 'r') as r:
    row_i = 0
    for l in r:
        l = l.strip()
        if utils.not_lemma(l):
            l = json.loads(l)
            out = init_out(row_i, opts.out)
            with open(out, 'a') as w:
                w.write(':-style_check(-discontiguous).\n')
                utils.pr_goal_predc(row_i, l['goal'], w)
                goal_predc = utils.add_goal_predc(l['goal'], set())
                utils.pr_hyps_predc(row_i, l['hyps'], w)
                hyp_predc = utils.add_hyps_predc(l['hyps'], set())
                for p in goal_predc:
                    w.write(f"goal_predc({p}).\n")
                for p in hyp_predc:
                    w.write(f"hyp_predc({p}).\n")
            
        row_i += 1

