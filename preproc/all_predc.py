import json
import os
import re
import sys
sys.path.append(os.path.dirname(sys.path[0]))

from lib import utils

dat_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split'
out= '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/all_predc.pl'

def pr_hyp_predc(predc, writer):
    for p in predc:
        p = utils.to_predc_name(p)
        writer.write(f"{p}(-1, none, []).\n")

def pr_goal_predc(predc, writer):
    for p in predc:
        p = utils.to_predc_name(p)
        writer.write(f"{p}(-1, []).\n")

def file_predc(file, hyp_predc, goal_predc):
    with (open(file, 'r') as reader):
        for l in reader:
            l = l.strip()
            if utils.not_lemma(l):
                l = json.loads(l)
                hyp_predc = utils.add_hyps_predc(l['hyps'], hyp_predc)
                goal_predc = utils.add_goal_predc(l['goal'], goal_predc)
    return hyp_predc, goal_predc

def read_predc():
    hyp_predc = set()
    goal_predc = set()
    for filename in os.listdir(dat_dir):
        if re.match('split[0-9].json', filename):
            file = os.path.join(dat_dir, filename)
            hyp_predc, goal_predc = file_predc(file, hyp_predc, goal_predc)
    return hyp_predc, goal_predc

def pr_predc(hyp, goal):
    with open(out, 'a') as w:
        w.write(':-style_check(-discontiguous).\n')
        pr_hyp_predc(hyp, w)
        pr_goal_predc(goal, w)

if os.path.exists(out):
    os.remove(out)

hyp_predc, goal_predc = read_predc()
pr_predc(hyp_predc, goal_predc)