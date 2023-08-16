import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

import math

from lib import utils

pos_neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/split0_neg.json'
dat_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split0.json'
bias_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/bias_auto.pl'
out_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto'
# noise = 0.1
noise = 0

def pr_mode(hyp_predc, goal_predc, writer, tac):
    writer.write(f":- modeh(2, tac(+nat, \"{tac}\")).\n")
    for p in goal_predc:
        writer.write(f":- modeb(3, {p}(+nat, -goal_idx)).\n")
    for p in hyp_predc:
        writer.write(f":- modeb(3, {p}(+nat, -string, -hyp_idx)).\n")

    for p in goal_predc:
        writer.write(f":- determination(tac/2, {p}/2).\n")
    for p in hyp_predc:
        writer.write(f":- determination(tac/2, {p}/3).\n")

def pr_hyps_predc(i, l, writer, predc):
    utils.pr_hyps_predc(i, l, writer)
    return utils.add_hyps_predc(l, predc)

def pr_goal_predc(i, l, writer, predc):
    utils.pr_goal_predc(i, l, writer)
    return utils.add_goal_predc(l, predc)

def pr_bias(w, n_neg):
    with open(bias_file,'r') as r:
        for b in r:
            b = b.strip()
            w.write(b + '\n')
    n_noise = int(math.ceil(n_neg * noise))
    w.write(f':- set(noise, {n_noise}).\n')

def pr_bk(pos_dict, neg_dict, fbk, tac):
    hyp_predc = set()
    goal_predc = set()
    with (
        open(dat_file, 'r') as reader,
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
        pr_bias(bk_w, len(neg_dict))

def pr_exg_predc(exg, out, tac):
    with open(out, 'a') as writer:
        for e in exg:
            writer.write(f"tac({e}, \"{tac}\").\n")

def neg_ratio(npos):
    return 4
    # if npos <= 16:
    #     return 8
    # elif npos <= 32:
    #     return 4
    # elif npos <= 64:
    #     return 2
    # else:
    #     return 1

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
    for origin_tac, pos_neg_list in json.load(r).items():
        tac = utils.tac_as_file(origin_tac)
        pos, neg = get_pos_neg(pos_neg_list)
        bk_file, pos_file, neg_file, run_file, rule_file = init_files(tac)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        try:
            pr_bk(pos, neg, bk_file, origin_tac)
            pr_exg_predc(pos, pos_file, origin_tac)
            pr_exg_predc(neg, neg_file, origin_tac)
            pr_run(tac, out_dir, run_file, rule_file)
        except OSError as e:
            if e.errno == 36:
                print('Ignore', e)
                continue
            else:
                raise