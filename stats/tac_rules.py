import json

file = "data/json/predicate/rand_train_test/train/prop/5k/train0/alltac_rule.pl"
out = '/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/log/prop_tacs.json'

def parse_tac(s):
    return s[7:][:-5]


def rule_dct(dat):
    dct = {}
    is_hd = True
    for r in dat:
        r = r.strip()
        if r.startswith("tac(A,"):
            is_hd = True
            body = ''
        if is_hd:
            hd = parse_tac(r)
            is_hd = False
        else:
            body += r

        if r.endswith("."):
            if hd not in dct.keys():
                dct[hd] = [body]
            else:
                dct[hd].append(body)

    return dct

def sort_rules(dct):
    for tac, rules in dct.items():
        rules = list(set(rules))
        rules.sort()
        dct[tac] = rules
    return dct

with open(file, "r") as r:
    dat = r.readlines()[1:]

dct = sort_rules(rule_dct(dat))


with open(out , 'w') as w:
    json.dump(dct, w, indent= 4)