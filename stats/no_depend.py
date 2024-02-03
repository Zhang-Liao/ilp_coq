import json
import random
depend_f = 'stats/depend.json'
test = set(['rtauto', 'FSets', 'Wellfounded', 'funind', 'btauto', 'MSets', 'nsatz'])
reader = open(depend_f, 'r')
depend_dic = json.load(reader)

for theory, depends in depend_dic.items():
    depends = set(depends)
    if test.intersection(depends) == set():
        if theory not in test:
            print(theory)

# theories = set(theory_dic.keys())
# depends = set(theory_dic['MSets'])
# no_depends = list(theories.difference(depends))
# random.shuffle(no_depends)
# print(no_depends)

# QArith # do not depend ['rtauto', 'ltac', 'FSets', 'derive', 'Wellfounded', 'funind', 'btauto', 'MSets', 'nsatz', 'Ltac2', 'Compat']
# QArith ['rtauto', 'FSets', 'Wellfounded', 'funind', 'btauto', 'MSets', 'nsatz']

# QArith ['Wellfounded', 'funind' (very small), 'btauto', 'MSets', 'nsatz']

# do not depend
# rtauto ['MSets', 'Wellfounded', 'rtauto', 'Compat', 'FSets', 'btauto', 'Ltac2', 'nsatz', 'ltac', 'funind', 'derive']

# Logic ['funind', 'rtauto', 'btauto', 'MSets', 'Compat', 'Ltac2', 'derive', 'Wellfounded', 'FSets', 'nsatz', 'ltac']

# ZArith ['nsatz', 'derive', 'FSets', 'Wellfounded', 'btauto', 'MSets', 'Compat', 'ltac', 'Ltac2', 'rtauto', 'funind']

# Classes ['derive', 'Compat', 'ltac', 'funind', 'MSets', 'Wellfounded', 'rtauto', 'btauto', 'FSets', 'nsatz', 'Ltac2']

# FSets ['btauto', 'derive', 'Wellfounded', 'nsatz', 'ltac', 'rtauto', 'Ltac2', 'Compat']

# MSet ['ltac', 'Compat', 'derive', 'nsatz', 'btauto', 'rtauto', 'Ltac2', 'Wellfounded']
