import os
import random
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

f_lemmas = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/lemmas'
split_size = 1137
dat_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/before_after'

def load_split_lemmas():
    with open(f_lemmas, 'r') as r:
        lemmas = r.readlines()
        # lemmas = [l.strip() for l in lemmas]
    return lemmas

def load_file(f, dat):
    lemma_states = []
    with open(f, 'r') as reader:
        for line in reader:
            # line = line.strip()
            if utils.not_lemma(line):
                lemma_states.append(line)
            else:
                if lemma_states != []:
                    dat[lemma] = lemma_states
                lemma = line
                lemma_states = []
        dat[lemma] = lemma_states
    return dat

def valid(f):
    return f.endswith('.json') & (('plugins/' in f) | ('theories/' in f))

def load_dataset():
    dat = {}
    for root, _, files in os.walk(dat_dir):
        for file in files:
            path = os.path.join(root, file)
            if valid(path):
                dat = load_file(path, dat)
    return dat

def iter(lemmas, dat, i):
    random.shuffle(lemmas)
    train = lemmas[0:split_size]
    test = lemmas[split_size:(2 * split_size)]
    with open(f'data/json/predicate/20splits/train{i}.json', 'w') as w:
        for lm in train:
            w.write(lm)
            w.writelines(dat[lm])

    with open(f'data/json/predicate/20splits/test{i}.json', 'w') as w:
        for lm in test:
            w.write(lm)
            w.writelines(dat[lm])

def iters(lemmas, dat):
    for i in range(3):
        iter(lemmas, dat, i)

lemmas = load_split_lemmas()
dat = load_dataset()
iters(lemmas, dat)