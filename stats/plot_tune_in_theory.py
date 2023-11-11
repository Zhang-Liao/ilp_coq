import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def get_params(dat):
    params = []
    for pos in dat.keys():
        for neg in dat[pos].keys():
            params.append(f"p{pos}n{neg}")
    return params


def aver(dat):
    # df_dat = {}
    dat_mat = []
    for pos in dat.keys():
        for neg in dat[pos].keys():
            accs = list(dat[pos][neg].values())
            accs = [a[0] for a in accs]
            accs = np.array(accs)
            aver = np.average(accs, axis=0)
            dat_mat.append(aver)
    dat_mat = np.array(dat_mat)
    return dat_mat


def rank(dat_mat):
    num_rows, num_cols = dat_mat.shape
    for i in range(num_cols):
        column = dat_mat[:, i]
        # for r in dat_mat:
        sort_r = sorted(column, reverse=True)
        dat_mat[:, i] = [sort_r.index(x) for x in column]
    return np.ndarray.tolist(dat_mat)


def mK_acc_df(dat, params):
    # assert (len(dat) == len(params))
    dic = {"topk": [], "rank among params": [], "param": []}
    for accs, param in zip(dat, params):
        for i in range(len(accs)):
            dic["topk"].append(i)
            dic["rank among params"].append(accs[i])
            dic["param"].append(param)
    df = pd.DataFrame(data=dic)
    return df


def stat_acc(dat, params):
    rows = aver(dat)
    rows = rank(rows)
    df = mK_acc_df(rows, params)
    sns.lineplot(data=df, x="topk", y="rank among params", hue="param")
    # plt.show()
    plt.savefig("stats/rel_tune.pdf")


def stat_f1(df):
    # df = mk_f1_df(dat, params)
    # print(df)
    plt.figure(figsize=(24, 4.8))
    sns.lineplot(data=df, x="param", y="f1", hue="kind")
    # plt.show()
    plt.savefig("stats/tune_QArith_nontrivial_f1.pdf")


def mk_f1_df(stat, theory, name):
    # print(theory)
    # name = theory.split("/")[-1]
    dic = {"kind": [], "f1": [], "param": []}
    # print(stat.keys())
    # exit()
    for kind, kind_stat in stat.items():
        theory_stat = kind_stat[theory]
        for pos, pos_stat in theory_stat.items():
            for neg, f1 in pos_stat.items():
                dic["kind"].append(f"{kind}_{name}")
                dic["f1"].append(f1)
                dic["param"].append(f"p{pos}n{neg}")

    df = pd.DataFrame(data=dic)
    # print(df)
    return df


def mk_f1_dfs(stat, theories):
    dfs = []
    for theory in theories:
        name = theory.split("/")[-1]
        # dfs.append(mk_f1_df(stat["f1"], theory, name))
        dfs.append(mk_f1_df(stat["f1_no_ignored_tac"], theory, f"{name}_nontrivial"))
    return pd.concat(dfs)


f_stats = "tune_QArith.json"
reader = open(f_stats, "r")
stat = json.load(reader)
theories = ["theories/Lists"]
# theories = ["theories/Lists", "theories/Sorting", "aver"]
df = mk_f1_dfs(stat, theories)
stat_f1(df)
