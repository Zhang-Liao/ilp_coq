import json
import os
import re

num_of_test = 10
test_dir = "data/json/origin_feat/tune/MSets/"


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
    if len(stat[int(pos)][int(neg)][split]) > 1:
        assert False
    stat[int(pos)][int(neg)][split].append(acc)
    return stat


def check_miss(stats):
    for pos in stats.keys():
        for neg in stats[pos].keys():
            for split, st in stats[pos][neg].items():
                if st == []:
                    print("miss: pos", pos, "neg", neg, "split", split)


acc_stat = inti_stat()
f1_stat = inti_stat()
for i in range(num_of_test):
    stat_i = f"data/json/origin_feat/tune/MSets/test{i}/subsum/rel/anonym"
    # test_i = os.path.join(test_dir, f"test{i}", "subsum")
    pred = os.path.join(test_dir, f"test{i}.eval")
    label = os.path.join(test_dir, f"test{i}.label")

    for param in os.listdir(stat_i):
        # test_time = f"subsum/{test_time}"
        curr_dir = os.path.join(stat_i, param)
        f_ilp_stat = os.path.join(curr_dir, f"good/stat_filter.json")
        f_reorder = os.path.join(curr_dir, f"reorder/test{i}_stat.json")
        reorder_r = open(f_reorder, "r")
        reorder = json.load(reorder_r)
        try:
            info = re.match(r".*p(?P<pos>[0-9]+)n(?P<neg>[0-9]+).*", param)
        except:
            print("fail to match", param)
            exit()
        if info != None:
            info = info.groupdict()
            pos = info["pos"]
            neg = info["neg"]
            acc_stat = update_stats(acc_stat, pos, neg, i, reorder["accs"])
            ilp_r = open(f_ilp_stat, "r")
            ilp_stat = json.load(ilp_r)
            f1_stat = update_stats(f1_stat, pos, neg, i, ilp_stat["f1"])

stat = {"info": stat_i, "acc": acc_stat, "f1": f1_stat}
# print(stat)
check_miss(stat["f1"])
with open("rel_anonym_stat.json", "w") as w:
    json.dump(stat, w)
