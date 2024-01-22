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


def mk_acc_df(dat, ilp_stat, knn_stat, theory):
    for predc, predc_stat in ilp_stat["acc"].items():
        acc = predc_stat[theory]
        for i in range(len(acc)):
            dat["method"].append(utils.kind_to_abs(predc) + '+kNN')
            dat["accuracy"].append(acc[i])
            dat["top-k"].append(i + 1)
            dat["theory"].append(to_theory_name(theory))
    acc = knn_stat[theory]
    for i in range(len(acc)):
        dat["method"].append("kNN")
        dat["accuracy"].append(acc[i])
        dat["top-k"].append(i + 1)
        dat["theory"].append(to_theory_name(theory))
    return dat

def plot_theories_acc(ilp_stat, knn_stat):
    df = {"method": [], "accuracy": [], "top-k": [], 'theory':[]}

    theories = [
        'plugins/rtauto',
        'theories/FSets',
        'theories/Wellfounded',
        'plugins/funind',
        'plugins/btauto',
        'plugins/nsatz',
        'theories/MSets'
    ]
    for theory in theories:
        df = mk_acc_df(df, ilp_stat, knn_stat, theory)
    df = pd.DataFrame(df)
    g = sns.FacetGrid(df, col="theory", hue="method",  col_wrap=4)
    # g.map(plot)
    # print(g)
    g.map(sns.lineplot, 'top-k', 'accuracy')
    g.add_legend()
    # sns.lineplot(data=df, x="top-k", y="acc", hue="method")
    plt.savefig(f"acc.pdf", bbox_inches='tight')

ilp_stat_f = "test.json"
ilp_stat = json.load(open(ilp_stat_f, "r"))
knn_stat_f = "stats/ortho/rev/no_same_complex/Structures/knn_theory_stat.json"
knn_stat = json.load(open(knn_stat_f, "r"))

plot_theories_acc(ilp_stat, knn_stat)
