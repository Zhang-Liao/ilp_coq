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
def to_predc_name(s):
    if not s.startswith('coq_'):
        s = 'coq_' + s
    s = s.replace('.', '_')
    s = s.replace('₁', '_under1_')
    s = s.replace('₂', '_under2_')
    s = s.replace('₃', '_under3_')
    return s

def goal_idx(idx):
    idx = ",".join(idx)
    idx = "[" + idx +"]"
    return idx

def hyp_idx(idx):
    idx[0] = to_predc_name(idx[0])
    idx = ",".join(idx)
    idx = "[" + idx +"]"
    return idx

def pr_hyps_predc(i, l, writer):
    for ident, name, idx in l:
        ident = to_predc_name(ident)
        name = to_predc_name(name)
        writer.write(f"{ident}({i},\"{name}\",{hyp_idx(idx)}).\n")

def pr_goal_predc(i, l, writer):
    for ident, idx in l:
        if ident != 'coq_app':
            ident = to_predc_name(ident)
            writer.write(f"{ident}({i},{goal_idx(idx)}).\n")

def add_hyps_predc(l, predc_set):
    for ident, _, _ in l:
        if ident != 'coq_app':
            predc_set.add(to_predc_name(ident))
    return predc_set

def add_goal_predc(l, predc_set):
    for ident, _, in l:
        if ident != 'coq_app':
            predc_set.add(to_predc_name(ident))
    return predc_set

# ## and @@ do not exist in tactics in the Coq standard library
def tac_as_file(t):
    t = t.replace('/', '##')
    t = t.replace("'", '@@')
    return t
