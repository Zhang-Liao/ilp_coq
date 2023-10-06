import os
import json

num_of_test = 10
test_dir = (
    "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/2percent_split"
)

accs = []
for i in range(num_of_test):
    test_i = os.path.join(test_dir, f"test{i}")

    pred = os.path.join(test_dir, f"test{i}.eval")
    label = os.path.join(test_dir, f"test{i}.label")

    for test_time in os.listdir(test_i):
        curr_dir = os.path.join(test_i, test_time)

        f_reorder = os.path.join(curr_dir, f"reorder/test{i}_stat.json")
        with open(f_reorder, "r") as r:
            reorder = json.load(r)
            if "/p16n32/" in reorder["info"]:
                accs.append(reorder["accs"])
print(accs)
