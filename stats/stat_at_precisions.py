import json

import argparse


def init_rules(stat):
    rules = {}
    for tac in stat.keys():
        rules[tac] = []
    return rules


def filter_rules(f_stat):
    reader = open(f_stat, "r")
    stat = json.load(reader)
    good_rules = init_rules(stat["tactic"])
    for tac, tac_stat in stat["tactic"].items():
        for rule, rule_stat in tac_stat["rule"].items():
            if rule_stat["precision"] > 0.1:
                good_rules[tac].append(rule)
    print(good_rules)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns false positive and false negative."
    )
    parser.add_argument("--stat", type=str)
    # parser.add_argument("--pred", type=str)
    # parser.add_argument("--label", type=str)
    # parser.add_argument("--rule", type=str)
    args = parser.parse_args()
    filter_rules(args.stat)
