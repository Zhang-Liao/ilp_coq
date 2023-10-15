import json
import os

import argparse

from lib import utils


tac2id_file = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/tac2id.json"


def pr_mode(hyp_predc, goal_predc, writer, tac):
    writer.write(f':- modeh(1, tac(+nat, "{tac}")).\n')
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


def pr_hyps_predc(i, l, writer, predc, kind):
    if kind in ["rel", "prop"]:
        utils.pr_hyps_predc(i, l, writer)
        return utils.add_hyps_predc(l, predc)
    elif kind == "anonym":
        utils.pr_hyps_anonym_predc(i, l, writer)
        return utils.add_hyps_anonym_predc(l, predc)


def pr_goal_predc(i, l, writer, predc, kind):
    if kind in ["rel", "prop"]:
        utils.pr_goal_predc(i, l, writer)
        return utils.add_goal_predc(l, predc)
    elif kind == "anonym":
        utils.pr_goal_anonym_predc(i, l, writer)
        return utils.add_goal_anonym_predc(l, predc)


def pr_bias(w, bias):
    with open(bias, "r") as r:
        for b in r:
            b = b.strip()
            w.write(b + "\n")
    w.write(f":- set(noise, 0).\n")


def pr_bk(poss, negs, fbk, tac, opts):
    hyp_predc = set()
    goal_predc = set()
    with (
        open(opts.dat, "r") as reader,
        open(fbk, "a") as bk_w,
    ):
        bk_w.write(":-style_check(-discontiguous).\n")
        row_i = 0
        for l in reader:
            l = l.strip()
            if utils.not_lemma(l):
                if row_i in poss:
                    l = json.loads(l)
                    hyp_predc = pr_hyps_predc(
                        row_i, l["hyps"], bk_w, hyp_predc, opts.kind
                    )
                    goal_predc = pr_goal_predc(
                        row_i, l["goal"], bk_w, goal_predc, opts.kind
                    )
                elif row_i in negs:
                    l = json.loads(l)
                    pr_hyps_predc(row_i, l["hyps"], bk_w, set(), opts.kind)
                    pr_goal_predc(row_i, l["goal"], bk_w, set(), opts.kind)
            row_i += 1
        pr_mode(hyp_predc, goal_predc, bk_w, tac)
        pr_bias(bk_w, opts.bias)


def pr_exg_predc(exg, out, tac):
    with open(out, "a") as writer:
        for e in exg:
            writer.write(f'tac({e}, "{tac}").\n')


def flatten_neg_mat(mat):
    flat = []
    for row in mat:
        flat += row
    # print(flat)
    return flat


def get_negs(neg_dict, poss, tac, neg_ratio):
    negss = neg_dict[tac]
    needed_negs = []

    for pos in poss:
        needed_negs += negss[str(pos)][:neg_ratio]
    needed_negs = list(set(needed_negs))
    needed_negs.sort()

    # n_pos = len(poss)
    # n_neg = 0
    # curr_neg = neg_ratio
    # while (n_neg < n_pos * neg_ratio) & (curr_neg <= max_neg_ratio):
    #     for pos in poss:
    #         needed_negs += negss[str(pos)][:curr_neg]
    #     needed_negs = list(set(needed_negs))
    #     needed_negs.sort()
    #     curr_neg += 1
    #     n_neg = len(needed_negs)
    return needed_negs


def pr_run(tac, run):
    # load_path = out + '/' + tac
    with open(run, "w") as w:
        w.write(":- ['/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/aleph_orig'].\n")
        w.write(f":-read_all('{tac}').\n")
        w.write(":-induce.\n")
        w.write(f":-write_rules('{tac}_rule.pl').\n")
        w.write(":-halt.")


def init_files(tac, out_dir):
    bk_file = os.path.join(out_dir, tac + ".b")
    pos_file = os.path.join(out_dir, tac + ".f")
    neg_file = os.path.join(out_dir, tac + ".n")
    run_file = os.path.join(out_dir, tac + ".pl")
    rule_file = os.path.join(out_dir, tac + "_rule.pl")
    for f in [bk_file, pos_file, neg_file, run_file, rule_file]:
        if os.path.exists(f):
            os.remove(f)
    return bk_file, pos_file, neg_file, run_file


def gen_tac_file(origin_tac, posss):
    safe_tac = utils.safe_tac(origin_tac)
    tac_id = tac2id[safe_tac]
    for i in range(len(posss)):
        poss = posss[i]
        tac = str(tac_id) + "c" + str(i)
        negs = get_negs(neg_dict, poss, origin_tac, opts.neg_ratio)
        bk_file, pos_file, neg_file, run_file = init_files(tac, opts.out)
        if not os.path.exists(opts.out):
            os.makedirs(opts.out)
        pr_bk(poss, negs, bk_file, safe_tac, opts)
        pr_exg_predc(poss, pos_file, safe_tac)
        pr_exg_predc(negs, neg_file, safe_tac)
        pr_run(tac, run_file)


parser = argparse.ArgumentParser()
parser.add_argument("--neg", type=str)
parser.add_argument("--cluster", type=str)
parser.add_argument("--dat", type=str)
parser.add_argument("--out", type=str)
parser.add_argument("--kind", type=str, choices=["prop", "rel", "anonym"])
parser.add_argument("--bias", type=str)
parser.add_argument("--neg_ratio", type=int)
parser.add_argument("--only_common", action=argparse.BooleanOptionalAction)

opts = parser.parse_args()

with open(tac2id_file, "r") as r:
    tac2id = json.load(r)

with open(opts.neg, "r") as r:
    neg_dict = json.load(r)

num_tac = 0

with open(opts.cluster, "r") as r:
    for origin_tac, posss in json.load(r).items():
        if opts.only_common != None:
            if origin_tac in utils.COMMON_TAC:
                gen_tac_file(origin_tac, posss)
        else:
            gen_tac_file(origin_tac, posss)

log = {
    "tac2id_file": tac2id_file,
    "neg_ratio": opts.neg_ratio,
    "options": opts.__dict__,
}
with open(os.path.join(opts.out, "log.json"), "w") as w:
    json.dump(log, w, indent=4)
