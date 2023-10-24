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


def mk_f1_df(dat, params, predc):
    # assert (len(dat) == len(params))
    # dic = {"param": params, "f1": []}
    f1s = []
    for pos in dat.values():
        for neg in pos.values():
            avg_f1 = np.mean(list(neg.values()))
            # avg_f1 = np.mean([f1 for f1 in neg.values()])
            f1s.append(avg_f1)
    # print(f1s, len(f1s))
    # print(params, len(params))
    predcs = [predc] * len(f1s)
    dic = {"param": params, "f1": f1s, "predc": predcs}
    df = pd.DataFrame(data=dic)
    return df


def stat_f1(df):
    # df = mk_f1_df(dat, params)
    # print(df)
    plt.figure(figsize=(24, 4.8))
    sns.lineplot(data=df, x="param", y="f1", hue="predc")
    # plt.show()
    # plt.savefig("stats/f1_tune.pdf")


def mk_dfs(files):
    dfs = []
    for key, f in files:
        r = open(f, "r")
        dat = json.load(r)
        params = get_params(dat["f1"])
        df = mk_f1_df(dat["f1"], params, key)
        print(f)
        print(df.loc[df["f1"].idxmax()])
        dfs.append(df)
    return pd.concat(dfs)


f_stats = [
    (
        "prop_origin",
        "/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/alltac/prop_origin_stat.json",
    ),
    (
        "rel_origin",
        "/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/alltac/rel_origin_stat.json",
    ),
    (
        "rel_anonym",
        "/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/alltac/rel_anonym_stat.json",
    ),
]

df = mk_dfs(f_stats)
stat_f1(df)
# r_rel_origin = open("/home/zhangliao/ilp_out_coq/ilp_out_coq/rel_origin_stat.json")
# dat_rel_origin = json.load(r_rel_origin)
# params = get_params(dat_rel_origin["f1"])
# df_rel_origin = mk_f1_df(dat_rel_origin["f1"], params)
# stat_f1(df_rel_origin, params)
