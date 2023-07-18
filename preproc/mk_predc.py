import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

import random

from lib import global_setting

random.seed(110)

pos_neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/1000_neg.json'
dat_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/1000.json'
# bk_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl.b'
# pos_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl.f'
# neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl.n'
bias_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/bias.pl'
out_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc'

def tac_as_file(t):
    return t.replace('/', '$')

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
    with open(bias_file,'r') as r:
        for b in r:
            w.write(b)

def pr_predc_typ(predc, writer):
    for p, kind in predc:
        if kind == 'g':
            writer.write("body_predc({}).\n".format(p))
    for p, kind in predc:
        if kind == 'h':
            writer.write("hyp_predc({}).\n".format(p))

def pr_bk(pos_dict, neg_dict, fbk):
    pos_predc = set()
    with (
        open(dat_file, 'r') as reader,
        open(fbk, 'a') as bk_w,
        ):
        bk_w.write(':-style_check(-discontiguous).\n')
        i = 0
        for l in reader:
            l = l.strip()
            if global_setting.lemma_delimiter not in l:
                if i in pos_dict:
                    l = json.loads(l)
                    hyps_predc(i, l['hyps'], bk_w, pos_predc)
                    goal_predc(i, l['goal'], bk_w, pos_predc)
                elif i in neg_dict:
                    l = json.loads(l)
                    hyps_predc(i, l['hyps'], bk_w, set())
                    goal_predc(i, l['goal'], bk_w, set())
                i += 1
        pr_mode(pos_predc, bk_w)
        pr_predc_typ(pos_predc, bk_w)
        pr_bias(bk_w)

def pr_predc(exg, out):
    with open(out, 'a') as writer:
        for e in exg:
            writer.write("tac({}).\n".format(e))

with open(pos_neg_file, 'r') as r:
    for tac, pos_neg in json.load(r).items():
        tac = tac_as_file(tac)
        pos_ids = pos_neg['pos']
        neg_ids = pos_neg['neg']
        # tac_pos_neg['pos'] = random.choices(tac_pos_neg['pos'])
        # tac_pos_neg['neg'] = random.choices(tac_pos_neg['neg'])
        bk_file = os.path.join(out_dir, tac + '.b')
        pos_file = os.path.join(out_dir, tac + '.f')
        neg_file = os.path.join(out_dir, tac + '.n')

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if os.path.exists(bk_file):
            os.remove(bk_file)
        if os.path.exists(pos_file):
            os.remove(pos_file)
        if os.path.exists(neg_file):
            os.remove(neg_file)

        pr_bk(pos_ids, neg_ids, bk_file)
        pr_predc(pos_ids, pos_file)
        pr_predc(neg_ids, neg_file)
