import glob
import os
import stat_filter

num_of_test = 10
test_dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets"

for i in range(num_of_test):
    test_i = os.path.join(test_dir, f"test{i}", "subsum")

    pred = os.path.join(test_dir, f"test{i}.eval")
    label = os.path.join(test_dir, f"test{i}.label")

    for test_time in os.listdir(test_i):
        try:
            curr_dir = os.path.join(test_i, test_time)
            # print(curr_dir)
            reorder = os.path.join(curr_dir, f"reorder/test{i}.eval")
            good = os.path.join(curr_dir, f"good/test{i}.eval")
            stat_filter.stat_ilp_stat_ml(good, label, pred, reorder, True)
        except FileNotFoundError:
            print("not find", curr_dir)
            continue
