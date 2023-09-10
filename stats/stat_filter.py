#!/bin/env python3
import os
import sys
import json

import argparse
import numpy as np
import scipy.stats as stats

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

def round_f(acc):
    return round (acc * 100, 5)

def load(f_good, f_label, f_pred):
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
    return labels, goodss, predss    

def cal_confident(dict):
    for tac, stat in dict.items():
        correct = [1] * (stat['TP'] + stat['TN'])
        wrong = [0] * (stat['FP'] + stat['FN'])
        dat = correct + wrong
        # stats.norm.interval(alpha=0.95,
        #          loc=np.mean(dat),
        #          scale=stats.sem(dat))
        # dict[tac]['95confident'] =stats.norm.interval(alpha=0.95, loc=np.mean(dat), scale=stats.sem(dat))
        neg = stat['FN'] + stat['TN']
        if neg == 0:
            dict[tac]['false_neg'] = 0
        else:
            dict[tac]['false_neg'] = stat['FN'] / (stat['FN'] + stat['TN'])

    return dict

def stat(f_good, f_label, f_pred):
    labels, goodss, predss = load(f_good, f_label, f_pred)

    tac_stats = {}
    false_pos = 0
    false_neg = 0
    n_label = 0
    n_in_pred = 0
    row_i = 0
    for goods, label, preds in zip(goodss, labels, predss):
        if utils.not_lemma(label):
            n_label += 1
            # print(label, goods)
            preds = preds[:10]
            for p in preds:
                if p not in tac_stats.keys():
                    tac_stats[p] = {'num': 1, 'TP' : 0, 'TN' : 0, 'FP' : 0, 'FN' : 0}
                else:
                    tac_stats[p]['num'] += 1
                    
                is_good = p in goods
                is_correct = (p == label)
                if is_good & is_correct:
                    tac_stats[p]['TP'] += 1
                elif is_good & (not is_correct):
                    tac_stats[p]['FP'] += 1
                elif (not is_good) & (not is_correct):
                    tac_stats[p]['TN'] += 1
                else:
                    tac_stats[p]['FN'] += 1    
            if label in preds:
                n_in_pred += 1
                if label not in goods:
                    false_neg += 1
            bad = [g != label for g in goods]
            false_pos += len(bad)
        row_i += 1

    items = tac_stats.items()
    tac_stats = dict(sorted(items, key=lambda x:x[1]['num'], reverse= True))
    # confident = cal_confident(confident)
    # print(confident)
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
        # 'confident' : confident,
    }
    log = log | tac_stats
    # for tac, stat in tac_stats.ite
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
