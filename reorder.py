import argparse
import functools
import json
import os



from lib import utils

def load(good_f, pred_f):
    with open(pred_f, "r") as f:
        predss = f.read().splitlines()
    # predss = [l.strip().split("\t") for l in predss]

    with open(good_f, "r") as f:
        goodss = f.read().splitlines()
    # goodss = [json.loads(l) for l in goodss]

    return goodss, predss

def reorder(good_f, pred_f):
    reorders = []
    goodss, predss = load(good_f, pred_f)
    for goods, preds in zip(goodss, predss):
        if utils.not_lemma(preds):
            preds = preds.strip().split("\t")
            goods = list(json.loads(goods).keys()) 
            goods_set = set(goods)
            reorder = goods + list(set(preds).difference(goods_set))
            reorder = '\t'.join(reorder)
            reorders.append(reorder)
        else:
            reorders.append(preds)   
    dir = os.path.split(os.path.split(good_f)[0])[0]
    name = os.path.basename(good_f)
    reorder_dir = os.path.join(dir, 'reorder')
    os.makedirs(reorder_dir, exist_ok = True)
    with open(os.path.join(reorder_dir, name), 'w') as w:
        w.writelines([x + '\n' for x in reorders])

parser = argparse.ArgumentParser()
parser.add_argument("--good", type=str)
parser.add_argument("--pred", type=str)

opts = parser.parse_args()
reorder(opts.good, opts.pred)


# /home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/QArith/test_theory/theories/Init/ListsLogic/prop_ident/anonym/p2n2/good/Init.eval
# /home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/QArith/test_theory/theories/Init.eval