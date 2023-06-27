# import shutil
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--f", type=str, help = 'The file that contains the labels of the training dataset.' )
opts = parser.parse_args()
root, ext = os.path.splitext(opts.f)
assert (ext == '.label')

dict = {}
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