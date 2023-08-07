#!/bin/env python3
import os
import json

import argparse

parser = argparse.ArgumentParser(
    description="Returns percentage of matching lines from two files.")
parser.add_argument('--train', type=str, default = None)
parser.add_argument('--pred', type=str)
parser.add_argument('--label', type=str)
args = parser.parse_args()

def cal_k(preds, label):
    for i in range(len(preds)):
        if preds[i] == label:
            return i + 1
    return -1

def round_acc(acc):
    return round (acc * 100, 3)

with open(args.pred, 'r') as f:
    lines1 = f.read().splitlines()
lines1 = [l.strip().split('\t') for l in lines1]

with open(args.label, 'r') as f:
    lines2 = f.read().splitlines()
lines2 = [l.strip() for l in lines2]

assert len(lines1) == len(lines2)

ranks = []
for preds, label in zip(lines1, lines2):
    if not label.startswith('#lemma'):
        k = cal_k(preds, label)
        ranks.append(k)


total = len(ranks)
top1 = round_acc(len([r for r in ranks if r == 1]) / total)
top10 = round_acc(len([r for r in ranks if (r <= 10) & (r != -1)]) / total)
print('total', total)
print("Top1 acc: {:.3f}%".format(top1))
print("Top10 acc: {:.3f}%".format(top10))

log = {
    'top1': top1,
    'top10': top10,
    'train': args.train,
    'test' : args.label
}
out_dir = os.path.dirname(args.pred)
with open(os.path.join(out_dir, 'log.json'), 'w') as w:
    json.dump(log, w, indent=4)

