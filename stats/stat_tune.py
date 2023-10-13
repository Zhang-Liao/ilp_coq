import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def aver(dat):
    # df_dat = {}
    dat_mat = []
    params = []
    for pos in dat.keys():
        for neg in dat[pos].keys():
            accs = list(dat[pos][neg].values())
            accs = [a[0] for a in accs]
            accs = np.array(accs)
            aver = np.average(accs, axis=0)
            dat_mat.append(aver)
            params.append(f"p{pos}n{neg}")
            # df_dat[f"p{pos}n{neg}"] = aver
        # df = pd.DataFrame(df_dat)
    dat_mat = np.array(dat_mat)
    # rows = np.transpose(rows)
    return dat_mat, params


def rank(dat_mat):
    num_rows, num_cols = dat_mat.shape
    for i in range(num_cols):
        column = dat_mat[:, i]
        # for r in dat_mat:
        sort_r = sorted(column, reverse=True)
        dat_mat[:, i] = [sort_r.index(x) for x in column]
    return np.ndarray.tolist(dat_mat)


def mK_df(dat, params):
    # assert (len(dat) == len(params))
    dic = {"topk": [], "rank among params": [], "param": []}
    for accs, param in zip(dat, params):
        for i in range(len(accs)):
            dic["topk"].append(i)
            dic["rank among params"].append(accs[i])
            dic["param"].append(param)
    df = pd.DataFrame(data=dic)
    return df


r = open("/home/zhangliao/ilp_out_coq/ilp_out_coq/rel_stat.json")
dat = json.load(r)

rows, params = aver(dat)
rows = rank(rows)
df = mK_df(rows, params)
ax = sns.lineplot(data=df, x="topk", y="rank among params", hue="param")
# plt.show()
plt.savefig("stats/rel_tune.pdf")
