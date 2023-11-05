import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def mk_f1_df(stat):
    dat = {"predc": [], "f1": [], "theory": []}
    for kind, kind_stat in stat["f1_no_ignored_tac"].items():
        for theory, theory_stat in kind_stat.items():
            theory = theory.split("/")[-1]
            # f1s = list(theory_stat.values())
            for f1 in theory_stat.values():
                dat["predc"].append(kind)
                dat["f1"].append(np.average(f1))
                dat["theory"].append(theory)
    df = pd.DataFrame(data=dat)
    return df


def mk_acc_df(ilp_stat, knn_stat, theory):
    dat = {"kind": [], "acc": [], "top-k": []}
    for predc, predc_stat in ilp_stat["acc"].items():
        for acc in predc_stat[theory].values():
            for i in range(len(acc)):
                dat["kind"].append(predc)
                dat["acc"].append(acc[i])
                dat["top-k"].append(i + 1)

    for acc in knn_stat[theory].values():
        for i in range(len(acc)):
            dat["kind"].append("knn")
            dat["acc"].append(acc[i])
            dat["top-k"].append(i + 1)

    return dat
    # for acc in knn_stat.values():
    #     for i in range(len(acc)):
    #         dat["kind"].append("knn")
    #         dat["acc"].append(acc[i])
    #         dat["top-k"].append(i + 1)


def plot_theories_acc(ilp_stat, knn_stat):
    for theory in utils.THEORIES:
        df = mk_acc_df(ilp_stat, knn_stat, theory)
        sns.lineplot(data=df, x="top-k", y="acc", hue="kind")
        # plt.show()
        theory_name = theory.split("/")[-1]
        plt.savefig(f"stats/alltac/acc_{theory_name}.pdf")
        plt.clf()
        # dfs.append(df)


ilp_stat_f = "stats/alltac/ilp_theory_stat.json"
knn_stat_f = "knn_theory_stat.json"
ilp_stat = json.load(open(ilp_stat_f, "r"))
knn_stat = json.load(open(knn_stat_f, "r"))

# f1_df = mk_f1_df(stat)
# sns.barplot(data=f1_df, x="theory", y="f1", hue="predc")
# plt.show()
# plt.savefig("stats/alltac/theory_stat_no_ignored.pdf")
plot_theories_acc(ilp_stat, knn_stat)
