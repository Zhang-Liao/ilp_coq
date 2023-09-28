import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

split_dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/rand_lemmas"
dat_dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/anonym"
out_dir = os.path.join(dat_dir, "rand_train_test")
if not os.path.exists(out_dir):
    os.mkdir(out_dir)


def iter(train, test, valid, dat, i):
    with open(os.path.join(out_dir, f"train{i}.json"), "w") as w:
        for lm in train:
            w.write(lm)
            w.writelines(dat[lm])

    with open(os.path.join(out_dir, f"test{i}.json"), "w") as w:
        for lm in test:
            w.write(lm)
            w.writelines(dat[lm])

    with open(os.path.join(out_dir, f"valid{i}.json"), "w") as w:
        for lm in valid:
            w.write(lm)
            w.writelines(dat[lm])


def iters(dat):
    for i in range(20):
        with open(os.path.join(split_dir, f"train{i}")) as r:
            train = r.readlines()
        with open(os.path.join(split_dir, f"test{i}")) as r:
            test = r.readlines()
        with open(os.path.join(split_dir, f"valid{i}")) as r:
            valid = r.readlines()
        iter(train, test, valid, dat, i)


dat = utils.load_dataset(dat_dir)
iters(dat)
