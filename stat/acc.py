#!/bin/env python3
import argparse

parser = argparse.ArgumentParser(
    description="Returns percentage of matching lines from two files.")
parser.add_argument('--pred', type=str)
parser.add_argument('--label', type=str)
args = parser.parse_args()

with open(args.pred, 'r') as f:
    lines1 = f.read().splitlines()
lines1 = [l.strip().split('\t') for l in lines1]

with open(args.label, 'r') as f:
    lines2 = f.read().splitlines()
lines2 = [l.strip() for l in lines2]

assert len(lines1) == len(lines2)

def cal_k(preds, label):
    for i in range(len(preds)):
        if preds[i] == label:
            return i + 1
    return -1

ranks = []
for preds, label in zip(lines1, lines2):
    if not label.startswith('#lemma'):
        k = cal_k(preds, label)
        ranks.append(k)

total = len(ranks)
top1 = len([r for r in ranks if r == 1])
top10 = len([r for r in ranks if (r <= 10) & (r != -1)])
print('total', total)
print("Top1 acc: {:.2f}%".format((top1/total) * 100))
print("Top10 acc: {:.2f}%".format(top10/total * 100))