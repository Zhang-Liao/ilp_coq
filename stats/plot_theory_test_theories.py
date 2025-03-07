import json
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.append(os.path.dirname(sys.path[0]))

def to_theory_name(theory):
    return theory.split("/")[-1]


def kind_to_abs(k):
    if k == 'anonym_feat':
        return 'AF'
    elif k == 'anonym_repr':
        return 'AR'
    elif k == 'origin_repr':
        return 'OR'
    elif k == 'origin_feat':
        return 'OF'

def mk_acc_df(dat, ilp_stat, knn_stat, theory):
    for predc, predc_stat in ilp_stat["acc"].items():
        acc = predc_stat[theory]
        for i in range(len(acc)):
            dat["Method"].append(kind_to_abs(predc) + '+kNN')
            dat["Accuracy"].append(acc[i])
            dat["Top-k"].append(i + 1)
            dat["Theory"].append(to_theory_name(theory))
    acc = knn_stat[theory]
    for i in range(len(acc)):
        dat["Method"].append("kNN")
        dat["Accuracy"].append(acc[i])
        dat["Top-k"].append(i + 1)
        dat["Theory"].append(to_theory_name(theory))
    return dat

def plot_theories_acc(ilp_stat, knn_stat):
    df = {"Method": [], "Accuracy": [], "Top-k": [], 'Theory':[]}

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
    g = sns.FacetGrid(df, col="Theory", hue="Method",  col_wrap=4)
    # g.map(plot)
    # print(g)
    g.map(sns.lineplot, 'Top-k', 'Accuracy')
    g.add_legend()
    plt.savefig(f"acc.pdf", bbox_inches='tight')

ilp_stat_f = "test.json"
ilp_stat = json.load(open(ilp_stat_f, "r"))
knn_stat_f = "data/knn_theory_stat.json"
knn_stat = json.load(open(knn_stat_f, "r"))

plot_theories_acc(ilp_stat, knn_stat)
