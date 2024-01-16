import json

depend_file='stats/dependencies'
out='stats/depend.json'
def path2theory(p):
    return p.split('/')[1]

def load_depend(f):
    depend_dic = {}
    r = open(f, 'r')
    for l in r:
        splits = l.split(':')
        depends = splits[1].split()
        depends = [path2theory(x) for x in depends]
        theory = path2theory(splits[0])
        depends = set([x for x in depends if x != theory])
        # depends = set(depends)
        # theory = splits[0]
        # depends = set([x for x in depends if x != theory])
        if theory not in depend_dic.keys():
            depend_dic[theory] = depends
        else:
            depend_dic[theory] =  depend_dic[theory].union(depends)
    return depend_dic

def closure(depend_dic):
    new_depend_dic = {}
    for theory, parents in depend_dic.items():
        depends = parents
        new_depends = parents
        first = True
        while first | (new_depends != depends):
            depends = new_depends
            for d in depends:
                futher_depends = depend_dic[d]
                new_depends = new_depends.union(futher_depends)
            first = False
        depends = [x for x in depends if x != theory]
        new_depend_dic[theory] = list(depends)
    return new_depend_dic

def gather_by_theory(dic):
    # theory = 'theories/QArith'
    t_depends = set()
    for file, depends in dic.items():
        t_depends = t_depends.union(depends)
    t_depends = sorted(t_depends)
    # print(t_depends)
    return t_depends

depend_dic = load_depend(depend_file)
depend_dic = closure(depend_dic)
# depends = gather_by_theory(depend_dic)
w = open(out, 'w')
json.dump(depend_dic, w, indent=4)
# print(depend_dic)