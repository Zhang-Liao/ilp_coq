import argparse

import json
import math
import os

from lib import utils

# pos_neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/split0_neg.json'
# dat_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split0.json'
# bias_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/bias_auto.pl'
# out_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto/no_cluster2'
tac2id_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/tac2id.json'
neg_ratio = 10

# noise = 0.1

def pr_mode(hyp_predc, goal_predc, writer, tac):
    writer.write(f":- modeh(1, tac(+nat, \"{tac}\")).\n")
    for p in goal_predc:
        writer.write(f":- modeb(3, {p}(+nat, -goal_idx)).\n")
    for p in hyp_predc:
        writer.write(f":- modeb(3, {p}(+nat, -string, -hyp_idx)).\n")

    for p in goal_predc:
        writer.write(f":- determination(tac/2, {p}/2).\n")
    for p in hyp_predc:
        writer.write(f":- determination(tac/2, {p}/3).\n")

    for p in goal_predc:
        writer.write(f"goal_predc({p}).\n")
    for p in hyp_predc:
        writer.write(f"hyp_predc({p}).\n")


def pr_hyps_predc(i, l, writer, predc):
    utils.pr_hyps_predc(i, l, writer)
    return utils.add_hyps_predc(l, predc)

def pr_goal_predc(i, l, writer, predc):
    utils.pr_goal_predc(i, l, writer)
    return utils.add_goal_predc(l, predc)

def pr_bias(w, bias):
    with open(bias,'r') as r:
        for b in r:
            b = b.strip()
            w.write(b + '\n')
    w.write(':- set(noise, 0).\n')

def pr_bk(pos_dict, neg_dict, fbk, tac, opts):
    hyp_predc = set()
    goal_predc = set()
    with (
        open(opts.dat, 'r') as reader,
        open(fbk, 'a') as bk_w,
        ):
        bk_w.write(':-style_check(-discontiguous).\n')
        row_i = 0
        for l in reader:
            l = l.strip()
            if utils.not_lemma(l):
                if row_i in pos_dict:
                    l = json.loads(l)
                    hyp_predc = pr_hyps_predc(row_i, l['hyps'], bk_w, hyp_predc)
                    goal_predc = pr_goal_predc(row_i, l['goal'], bk_w, goal_predc)
                elif row_i in neg_dict:
                    l = json.loads(l)
                    pr_hyps_predc(row_i, l['hyps'], bk_w, set())
                    pr_goal_predc(row_i, l['goal'], bk_w, set())
            row_i += 1
        pr_mode(hyp_predc, goal_predc, bk_w, tac)
        pr_bias(bk_w, opts.bias)

def pr_exg_predc(exg, out, tac):
    with open(out, 'a') as writer:
        for e in exg:
            writer.write(f"tac({e}, \"{tac}\").\n")

def flatten_neg_mat(mat):
    flat = []
    for row in mat:
        flat += row
    # print(flat)
    return flat

def get_pos_neg(pos_neg_dict):
    pos = [int(p) for p in pos_neg_dict.keys()]
    neg_mat = [n for n in pos_neg_dict.values()]
    neg_mat = [ns[:neg_ratio] for ns in neg_mat]
    neg = list(set(flatten_neg_mat(neg_mat)))
    neg.sort()
    return pos, neg

def pr_run(tac, out, run, rule):
    # load_path = os.path.join(out, tac)
    load_path = out + '/' + tac
    with open (run, 'w') as w:
        w.write(':- [\'/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/aleph_orig\'].\n')
        w.write(f':-read_all(\'{load_path}\').\n')
        w.write(':-induce.\n')
        w.write(f':-write_rules(\'{rule}\').\n')
        w.write(':-halt.')

def init_files(tac, out_dir):
    bk_file = os.path.join(out_dir, tac + '.b')
    pos_file = os.path.join(out_dir, tac + '.f')
    neg_file = os.path.join(out_dir, tac + '.n')
    run_file = os.path.join(out_dir, tac + '.pl')
    rule_file = os.path.join(out_dir, tac + '_rule.pl')
    for f in [bk_file, pos_file, neg_file, run_file, rule_file]:
        if os.path.exists(f):
            os.remove(f)
    return bk_file, pos_file, neg_file, run_file, rule_file

parser = argparse.ArgumentParser()
parser.add_argument("--neg", type=str)
parser.add_argument("--dat", type=str)
parser.add_argument("--out", type=str)
parser.add_argument("--bias", type=str)

opts = parser.parse_args()

with open(tac2id_file, 'r') as r:
    tac2id = json.load(r)

with open(opts.neg, 'r') as r:
    for origin_tac, pos_neg_list in json.load(r).items():
        safe_tac = utils.safe_tac(origin_tac)
        tac_id = str(tac2id[safe_tac])
        pos, neg = get_pos_neg(pos_neg_list)
        bk_file, pos_file, neg_file, run_file, rule_file = init_files(tac_id, opts.out)
        if not os.path.exists(opts.out):
            os.makedirs(opts.out)
        pr_bk(pos, neg, bk_file, safe_tac, opts)
        pr_exg_predc(pos, pos_file, safe_tac)
        pr_exg_predc(neg, neg_file, safe_tac)
        pr_run(tac_id, opts.out, run_file, rule_file)


log = {
    'description' : '' }
with open(os.path.join(opts.out, 'readme.json'), 'w') as w:
    json.dump(log, w, indent=4)


