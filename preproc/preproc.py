# import shutil
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)
opts = parser.parse_args()

input = opts.file
base  = os.path.splitext(input)[0]
f_feat = os.path.splitext(input)[0] + ".feat"
f_label = os.path.splitext(input)[0] + ".label"

def mk_feat(f):
    return (" ".join([str(feat) for (feat, _num) in f]))
    # return (" ".join(["%s:%s" % (feat, num) for (feat, num) in f]))

if os.path.exists(f_feat):
    os.remove(f_feat)
if os.path.exists(f_label):
    os.remove(f_label)

with (
    open(input, 'r') as reader,
    open(f_feat, 'a') as w_feat,
    open(f_label, 'a') as w_label):
    for l in reader:
        l = l.strip()
        if utils.notlemma(l):
            l = json.loads(l)
            feat = mk_feat(l['feats'])
            w_feat.write(feat + '\n')
            w_label.write(l['tac'] + '\n')
        else:
            w_feat.write(l + '\n')
            w_label.write(l + '\n')