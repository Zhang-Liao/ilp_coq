import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting

pos_neg_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/1000_neg.json'
json_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/1000.json'
bk_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl_bk.pl'
pos_neg_prolog_file = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/simpl_pn.pl'
tac = 'simpl'
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

def pr_bk(pos_neg, out):
    with (
        open(json_file, 'r') as reader,
        open(out, 'a') as writer):
        i = 0
        for l in reader:
            l = l.strip()
            if global_setting.lemma_delimiter not in l:
                if i in pos_neg:
                    l = json.loads(l)
                    hyps_predc(i, l['hyps'], writer)
                    goal_predc(i, l['goal'], writer)
                i += 1            

def pr_predc(pos, neg, out):
    with open(out, 'a') as writer:
        writer.write(":-begin_in_pos.\n")    
        for p in pos:
            writer.write("{}({})\n".format(tac,p))
        writer.write(":-end_in_pos.\n")                
        writer.write(":-begin_in_neg.\n")   
        for n in neg:
            writer.write("{}({})\n".format(tac,n))
        writer.write(":-end_in_neg.\n")   



with open(json_file, 'r') as r:
    pos_neg_dict = json.load(r) 
    tac_pos_neg = pos_neg_dict[tac]
    pos_neg = tac_pos_neg['pos'] + tac_pos_neg['neg']

if os.path.exists(bk_file):
    os.remove(bk_file)

if os.path.exists(pos_neg_prolog_file):
    os.remove(pos_neg_prolog_file)
        
pr_bk(pos_neg, bk_file)
pr_predc(tac_pos_neg['pos'], tac_pos_neg['neg'], pos_neg_prolog_file)