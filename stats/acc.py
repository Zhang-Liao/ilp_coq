#!/bin/env python3
import os
import json

import argparse


def cal_k(preds, label):
    for i in range(len(preds)):
        if preds[i] == label:
            return i + 1
    return -1


def round_acc(acc):
    return round(acc * 100, 3)


def cal_accs(ranks, total):
    accs = []
    for i in range(100):
        num = len([r for r in ranks if (r <= i + 1) & (r != -1)])
        acc = round_acc(num / total)
        accs.append(acc)
    return accs


def acc(pred, f_label):
    with open(pred, "r") as f:
        lines1 = f.read().splitlines()
    lines1 = [l.strip().split("\t") for l in lines1]

    with open(f_label, "r") as f:
        lines2 = f.read().splitlines()
    lines2 = [l.strip() for l in lines2]

    assert len(lines1) == len(lines2)

    ranks = []
    for preds, label in zip(lines1, lines2):
        if not label.startswith("#lemma"):
            k = cal_k(preds, label)
            ranks.append(k)

    total = len(ranks)
    accs = cal_accs(ranks, total)
    print("total", total)
    print(f"acc: {accs}")

    log = {"acc": accs, "test": f_label}
    stat = os.path.splitext(pred)[0] + "_stat.json"
    with open(stat, "w") as w:
        json.dump(log, w, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns percentage of matching lines from two files."
    )
    parser.add_argument("--pred", type=str)
    parser.add_argument("--label", type=str)
    args = parser.parse_args()
    acc(args.pred, args.label)
