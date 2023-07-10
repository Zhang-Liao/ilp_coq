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
tac = 'simpl'

def idx_str(idx):
    idx = ",".join(idx)
    idx = "[" + idx +"]"
    return idx

def hyps_predc(i, l, writer, predc):
    for ident, name, idx in l:
        if ident != 'app':
            predc.add(ident)
            writer.write("{}({},{},{}).\n".format(ident, i, name, idx_str(idx)))

def goal_predc(i, l, writer, predc):
    for ident, idx in l:
        if ident != 'app':
            predc.add(ident)
            writer.write("{}({},{}).\n".format(ident, i, idx_str(idx)))

def body_predc(predc, writer):
    for p in predc:
        writer.write("body_predc({}).\n".format(p))

def pr_bk(pos_neg, out):
    predc = set()
    with (
        open(json_file, 'r') as reader,
        open(out, 'a') as writer):
        writer.write(":-begin_bg.\n")
        i = 0
        for l in reader:
            l = l.strip()
            if global_setting.lemma_delimiter not in l:
                if i in pos_neg:
                    l = json.loads(l)
                    hyps_predc(i, l['hyps'], writer, predc)
                    goal_predc(i, l['goal'], writer, predc)
                i += 1
        writer.write(":-end_bg.\n")
        body_predc(predc, writer)

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

pr_bk(pos_neg, bk_file)
pr_predc(tac_pos_neg['pos'], tac_pos_neg['neg'], exg_file)