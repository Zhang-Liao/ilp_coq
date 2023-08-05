import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib.global_setting import *

def output_lemma_aux(lemma, data , file):
    with open(file, 'a') as writer:
        writer.write(f"#lemma\t{lemma}\n")
        for state in data:
            writer.write(state + '\n')

def lemma_name(l):
    return l.split('\t')[1]

def pred_lemmas(pred_file):
    ls = []
    with open(pred_file, 'r') as reader:
        for l in reader:
            l = l.strip("\n")
            if lemma_delimiter in l:
                ls.append(lemma_name(l))
    return ls


def load_by_lemma(file, dict, func):
    lemma_tacs = []
    with open(file, 'r') as reader:
        for line in reader:
            line = line.strip("\n")
            if lemma_delimiter not in line:
                lemma_tacs.append(func(line))
            else:
                if lemma_tacs != []:
                    dict[lemma] = lemma_tacs
                lemma = line.split('\t')[1]
                lemma_tacs = []
        dict[lemma] = lemma_tacs
    return dict

## For predicates
def idx_str(idx):
    idx = ",".join(idx)
    idx = "[" + idx +"]"
    return idx

def rm_head_dash(i):
    if i[0] == '_':
        i = 'dash_' + i[1:]
    return i

# def pr_hyp_predc(ident, i, name, idx):
#     ident = rm_head_dash(ident)
#     name = rm_head_dash(name)
#     return f"{ident}({i},\"{name}\",{idx_str(idx)})."

# def pr_goal_predc(ident, i, idx):
#     ident = rm_head_dash(ident)
#     return f"{ident}({i}, {idx_str(idx)})."

def pr_hyps_predc(i, l, writer):
    for ident, name, idx in l:
        ident = rm_head_dash(ident)
        name = rm_head_dash(name)
        writer.write(f"{ident}({i},\"{name}\",{idx_str(idx)}).\n")

def pr_goal_predc(i, l, writer):
    for ident, idx in l:
        if ident != 'coq_app':
            ident = rm_head_dash(ident)
            writer.write(f"{ident}({i},{idx_str(idx)}).\n")

def add_hyps_predc(l, predc_set):
    for ident, _, _ in l:
        if ident != 'coq_app':
            predc_set.add(rm_head_dash(ident))
    return predc_set

def add_goal_predc(l, predc_set):
    for ident, _, in l:
        if ident != 'coq_app':
            predc_set.add(rm_head_dash(ident))
    return predc_set
