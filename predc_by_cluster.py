import json
import os

import argparse

from lib import utils


tac2id_file = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/tac2id.json"


def pr_origin_mode(writer, tac):
    writer.write(f':- modeh(1, tac(+nat, "{tac}")).\n')
    writer.write(f":- modeb(*, goal_node(#coq_predc, +nat, -goal_idx)).\n")
    writer.write(f":- modeb(*, hyp_node(#coq_predc, +nat, -string, -hyp_idx)).\n")

    writer.write(f":- determination(tac/2, goal_node/3).\n")
    writer.write(f":- determination(tac/2, hyp_node/4).\n")


def pr_anonym_mode(writer, tac, ident):
    for id in ident:
        writer.write(f"coq_ident({id}).\n")

    writer.write(f':- modeh(1, tac(+nat, "{tac}")).\n')
    writer.write(f":- modeb(*, goal_node(#coq_predc, +nat, -goal_idx, -coq_ident)).\n")
    writer.write(
        f":- modeb(*, hyp_node(#coq_predc, +nat, -string, -hyp_idx, -coq_ident)).\n"
    )

    writer.write(f":- determination(tac/2, goal_node/4).\n")
    writer.write(f":- determination(tac/2, hyp_node/5).\n")


def pr_mode(hyp_predc, goal_predc, writer, tac, ident, kind):
    for p in goal_predc:
        writer.write(f"coq_predc({p}).\n")
    for p in hyp_predc:
        writer.write(f"coq_predc({p}).\n")
    if kind == "anonym":
        pr_anonym_mode(writer, tac, ident)
    elif kind == "origin":
        pr_origin_mode(writer, tac)


def pr_hyps_predc(i, l, writer, predc, kind, ident):
    if kind in ["origin"]:
        utils.pr_hyps_predc(i, l, writer)
        return utils.add_hyps_predc(l, predc), set()
    elif kind == "anonym":
        utils.pr_hyps_anonym_predc(i, l, writer)
        return utils.add_hyps_anonym_predc(l, predc, ident)


def pr_goal_predc(i, l, writer, predc, kind, ident):
    if kind in ["origin"]:
        utils.pr_goal_predc(i, l, writer)
        return utils.add_goal_predc(l, predc), set()
    elif kind == "anonym":
        utils.pr_goal_anonym_predc(i, l, writer)
        return utils.add_goal_anonym_predc(l, predc, ident)


def pr_bias(w, bias):
    path = os.path.abspath(bias)
    w.write(f":- consult('{path}').\n")
    # with open(bias, "r") as r:
    #     w.writelines(r.readlines())
    # w.write(f":- set(noise, 0).\n")


def pr_bk(poss, negs, fbk, tac, opts):
    hyp_predc = set()
    goal_predc = set()
    ident = set()
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
                    # Merely add the identifiers from positive examples.
                    hyp_predc, ident = pr_hyps_predc(
                        row_i, l["hyps"], bk_w, hyp_predc, opts.kind, ident
                    )
                    goal_predc, ident = pr_goal_predc(
                        row_i, l["goal"], bk_w, goal_predc, opts.kind, ident
                    )
                elif row_i in negs:
                    l = json.loads(l)
                    pr_hyps_predc(row_i, l["hyps"], bk_w, set(), opts.kind, set())
                    pr_goal_predc(row_i, l["goal"], bk_w, set(), opts.kind, set())
            row_i += 1
        if (negs == []) | (len(poss) == 1):
            bk_w.write(f":- consult('/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/user_cost.pl').\n")

        pr_mode(hyp_predc, goal_predc, bk_w, tac, ident, opts.kind)
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

    # set neg
    for pos in poss:
        needed_negs += negss[str(pos)][:neg_ratio]
    needed_negs = list(set(needed_negs))
    needed_negs.sort()

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
parser.add_argument("--kind", type=str, choices=["origin", "anonym"])
parser.add_argument("--bias", type=str)
parser.add_argument("--neg_ratio", type=int)

opts = parser.parse_args()

with open(tac2id_file, "r") as r:
    tac2id = json.load(r)

with open(opts.neg, "r") as r:
    neg_dict = json.load(r)

num_tac = 0

with open(opts.cluster, "r") as r:
    for origin_tac, posss in json.load(r).items():
        gen_tac_file(origin_tac, posss)

log = {
    "tac2id_file": tac2id_file,
    "neg_ratio": opts.neg_ratio,
    "options": opts.__dict__,
}
with open(os.path.join(opts.out, "log.json"), "w") as w:
    json.dump(log, w, indent=4)
