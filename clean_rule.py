import argparse
import re


def parse_tac(s):
    return s[7:][:-5]


def mk_rule_dic(dat):
    dct = {}
    is_hd = True
    for r in dat:
        r = r.strip()
        if r.startswith("tac(A,"):
            is_hd = True
            body = ""
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


parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)

opts = parser.parse_args()

with open(opts.file, "r") as r:
    dat = []
    for l in r:
        if not re.match("tac\(.+\)\.\n", l):
            dat.append(l)

assert dat[0] == ":- style_check(-singleton).\n"
dat = dat[1:]
rule_dic = sort_rules(mk_rule_dic(dat))

with open(opts.file, "w") as w:
    w.write(":- style_check(-singleton).\n")
    for tac, rules in rule_dic.items():
        for r in rules:
            w.write(f'tac(A,"{tac}") :-\n')
            w.write(f"    {r}\n")
