import json
import os

num_of_test = 10
test_dir = "data/json/origin_feat/rand_lines"

accs = {}

for i in range(num_of_test):
    f_test = os.path.join(test_dir, f"valid{i}_stat.json")
    reader = open(f_test, "r")
    stat = json.load(reader)
    accs[i] = stat["accs"]

writer = open("stats/knn_split.json", "w")
json.dump(accs, writer)
print(accs)
