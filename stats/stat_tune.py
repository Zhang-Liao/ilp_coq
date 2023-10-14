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


def mK_f1_df(dat, params):
    # assert (len(dat) == len(params))
    # dic = {"param": params, "f1": []}
    f1s = []
    for pos in dat.values():
        for neg in pos.values():
            avg_f1 = np.mean(list(neg.values()))
            # avg_f1 = np.mean([f1 for f1 in neg.values()])
            f1s.append(avg_f1)
    print(f1s, len(f1s))
    print(params, len(params))

    dic = {"param": params, "f1": f1s}
    df = pd.DataFrame(data=dic)
    return df


def stat_f1(dat, params):
    df = mK_f1_df(dat, params)
    print(df)
    plt.figure(figsize=(20, 4.8))
    sns.barplot(data=df, x="param", y="f1", color="tab:blue", width=0.5)
    # plt.show()
    plt.savefig("stats/prop_tune.pdf")


r = open("/home/zhangliao/ilp_out_coq/ilp_out_coq/prop_stat.json")
dat = json.load(r)
params = get_params(dat["acc"])
# stat_acc(dat["acc"], params)
stat_f1(dat["f1"], params)
