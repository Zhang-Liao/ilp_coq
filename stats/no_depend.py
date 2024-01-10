import json
import random
depend_f = 'depend_theory.json'
reader = open(depend_f, 'r')
theory_dic = json.load(reader)
theories = set(theory_dic.keys())
depends = set(theory_dic['FSets'])
no_depends = list(theories.difference(depends))
# random.shuffle(no_depends)
print(no_depends)

# QArith ['rtauto', 'ltac', 'FSets', 'derive', 'Wellfounded', 'funind', 'btauto', 'MSets', 'nsatz', 'Ltac2', 'Compat']
# QArith ['rtauto', 'FSets', 'Wellfounded', 'funind', 'btauto', 'MSets', 'nsatz']

# QArith ['Wellfounded', 'funind' (very small), 'btauto', 'MSets', 'nsatz']

# rtauto ['MSets', 'Wellfounded', 'rtauto', 'Compat', 'FSets', 'btauto', 'Ltac2', 'nsatz', 'ltac', 'funind', 'derive']

# Logic ['funind', 'rtauto', 'btauto', 'MSets', 'Compat', 'Ltac2', 'derive', 'Wellfounded', 'FSets', 'nsatz', 'ltac']

# ZArith ['nsatz', 'derive', 'FSets', 'Wellfounded', 'btauto', 'MSets', 'Compat', 'ltac', 'Ltac2', 'rtauto', 'funind']

# Classes ['derive', 'Compat', 'ltac', 'funind', 'MSets', 'Wellfounded', 'rtauto', 'btauto', 'FSets', 'nsatz', 'Ltac2']

# FSets ['btauto', 'derive', 'Wellfounded', 'nsatz', 'ltac', 'rtauto', 'Ltac2', 'Compat']