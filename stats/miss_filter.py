import json

file = "/home/zhangliao/ilp_out_coq/ilp_out_coq/prop_stat.json"
r = open(file, "r")
stats = json.load(r)

for pos in stats.keys():
    for neg in stats[pos].keys():
        for split, st in stats[pos][neg].items():
            if st == []:
                print("pos", pos, "neg", neg, "split", split)
