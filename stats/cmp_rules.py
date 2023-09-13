import json
f1 = '/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/log/prop_tacs.json'
f2 = '/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/log/rel1_tacs.json'

with open(f1, 'r') as r:
    dct1 = json.load(r)
    
with open(f2, 'r') as r:
    dct2 = json.load(r)
    
new_rules = set(dct2['simpl']).difference(set(dct1['simpl']))
disappear_rules = set(dct1['simpl']).difference(set(dct2['simpl']))

print('new_rules', len(new_rules))
print('disappear_rules', len(disappear_rules))
