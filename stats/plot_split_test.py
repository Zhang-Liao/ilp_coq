import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

knn_acc = []


def mk_f1_df(stat):
    dat = {"predc": [], "f1": []}
    for predc, predc_stat in stat["f1"].items():
        for _, f1 in predc_stat.items():
            dat["predc"].append(predc)
            dat["f1"].append(f1)
    df = pd.DataFrame(data=dat)
    return df


def mk_acc_df(ilp_stat, knn_stat):
    dat = {"kind": [], "acc": [], "top-k": []}
    for predc, predc_stat in ilp_stat["acc"].items():
        for acc in predc_stat.values():
            for i in range(len(acc)):
                dat["kind"].append(predc)
                dat["acc"].append(acc[i])
                dat["top-k"].append(i + 1)
    for acc in knn_stat.values():
        for i in range(len(acc)):
            dat["kind"].append("knn")
            dat["acc"].append(acc[i])
            dat["top-k"].append(i + 1)

    # for
    df = pd.DataFrame(data=dat)
    return df


f_ilp = "stats/alltac/split_test_stat.json"
f_knn = "stats/alltac/knn_split.json"
ilp_stat = json.load(open(f_ilp, "r"))
knn_stat = json.load(open(f_knn, "r"))
# f1_df = mk_f1_df(stat)
# sns.barplot(data=f1_df, x="predc", y="f1")
# plt.savefig("stats/alltac/f1_split_test_stat.png")

acc_df = mk_acc_df(ilp_stat, knn_stat)
sns.lineplot(data=acc_df, x="top-k", y="acc", hue="kind")
# plt.show()
plt.savefig("stats/alltac/acc_split_test_stat.pdf")
