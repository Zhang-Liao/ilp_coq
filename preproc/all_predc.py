import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

from lib import utils

DAT_DIR = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/anonym/"
OUT = "/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_anonym_predc.pl"
KIND = "anonym"
assert KIND in ["prop", "rel", "anonym"]


def pr_hyp_predc(predc, writer):
    for p in predc:
        writer.write(f"{p}(-1, none, []).\n")


def pr_goal_predc(predc, writer):
    for p in predc:
        writer.write(f"{p}(-1, []).\n")


def pr_multifiles(hyp_predc, goal_predc, w):
    w.write(f":- multifile hyp_predc/1.\n")
    w.write(f":- multifile goal_predc/1.\n")
    w.write(f":- multifile hyp_coq_var/4.\n")
    w.write(f":- multifile goal_coq_var/3.\n")
    # TODO: replace by hyp_coq_var and goal_coq_var
    w.write(f":- multifile var/2.\n")
    w.write(f":- multifile var/3.\n")

    for p in hyp_predc:
        w.write(f":- multifile {p}/3.\n")
    for p in goal_predc:
        w.write(f":- multifile {p}/2.\n")


def row_predc(r, hyp_predc, goal_predc):
    r = json.loads(r)

    if KIND == "prop":
        goal_predc = utils.add_goal_prop_predc(r["goal"], goal_predc)
        hyp_predc = utils.add_hyps_prop_predc(r["hyps"], hyp_predc)
    elif KIND == "rel":
        goal_predc = utils.add_goal_predc(r["goal"], goal_predc)
        hyp_predc = utils.add_hyps_predc(r["hyps"], hyp_predc)
    elif KIND == "anonym":
        goal_predc = utils.add_goal_anonym_predc(r["goal"], goal_predc)
        hyp_predc = utils.add_hyps_anonym_predc(r["hyps"], hyp_predc)
    return hyp_predc, goal_predc


# def file_predc(file, hyp_predc, goal_predc):
#     with (open(file, 'r') as reader):
#         for l in reader:
#             l = l.strip()
#             if utils.not_lemma(l):
#                 row_predc(l, hyp_predc, goal_predc)
#     return hyp_predc, goal_predc


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


if os.path.exists(OUT):
    os.remove(OUT)

hyp_predc, goal_predc = read_predc()
pr_predc(hyp_predc, goal_predc)
