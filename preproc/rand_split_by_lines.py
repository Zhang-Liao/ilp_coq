import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

split_dir = "data/rand_lines/MSets"
subdir = "theories/MSets"
dat_dir = "data/json/predicate/origin"
out_dir = os.path.join(dat_dir, "tune/MSets/")

if not os.path.exists(out_dir):
    os.makedirs(out_dir)


def iter(train, test, dat, i):
    with open(os.path.join(out_dir, f"train{i}.json"), "w") as w:
        for id in train:
            w.write(dat[id])

    with open(os.path.join(out_dir, f"test{i}.json"), "w") as w:
        for id in test:
            w.write(dat[id])


def iters(dat):
    for i in range(10):
        with open(os.path.join(split_dir, f"train{i}.split")) as r:
            train = r.readlines()
        with open(os.path.join(split_dir, f"test{i}.split")) as r:
            test = r.readlines()
        train = [int(l) for l in train]
        test = [int(l) for l in test]
        iter(train, test, dat, i)


dat = utils.load_subdir_no_lemma(dat_dir, subdir)
dat = dict(dat)
iters(dat)
