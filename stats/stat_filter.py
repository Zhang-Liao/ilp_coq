#!/bin/env python3
import os
import sys
import json

import argparse

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

def round_f(acc):
    return round (acc * 100, 5)

def stat(f_good, f_label, f_pred):
    with open(f_label, 'r') as f:
        labels = f.read().splitlines()
    labels = [l.strip() for l in labels]

    with open(f_good, 'r') as f:
        goodss = f.read().splitlines()
    goodss = [l.strip().split('\t') for l in goodss]

    with open(f_pred, 'r') as f:
        predss = f.read().splitlines()
    predss = [l.strip().split('\t') for l in predss]

    assert len(goodss) == len(labels)
    false_neg_tac = {}
    truth_pos_tac = {}
    false_pos = 0
    false_neg = 0
    n_label = 0
    n_in_pred = 0
    for goods, label, preds in zip(goodss, labels, predss):
        if utils.not_lemma(label):
            n_label += 1
            # print(label, goods)
            preds = preds[:10]
            if label in preds:
                n_in_pred += 1
                if label not in goods:
                    false_neg += 1
                    if label not in false_neg_tac.keys():
                        false_neg_tac[label] = 1
                    else:
                        false_neg_tac[label] += 1
                else:
                    if label not in truth_pos_tac.keys():
                        truth_pos_tac[label] = 1
                    else:
                        truth_pos_tac[label] += 1  
            bad = [g != label for g in goods]
            false_pos += len(bad)

    items = false_neg_tac.items()
    false_neg_tac = dict(sorted(items, key=lambda x:x[1], reverse= True))

    items = truth_pos_tac.items()
    truth_pos_tac = dict(sorted(items, key=lambda x:x[1], reverse= True))

    print('false neg', false_neg)
    print('n_in_pred', n_in_pred)
    false_neg = round_f(false_neg / n_in_pred)
    false_pos = round_f(false_pos / (n_label * 10))
    print('number of labels', n_label)
    print(f"false_neg: {false_neg}%")
    print(f"false_pos: {false_pos}%")
    log = {
        'false_neg' : false_neg,
        'false_pos' : false_pos,
        'false_neg_tac' : false_neg_tac,
        'truth_pos_tac' : truth_pos_tac
    }
    out_dir = os.path.dirname(f_good)
    with open(os.path.join(out_dir, 'stat_filter.json'), 'w') as w:
        json.dump(log, w, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="Returns false positive and false negative.")
    parser.add_argument('--good', type=str)
    parser.add_argument('--pred', type=str)
    parser.add_argument('--label', type=str)
    args = parser.parse_args()
    stat(args.good, args.label, args.pred)
