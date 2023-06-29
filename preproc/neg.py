import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--feat", type=str)
parser.add_argument("--label", type=str)
parser.add_argument("--dict", type=str)

opts = parser.parse_args()

dict = json.loads(opts.dict)

i = 1
with open(opts.f, 'r') as reader:
    for l in reader:
        tac = l.strip()
        if global_setting.lemma_delimiter not in l:
            if tac not in dict.keys():
                dict[tac] = [i]
            else:
                dict[tac].append(i)
        i += 1
# print(dict)

out = root + "_tac.json"
with open(out, 'w') as w:
    json.dump(dict, w)  