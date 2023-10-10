import os
import json

import shutil

num_of_test = 10
test_dir = "data/json/origin_feat/tune/MSets"

for i in range(num_of_test):
    test_i = os.path.join(test_dir, f"test{i}")

    for test_time in os.listdir(test_i):
        curr_dir = os.path.join(test_i, test_time)

        f_reorder = os.path.join(curr_dir, f"reorder/test{i}_stat.json")
        with open(f_reorder, "r") as r:
            reorder = json.load(r)
            if "/rel/" in reorder["info"]:
                shutil.rmtree(curr_dir)
