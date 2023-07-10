import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

import random

from lib import global_setting

random.seed(110)

pos_neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/1000_neg.json'
json_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/1000.json'
bk_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl_bk.pl'
exg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl_exg.pl'
bias_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl_bias.pl'
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

# :- modeb(*,mother(+person,-person)).
# :- modeb(*,father(+person,-person)).
# :- determination(grandparent/2,father/2).


def auto_refine(predc, writer):
    writer.write(":- modeh(1,tac(-nat)).\n")
    for p, kind in predc:
        if kind == 'g':
            writer.write(":- modeb(5, {}(+nat, -list)).\n".format(p))
        elif kind == 'h':
            writer.write(":- modeb(5, {}(+nat, -string, -list)).\n".format(p))
        else:
            assert False
    for p, kind in predc:
        if kind == 'g':
            writer.write(":- determination(tac/1, {}/2).\n".format(p))
        elif kind == 'h':
            writer.write(":- determination(tac/1, {}/3).\n".format(p))
        else:
            assert False
    writer.write(":- aleph_set(refine, auto).\n")

# def body_predc(predc, writer):
#     for p in predc:
#         writer.write("body_predc({}).\n".format(p))

def pr_bk(pos_neg, fbk, fbias):
    predc = set()
    with (
        open(json_file, 'r') as reader,
        open(fbk, 'a') as bk_w,
        open(fbias, 'a') as bias_w
        ):
        bk_w.write(':-style_check(-discontiguous).\n')
        bk_w.write(":-begin_bg.\n")
        i = 0
        for l in reader:
            l = l.strip()
            if global_setting.lemma_delimiter not in l:
                if i in pos_neg:
                    l = json.loads(l)
                    hyps_predc(i, l['hyps'], bk_w, predc)
                    goal_predc(i, l['goal'], bk_w, predc)
                i += 1
        bk_w.write(":-end_bg.\n")
        auto_refine(predc, bias_w)
        # body_predc(predc, writer)

def pr_predc(pos, neg, out):
    with open(out, 'a') as writer:
        writer.write(":-begin_in_pos.\n")
        for p in pos:
            writer.write("tac({}).\n".format(p))
        writer.write(":-end_in_pos.\n")
        writer.write(":-begin_in_neg.\n")
        for n in neg:
            writer.write("tac({}).\n".format(n))
        writer.write(":-end_in_neg.\n")


with open(pos_neg_file, 'r') as r:
    pos_neg_dict = json.load(r)
    tac_pos_neg = pos_neg_dict[tac]
    tac_pos_neg['pos'] = random.choices(tac_pos_neg['pos'], k = 3)
    tac_pos_neg['neg'] = random.choices(tac_pos_neg['neg'], k = 5)
    pos_neg = tac_pos_neg['pos'] + tac_pos_neg['neg']

if os.path.exists(bk_file):
    os.remove(bk_file)

if os.path.exists(exg_file):
    os.remove(exg_file)

if os.path.exists(bias_file):
    os.remove(bias_file)


pr_bk(pos_neg, bk_file, bias_file)
pr_predc(tac_pos_neg['pos'], tac_pos_neg['neg'], exg_file)