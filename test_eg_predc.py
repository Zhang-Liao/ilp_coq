"""
Generate a file for every proof state to reduce the number of goal_predc and
hyp_predc used in eq_subterm.
"""

import json
import os

import argparse

from lib import utils


def init_out(i, out_dir):
    out = os.path.join(out_dir, f"{i}.pl")
    if os.path.exists(out):
        os.remove(out)
    return out


def pr_predc(row_i, l, w, kind):
    if kind in ["prop", "rel"]:
        utils.pr_goal_predc(row_i, l["goal"], w)
        utils.pr_hyps_predc(row_i, l["hyps"], w)
    elif kind == "anonym":
        utils.pr_goal_anonym_predc(row_i, l["goal"], w)
        utils.pr_hyps_anonym_predc(row_i, l["hyps"], w)


parser = argparse.ArgumentParser()
parser.add_argument("--test", type=str)
parser.add_argument("--out", type=str)
parser.add_argument("--kind", type=str, choices=["prop", "anonym"])

opts = parser.parse_args()

if not os.path.exists(opts.out):
    os.makedirs(opts.out)

with open(opts.test, "r") as r:
    row_i = 0
    for l in r:
        l = l.strip()
        if utils.not_lemma(l):
            l = json.loads(l)
            out = init_out(row_i, opts.out)
            with open(out, "a") as w:
                w.write(":-style_check(-discontiguous).\n")
                pr_predc(row_i, l, w, opts.kind)
        row_i += 1
