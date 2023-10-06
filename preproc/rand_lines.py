import os
import sys
import random

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def get_ids(dat):
    return [f"{i}\n" for (i, _) in dat]


def shuf_lines(dat, num, out):
    for i in range(10):
        cpy = dat.copy()
        random.shuffle(cpy)
        train = get_ids(cpy[:num])
        test = get_ids(cpy[num : num + num])
        with open(os.path.join(out, f"train{i}.split"), "w") as w:
            w.writelines(train)

        with open(os.path.join(out, f"test{i}.split"), "w") as w:
            w.writelines(test)


dataset = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg"
file_order = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/file_order"
out = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/rand_lines"
rand_line_num = 100
dat = []
with open(file_order, "r") as r:
    files = r.readlines()
    files = [f.strip() for f in files]

i = 0
for f in files:
    path = os.path.join(dataset, f)
    if not os.path.exists(path):
        raise FileNotFoundError(f)

    with open(path, "r") as r:
        for l in r:
            if utils.not_lemma(l):
                dat.append((i, l))
            i += 1

shuf_lines(dat, rand_line_num, out)
