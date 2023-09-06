import os
import random
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

split_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/rand_lemmas'
dat_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/before_after'
out_dir = os.path.join(dat_dir, 'rand_train_test')
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

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

def iter(train, test, dat, i):
    with open(os.path.join(out_dir, f'train{i}.json'), 'w') as w:
        for lm in train:
            w.write(lm)
            w.writelines(dat[lm])

    with open(os.path.join(out_dir, f'test{i}.json'), 'w') as w:
        for lm in test:
            w.write(lm)
            w.writelines(dat[lm])

def iters(dat):
    for i in range(20):
        with open(os.path.join(split_dir, f'train{i}')) as r:
            train = r.readlines()
        with open(os.path.join(split_dir, f'test{i}')) as r:
            test = r.readlines()
        iter(train, test, dat, i)

dat = load_dataset()
iters(dat)