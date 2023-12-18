import os
import random
import sys

sys.path.append(os.path.dirname(sys.path[0]))

from lib import utils

ALL_THEORY = [
    "theories/Setoids",
    "theories/Sorting",
    "theories/Logic",
    "theories/Arith",
    "theories/Program",
    "theories/Numbers",
    "theories/Floats",
    "theories/QArith",
    "theories/Bool",
    "theories/MSets",
    "theories/PArith",
    "theories/Classes",
    "theories/Sets",
    "theories/Lists",
    "theories/Vectors",
    "theories/FSets",
    "theories/NArith",
    "theories/Strings",
    "theories/Relations",
    "theories/Structures",
    "theories/Reals",
    "theories/ZArith",
    "theories/Wellfounded",
    "theories/Init",
    "plugins/omega",
    "plugins/micromega",
    "plugins/btauto",
    "plugins/ssr",
    "plugins/nsatz",
    "plugins/funind",
    "plugins/rtauto",
    "plugins/setoid_ring",
]

train_test_theories = [
    # train
    "theories/QArith",
    # test
    "theories/Sorting",
    "theories/Init",
    "plugins/setoid_ring",
    "theories/Vectors",
    "theories/NArith"
]


def valid_file(f):
    if utils.valid_dat_f(f):
        return all(x not in f for x in train_test_theories)
    else:
        return False


def load_dat(dir):
    paths = []
    dat = []
    for theory in ALL_THEORY:
        path = os.path.join(dir, f'{theory}.json')
        if valid_file(path):
            # print(path)
            paths.append(path)
    paths = sorted(paths)
    for path in paths:
        r = open(path, "r")
        f_dat = r.readlines()
        # f_dat = [x for x in f_dat if utils.not_lemma(x)]
        dat += f_dat
    dat = list(zip(range(len(dat)), dat))
    return dat


def rand_lines(all_lines):
    random.shuffle(all_lines)
    lines = all_lines[:7000]
    ids = [str(l[0]) + '\n' for l in lines]
    dat = [l[1] for l in lines]
    return ids, dat

def load_lines_by_ids(id_lines, ids_f):
    dat = []
    all_lines = [l[1] for l in id_lines]
    r = open(ids_f, 'r')
    ids = r.readlines()
    ids = [int(x) for x in ids]
    for id in ids:
        dat.append(all_lines[id])
    return dat

merge_dir = "data/json/ortho/predicate/anonym/merge"
rand_ids_f = 'data/json/ortho/feat/merge/valid/valid_ids'
dat = load_dat(merge_dir)
print('data length without train and test', len(dat))

if rand_ids_f == None: 
    ids, rand_dat = rand_lines(dat)

    with open(os.path.join(merge_dir, 'valid_ids'), 'w') as w:
        w.writelines(ids)

    with open(os.path.join(merge_dir, 'valid.json'), 'w') as w:
        w.writelines(rand_dat)
else:
    rand_dat = load_lines_by_ids(dat, rand_ids_f)
    with open(os.path.join(merge_dir, 'valid.json'), 'w') as w:
        w.writelines(rand_dat)
