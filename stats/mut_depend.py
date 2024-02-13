import json

depend_file='stats/dependencies'
out='stats/depend.json'
def path2theory(p):
    return p.split('/')[1]


def load_depend(f):
    file_dp_dic = {}
    theory_dp_dic = {}
    r = open(f, 'r')
    for l in r:
        splits = l.split(':')
        depends = splits[1].split()
        file = splits[0]
        theory = path2theory(splits[0])
        dp_theories = [path2theory(x) for x in depends]

        dp_theories = set([x for x in dp_theories if x != theory])
        file_dp_dic[file] = depends
        if theory not in theory_dp_dic.keys():
            theory_dp_dic[theory] = dp_theories
        else:
            theory_dp_dic[theory] = theory_dp_dic[theory].union(dp_theories)
    return file_dp_dic, theory_dp_dic

def cal_mut_dp_theories(theory_dp_dic):
    mut_dp_dic = {}
    for theory, dps in theory_dp_dic.items():
        mut_dps = [d for d in dps if theory in theory_dp_dic[d]]
        if mut_dps != []:
            mut_dp_dic[theory] = mut_dps
    return mut_dp_dic

def cal_mut_depend_files(dp_files, mut_dps):
    mut_files = []
    for f in dp_files:
        # print(f)
        theory = path2theory(f)
        if theory in mut_dps:
            mut_files.append(f)
    return mut_files

def check_mut_file_dps(file_dp_dic, mut_dp_dic):
    for file, dps in file_dp_dic.items():
        theory = path2theory(file)
        if theory in mut_dp_dic.keys():
            mut_dps = mut_dp_dic[theory]
            mut_depend_fs = cal_mut_depend_files(dps, mut_dps)
            if mut_depend_fs != []:
                print(f'{file} mututally depends on {mut_depend_fs}')

        # dp_theories = cal_dp_theories(files_dps)
        # for file, dps in files_dps.items():
        #     if theory in dic[dp_theory].keys():
        #         if ((dp_theory, theory) not in mutual) & ((theory, dp_theory) not in mutual):
        #             print(f'{theory} mutually depend {dp_theory}')
        #             print(f'{theory} depends on {dp_theorys[dp_theory]}')
        #             print(f'{dp_theory} depends on {dic[dp_theory][theory]}')
        #             print('================')
        #             mutual.append((dp_theory, theory))
file_dp_dic, theory_dp_dic = load_depend(depend_file)
# check_mut(depend_dic)
mut_dp_dic = cal_mut_dp_theories(theory_dp_dic)
# print(mut_dp_dic)
check_mut_file_dps(file_dp_dic, mut_dp_dic)