import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))

from lib import utils

DAT_DIR = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/anonym"
OUT = "/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_ident_predc2.pl"
KIND = "anonym"
assert KIND in ["prop", "rel", "anonym"]


def pr_hyp_predc(predc, writer):
    for p in predc:
        writer.write(f"{p}(-1, none, []).\n")


def pr_goal_predc(predc, writer):
    for p in predc:
        writer.write(f"{p}(-1, []).\n")


def pr_goal_to_hyp(goal, hyp, writer):
    for x in utils.goal_predc_to_hyp_predc(goal, hyp):
        writer.write(f"{x}\n")


def pr_multifiles(hyp_predc, goal_predc, w):
    w.write(f":- multifile hyp_predc/1.\n")
    w.write(f":- multifile goal_predc/1.\n")

    for p in hyp_predc:
        w.write(f":- multifile {p}/3.\n")
    for p in goal_predc:
        w.write(f":- multifile {p}/2.\n")


def row_predc(r, hyp_predc, goal_predc):
    r = json.loads(r)

    if KIND in ["prop", "rel"]:
        goal_predc = utils.add_goal_predc(r["goal"], goal_predc)
        hyp_predc = utils.add_hyps_predc(r["hyps"], hyp_predc)
    elif KIND == "anonym":
        goal_predc = utils.add_goal_anonym_predc(r["goal"], goal_predc)
        hyp_predc = utils.add_hyps_anonym_predc(r["hyps"], hyp_predc)
    return hyp_predc, goal_predc


def read_predc():
    hyp_predc = set()
    goal_predc = set()
    dat = utils.load_dataset(DAT_DIR)
    for sts in dat.values():
        for st in sts:
            hyp_predc, goal_predc = row_predc(st, hyp_predc, goal_predc)
    goal_predc = [utils.to_predc_name(p) for p in goal_predc]
    hyp_predc = [utils.to_predc_name(p) for p in hyp_predc]
    return hyp_predc, goal_predc


def pr_predc(hyp, goal):
    with open(OUT, "a") as w:
        # w.write(':-style_check(-discontiguous).\n')
        pr_multifiles(hyp, goal, w)
        pr_hyp_predc(hyp, w)
        pr_goal_predc(goal, w)
        pr_goal_to_hyp(goal, hyp, w)


if os.path.exists(OUT):
    os.remove(OUT)

hyp_predc, goal_predc = read_predc()
pr_predc(hyp_predc, goal_predc)
