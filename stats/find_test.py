import json
import os
import re

num_of_test = 10
test_dir = "data/json/origin_feat/tune/MSets"

for i in range(num_of_test):
    test_i = os.path.join(test_dir, f"test{i}")

    pred = os.path.join(test_dir, f"test{i}.eval")
    label = os.path.join(test_dir, f"test{i}.label")

    for test_time in os.listdir(test_i):
        curr_dir = os.path.join(test_i, test_time)
        f_log = os.path.join(curr_dir, f"log.json")
        reader = open(f_log, "r")
        reorder = json.load(reader)
        info = re.match(
            r".*/rel/p(?P<pos>[0-9]+)n(?P<neg>[0-9]+)/.*",
            reorder["clause"],
        )
        if info != None:
            info = info.groupdict()
            pos = int(info["pos"])
            neg = int(info["neg"])
            if (pos == 4) & (neg == 4):
                print("pos", pos, "neg", neg, 'split', i, "log", f_log)
