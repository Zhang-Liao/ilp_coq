import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def to_theory_name(theory):
    return theory.split("/")[-1]


def mk_f1_df(stat):
    dat = {"predc": [], "f1": [], "theory": []}
    for kind, kind_stat in stat["f1"].items():
        for theory, f1 in kind_stat.items():
            # f1 = kind_stat[theory].items()
            dat["predc"].append(kind)
            dat["f1"].append(f1)
            dat["theory"].append(to_theory_name(theory))
    df = pd.DataFrame(data=dat)
    return df


def mk_acc_df(ilp_stat, knn_stat, theory):
    dat = {"kind": [], "acc": [], "top-k": []}
    for predc, predc_stat in ilp_stat["acc"].items():
        acc = predc_stat[theory]
        for i in range(len(acc)):
            dat["kind"].append(predc)
            dat["acc"].append(acc[i])
            dat["top-k"].append(i + 1)
    acc = knn_stat[theory]
    # for acc in knn_stat[theory]:
    for i in range(len(acc)):
        dat["kind"].append("knn")
        dat["acc"].append(acc[i])
        dat["top-k"].append(i + 1)

    return dat

def plot_theories_acc(ilp_stat, knn_stat):
    theories = [
        "theories/Sorting",
        "theories/NArith",
        "theories/Init",
        "theories/Vectors",
        "plugins/setoid_ring",
    ]

    for theory in theories:
        df = mk_acc_df(ilp_stat, knn_stat, theory)
        sns.lineplot(data=df, x="top-k", y="acc", hue="kind")
        # plt.show()
        theory_name = theory.split("/")[-1]
        plt.savefig(f"acc_{theory_name}.pdf", bbox_inches='tight')
        plt.clf()
        # dfs.append(df)

ilp_stat_f = "stats/ortho/new_const/noident/ListsLogic/QArith_ListsLogic_test.json"
ilp_stat = json.load(open(ilp_stat_f, "r"))
knn_stat_f = "stats/knn_theory_stat.json"
knn_stat = json.load(open(knn_stat_f, "r"))

# f1_df = mk_f1_df(ilp_stat)
# sns.barplot(data=f1_df, x="theory", y="f1", hue="predc")
# plt.show()
# plt.savefig("stats/ortho/test.pdf")
plot_theories_acc(ilp_stat, knn_stat)
