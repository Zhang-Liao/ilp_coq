import json
import os

f_rule = '/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/log/prop_tacs.json'
out = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/rules/prop'
tac = 'simpl'
f_tac2id = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/tac2id.json'

with open(f_rule, 'r') as r:
    rule_d = json.load(r)

with open(f_tac2id, 'r') as r:
    tac2id = json.load(r)

tacid = tac2id[tac]

rules = rule_d[tac]
rule_ids = zip(rules, range(len(rules)))
rules = [f'tac(A, \"{tac}\", {i}) :- {b}\n' for b, i in rule_ids]
f_w = os.path.join(out, f'{tacid}.pl') 
with open(f_w, 'w') as w:
    w.write(":- style_check(-singleton).\n")    
    w.writelines(rules)