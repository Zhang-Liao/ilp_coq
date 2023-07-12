import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

import random

from lib import global_setting

random.seed(110)

pos_neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/1000_neg.json'
json_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/1000.json'
bk_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl.b'
pos_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl.f'
neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl.n'
tac = 'simpl'

def idx_str(idx):
    idx = ",".join(idx)
    idx = "[" + idx +"]"
    return idx

def name_as_prolog(n):
    if n == '$e':
        return 'evar'
    elif n == '$r':
        return 'rel'
    else:
        return n

def hyps_predc(i, l, writer, predc):
    for ident, name, idx in l:
        ident = name_as_prolog(ident)
        if ident != 'app':
            predc.add((ident, 'h'))
            writer.write("{}({},{},{}).\n".format(ident, i, name, idx_str(idx)))

def goal_predc(i, l, writer, predc):
    for ident, idx in l:
        ident = name_as_prolog(ident)
        if ident != 'app':
            predc.add((ident, 'g'))
            writer.write("{}({},{}).\n".format(ident, i, idx_str(idx)))

def pr_mode(predc, writer):
    writer.write(":- modeh(1,tac(+integer)).\n")
    for p, kind in predc:
        if kind == 'g':
            writer.write(":- modeb(5, {}(+integer, -is_list)).\n".format(p))
        elif kind == 'h':
            writer.write(":- modeb(5, {}(+integer, -string, -is_list)).\n".format(p))
        else:
            assert False
    for p, kind in predc:
        if kind == 'g':
            writer.write(":- determination(tac/1, {}/2).\n".format(p))
        elif kind == 'h':
            writer.write(":- determination(tac/1, {}/3).\n".format(p))
        else:
            assert False

def pr_bias(w):
    w.write(':- set(search, heuristic).\n')
    w.write(':- set(construct_bottom, false).\n')

def pr_bk(pos_neg, fbk):
    predc = set()
    with (
        open(json_file, 'r') as reader,
        open(fbk, 'a') as bk_w,
        ):
        pr_bias(bk_w)
        bk_w.write(':-style_check(-discontiguous).\n')
        i = 0
        for l in reader:
            l = l.strip()
            if global_setting.lemma_delimiter not in l:
                if i in pos_neg:
                    l = json.loads(l)
                    hyps_predc(i, l['hyps'], bk_w, predc)
                    goal_predc(i, l['goal'], bk_w, predc)
                i += 1
        pr_mode(predc, bk_w)
        bk_w.write(":- set(refine, auto).\n")

def pr_predc(exg, out):
    with open(out, 'a') as writer:
        for e in exg:
            writer.write("tac({}).\n".format(e))

with open(pos_neg_file, 'r') as r:
    pos_neg_dict = json.load(r)
    tac_pos_neg = pos_neg_dict[tac]
    # tac_pos_neg['pos'] = random.choices(tac_pos_neg['pos'])
    # tac_pos_neg['neg'] = random.choices(tac_pos_neg['neg'])
    pos_neg = tac_pos_neg['pos'] + tac_pos_neg['neg']

if os.path.exists(bk_file):
    os.remove(bk_file)

if os.path.exists(pos_file):
    os.remove(pos_file)

pr_bk(pos_neg, bk_file)
pr_predc(tac_pos_neg['pos'], pos_file)
pr_predc(tac_pos_neg['neg'], neg_file)
