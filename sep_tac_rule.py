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
for i in range(len(rules)):
    f_w = os.path.join(out, f'{tacid}_n{i}.pl')
    body = rules[i]
    rule = f'tac(A, \"{tac}\") :- {body}'
    with open(f_w, 'w') as w:
        w.write(rule)