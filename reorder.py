import argparse
import json
import os

from lib import utils
from stats import acc

def load(good_f, pred_f):
    with open(pred_f, "r") as f:
        predss = f.read().splitlines()

    with open(good_f, "r") as f:
        goodss = f.read().splitlines()

    return goodss, predss

def reorder(good_f, pred_f, label_f):
    reorders = []
    goodss, predss = load(good_f, pred_f)
    for goods, preds in zip(goodss, predss):
        if utils.not_lemma(preds):
            preds = preds.strip().split("\t")
            goods = list(json.loads(goods).keys()) 
            # goods_set = set(goods)
            reorder = goods + [x for x in preds if x not in goods]
            reorder = '\t'.join(reorder)
            reorders.append(reorder)
        else:
            reorders.append(preds)   
    dir = os.path.split(os.path.split(good_f)[0])[0]
    name = os.path.basename(good_f)
    reorder_dir = os.path.join(dir, 'reorder')
    os.makedirs(reorder_dir, exist_ok = True)
    reorder_f = os.path.join(reorder_dir, name)
    with open(reorder_f, 'w') as w:
        w.writelines([x + '\n' for x in reorders])
    acc.acc(reorder_f, label_f)
    
# parser = argparse.ArgumentParser()
# parser.add_argument("--good", type=str)
# parser.add_argument("--pred", type=str)
# parser.add_argument("--label", type=str)

# opts = parser.parse_args()
# reorder(opts.good, opts.pred, opts.label)