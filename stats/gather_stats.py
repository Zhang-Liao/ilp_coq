import json
import os
import re

num_of_test = 10
test_dir = (
    "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/2percent_split"
)


def inti_stat():
    stat = {}
    pos = [2, 4, 8, 16, 32]
    neg = [1, 2, 4, 8, 16, 32]
    split = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for p in pos:
        stat[p] = {}
        for n in neg:
            stat[p][n] = {}
            for s in split:
                stat[p][n][s] = []
    return stat


def update_stats(stat, pos, neg, split, acc):
    stat[int(pos)][int(neg)][split].append(acc)
    return stat


stat = inti_stat()
for i in range(num_of_test):
    test_i = os.path.join(test_dir, f"test{i}")

    pred = os.path.join(test_dir, f"test{i}.eval")
    label = os.path.join(test_dir, f"test{i}.label")

    for test_time in os.listdir(test_i):
        curr_dir = os.path.join(test_i, test_time)

        f_reorder = os.path.join(curr_dir, f"reorder/test{i}_stat.json")
        with open(f_reorder, "r") as r:
            reorder = json.load(r)
            info = re.match(
                r".*/p(?P<pos>[0-9]+)n(?P<neg>[0-9]+)/.*",
                reorder["info"],
            ).groupdict()
            stat = update_stats(stat, info["pos"], info["neg"], i, reorder["accs"])

print(stat)
