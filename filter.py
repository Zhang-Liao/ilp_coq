import copy
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

from pyswip import Prolog

from lib import global_setting

clause_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/'
pred_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/test.pred'
example_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/'

def read_cls_paths():
    cls_paths = {}
    rule_suffix = '.rule.pl'
    for filename in os.listdir(clause_dir):
        if filename.endswith(rule_suffix):
            tac = filename.removesuffix(rule_suffix)
            cls_paths[tac] = os.path.join(clause_dir, filename)
            # break
    return cls_paths

def read_exg_paths():
    exg_paths = {}
    pl_suffix = '.pl'
    for filename in os.listdir(example_dir):
        if filename.endswith(pl_suffix):
            # Ensure the name of the file only contains intergers.
            try:
                exg = int(filename.removesuffix(pl_suffix))
            except:
                continue
            exg_paths[exg] = os.path.join(example_dir, filename)
    return exg_paths

def filter_row(i, r, exg_paths, cls_paths):
    new_preds = []
    preds = r.split()
    for p in preds:
        prolog = Prolog()
        prolog.consult(exg_paths[i])
        prolog.consult(cls_paths[p])
        # query fail if return []
        if list(prolog.query(f'tac({i})')) != []:
            new_preds.append(p)
    print(new_preds)
    return new_preds


def filter(exg_paths, cls_paths):
    i = 0
    with open(pred_file, 'r') as f:
        for r in f:
            if global_setting.lemma_delimiter not in r :
                r = r.strip()
                filter_row(i, r, exg_paths, cls_paths)
            i += 1

exg_paths = read_exg_paths()
print('exg_paths', exg_paths)
cls_paths = read_cls_paths()
filter(exg_paths, cls_paths)
