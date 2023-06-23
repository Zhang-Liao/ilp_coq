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