import json
import os

from lib import utils


cluster_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/split0_pos.json'
neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/split0_neg.json'
dat_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split0.json'
bias_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/bias_prop.pl'
out_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto/neg4/prop'
tac2id_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/tac2id.json'
neg_ratio = 4

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
    utils.pr_hyps_prop_predc(i, l, writer)
    return utils.add_hyps_prop_predc(l, predc)

def pr_goal_predc(i, l, writer, predc):
    utils.pr_goal_prop_predc(i, l, writer)
    return utils.add_goal_prop_predc(l, predc)

def pr_bias(w):
    with open(bias_file,'r') as r:
        for b in r:
            b = b.strip()
            w.write(b + '\n')
    w.write(f':- set(noise, 0).\n')

def pr_bk(poss, negs, fbk, tac):
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
                if row_i in poss:
                    l = json.loads(l)
                    hyp_predc = pr_hyps_predc(row_i, l['hyps'], bk_w, hyp_predc)
                    goal_predc = pr_goal_predc(row_i, l['goal'], bk_w, goal_predc)
                elif row_i in negs:
                    l = json.loads(l)
                    pr_hyps_predc(row_i, l['hyps'], bk_w, set())
                    pr_goal_predc(row_i, l['goal'], bk_w, set())
            row_i += 1
        pr_mode(hyp_predc, goal_predc, bk_w, tac)
        pr_bias(bk_w)

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

def get_negs(neg_dict, poss, tac):
    negss = neg_dict[tac]
    needed_negs = []
    for pos in poss:
        needed_negs += negss[str(pos)][:neg_ratio]
    needed_negs = list(set(needed_negs))
    needed_negs.sort()
    return needed_negs

def pr_run(tac, out, run, rule):
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
    rule_file = os.path.join(out_dir, tac + '_rule.pl')
    for f in [bk_file, pos_file, neg_file, run_file, rule_file]:
        if os.path.exists(f):
            os.remove(f)
    return bk_file, pos_file, neg_file, run_file, rule_file

with open(tac2id_file, 'r') as r:
    tac2id = json.load(r)

with open(neg_file, 'r') as r:
    neg_dict = json.load(r)

with open(cluster_file, 'r') as r:
    for origin_tac, posss in json.load(r).items():
        safe_tac = utils.safe_tac(origin_tac)
        tac_id = tac2id[safe_tac]
        for i in range(len(posss)):
            poss = posss[i]
            tac = str(tac_id) + 'c' + str(i)
            negs = get_negs(neg_dict, poss, origin_tac)
            bk_file, pos_file, neg_file, run_file, rule_file = init_files(tac)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            pr_bk(poss, negs, bk_file, safe_tac)
            pr_exg_predc(poss, pos_file, safe_tac)
            pr_exg_predc(negs, neg_file, safe_tac)
            pr_run(tac, out_dir, run_file, rule_file)