import glob
import os
import shutil

num_of_test = 10
test_dir = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets"

# for i in range(num_of_test):
i = 9
test_i = os.path.join(test_dir, f"test{i}", "subsum")

for test_time in os.listdir(test_i):
    curr_dir = os.path.join(test_i, test_time)
    good = os.path.join(curr_dir, f"good/test{i}.eval")
    if not os.path.exists(good):
        shutil.rmtree(curr_dir)
