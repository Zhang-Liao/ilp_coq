import json
import os

import argparse

from lib import utils

def init_out(i, out_dir):
    out = os.path.join(out_dir, f'{i}.pl')
    if os.path.exists(out):
        os.remove(out)
    return out

def pr_predc(row_i, l, w, kind):
    if kind == 'prop':
        utils.pr_goal_prop_predc(row_i, l['goal'], w)
        goal_predc = utils.add_goal_prop_predc(l['goal'], set())
        utils.pr_hyps_prop_predc(row_i, l['hyps'], w)
        hyp_predc = utils.add_hyps_prop_predc(l['hyps'], set())
    elif kind == 'rel':
        utils.pr_goal_predc(row_i, l['goal'], w)
        goal_predc = utils.add_goal_predc(l['goal'], set())
        utils.pr_hyps_predc(row_i, l['hyps'], w)
        hyp_predc = utils.add_hyps_predc(l['hyps'], set())
    elif kind == 'anonym':
        utils.pr_goal_anonym_predc(row_i, l['goal'], w)
        goal_predc = utils.add_goal_anonym_predc(l['goal'], set())
        utils.pr_hyps_anonym_predc(row_i, l, w)
        hyp_predc = utils.add_hyps_anonym_predc(l, set())
    return goal_predc, hyp_predc

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=str)
parser.add_argument("--out", type=str)
parser.add_argument("--kind", action=argparse.BooleanOptionalAction)

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
                goal_predc, hyp_predc = pr_predc(row_i, l, w, opts.kind)
                for p in goal_predc:
                    w.write(f"goal_predc({p}).\n")
                for p in hyp_predc:
                    w.write(f"hyp_predc({p}).\n")
            
        row_i += 1

