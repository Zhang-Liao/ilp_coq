import os
import sys
import random

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def get_ids(dat):
    return [f"{i}\n" for (i, _) in dat]


def shuf_lines(dat, num, out):
    for i in range(20):
        cpy = dat.copy()
        random.shuffle(cpy)
        train = get_ids(cpy[:num])
        valid = get_ids(cpy[num : 2 * num])
        test = get_ids(cpy[2 * num : 3 * num])

        with open(os.path.join(out, f"train{i}.split"), "w") as w:
            w.writelines(train)

        with open(os.path.join(out, f"valid{i}.split"), "w") as w:
            w.writelines(valid)

        with open(os.path.join(out, f"test{i}.split"), "w") as w:
            w.writelines(test)


dataset = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg"
sub_dir = "theories/MSets"
out = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/rand_lines/all_dataset"
from_subdir = False

if not os.path.exists(out):
    os.makedirs(out)

if from_subdir:
    dat = utils.load_subdir_no_lemma(dataset, sub_dir)
    rand_line_num = 3000
else:
    # roughly 5% of states
    rand_line_num = 8000
    dat = utils.load_dataset_no_lemma(dataset)

shuf_lines(dat, rand_line_num, out)
