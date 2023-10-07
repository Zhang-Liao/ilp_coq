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
sub_dir = "theories/MSets"
out = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/rand_lines/MSets"
rand_line_num = 3000

dat = utils.load_subdir_no_lemma(dataset, sub_dir)

shuf_lines(dat, rand_line_num, out)
