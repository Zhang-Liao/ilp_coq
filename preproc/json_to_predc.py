import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting

pos_neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/1000_neg.json'
json_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/1000.json'
bk_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl_bk.pl'
pos_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl_pos.pl'
neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl_neg.pl'

def idx_str(idx):
    idx = ",".join(idx)
    idx = "[" + idx +"]"
    return idx

def hyps_predc(i, l, writer):
    for ident, name, idx in l:
        writer.write("{}({},{},{}).\n".format(ident, i, name, idx_str(idx)))

def goal_predc(i, l, writer):
    for ident, idx in l:
        writer.write("{}({},{}).\n".format(ident, i, idx_str(idx)))

def output(kind, pos_neg, out):
    with (
        open(json_file, 'r') as reader,
        open(out, 'a') as writer):
        i = 0
        for l in reader:
            l = l.strip()
            if global_setting.lemma_delimiter not in l:
                l = json.loads(l)
                if (kind == 'pos') & (i in pos_neg['pos']):
                    hyps_predc(i, l['hyps'], writer)
                    goal_predc(i, l['goal'], writer)
                elif (kind == 'neg') & (i in pos_neg['neg']):
                    hyps_predc(i, l['hyps'], writer)
                    goal_predc(i, l['goal'], writer)
                i += 1            
    
with open(pos_neg_file, 'r') as r:
    pos_neg_dict = json.load(r) 
    pos_neg = pos_neg_dict['simpl']

if os.path.exists(bk_file):
    os.remove(bk_file)

if os.path.exists(pos_file):
    os.remove(pos_file)

if os.path.exists(neg_file):
    os.remove(neg_file)
    
output('pos', pos_neg, pos_file)
output('neg', pos_neg, neg_file)
