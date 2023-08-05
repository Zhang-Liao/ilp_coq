import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

import math

from lib import global_setting

pos_neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/1000_neg.json'
dat_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/1000.json'
bias_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/bias.pl'
out_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc'
noise = 0.1

# Store tactics as the names of files because converting tactics to predicates has many difficulties.
def tac_as_file(t):
    return t.replace('/', '$')

def idx_str(idx):
    idx = ",".join(idx)
    idx = "[" + idx +"]"
    return idx

def rm_head_dash(i):
    if i[0] == '_':
        i = 'dash_' + i[1:]
    return i

def hyps_predc(i, l, writer, predc):
    for ident, name, idx in l:
        if ident != 'coq_app':
            ident = rm_head_dash(ident)
            name = rm_head_dash(name)
            predc.add((ident, 'h'))
            writer.write(f"{ident}({i},{name},{idx_str(idx)}).\n")

def goal_predc(i, l, writer, predc):
    for ident, idx in l:
        if ident != 'coq_app':
            ident = rm_head_dash(ident)
            predc.add((ident, 'g'))
            writer.write(f"{ident}({i},{idx_str(idx)}).\n")

def pr_bias(w, n_neg):
    with open(bias_file,'r') as r:
        for b in r:
            b = b.strip()
            w.write(b + '\n')
    n_noise = int(math.ceil(n_neg * noise))
    w.write(f':- set(noise, {n_noise}).\n')
    w.write(f':- set(discontinue_noise, {n_noise}).\n')

def pr_predc_typ(predc, writer):
    for p, kind in predc:
        if kind == 'g':
            writer.write(f"goal_predc({p}).\n")
    for p, kind in predc:
        if kind == 'h':
            writer.write(f"hyp_predc({p}).\n")

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
        pr_predc_typ(pos_predc, bk_w)
        pr_bias(bk_w, len(neg_dict))

def pr_predc(exg, out):
    with open(out, 'a') as writer:
        for e in exg:
            writer.write(f"tac({e}).\n")

def neg_ratio(npos):
    if npos <= 16:
        return 8
    elif npos <= 32:
        return 4
    elif npos <= 64:
        return 2
    else:
        return 1

def flatten_neg_mat(mat):
    flat = []
    for row in mat:
        flat += row
    # print(flat)
    return flat

def get_pos_neg(pos_neg_list):
    pos = [e['pos'][0] for e in pos_neg_list]
    neg_mat = [e['neg'] for e in pos_neg_list]
    k = neg_ratio(len(pos))
    neg_mat = [ns[:k] for ns in neg_mat]
    neg = list(set(flatten_neg_mat(neg_mat)))
    return pos, neg

def pr_run(tac, out, run, rule):
    load_path = os.path.join(out, tac)
    with open (run, 'w') as w:
        w.write(':- [\'/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/aleph_orig\', \'/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/refine\'].\n')
        w.write(f':-read_all(\'{load_path}\').\n')
        w.write(':-induce.\n')
        w.write(f':-write_rules(\'{rule}\').\n')

def init_files(tac):
    bk_file = os.path.join(out_dir, tac + '.b')
    pos_file = os.path.join(out_dir, tac + '.f')
    neg_file = os.path.join(out_dir, tac + '.n')
    run_file = os.path.join(out_dir, tac + '.pl')
    rule_file = os.path.join(out_dir, tac + '.rule.pl')
    for f in [bk_file, pos_file, neg_file, run_file, rule_file]:
        if os.path.exists(f):
            os.remove(f)
    return bk_file, pos_file, neg_file, run_file, rule_file

with open(pos_neg_file, 'r') as r:
    for tac, pos_neg_list in json.load(r).items():
        tac = tac_as_file(tac)
        pos, neg = get_pos_neg(pos_neg_list)
        bk_file, pos_file, neg_file, run_file, rule_file = init_files(tac)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        pr_bk(pos, neg, bk_file)
        pr_predc(pos, pos_file)
        pr_predc(neg, neg_file)
        pr_run(tac, out_dir, run_file, rule_file)