import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def kind_to_abs(k):
    if k == "anonym_feat":
        return "AF"
    elif k == "anonym_repr":
        return "AR"
    elif k == "origin_feat":
        return "OF"
    elif k == "origin_repr":
        return "OR"


def stat_f1(df):
    # df = df.loc[df["Precision"].isin([0.1])]
    df = df.loc[df["Precision"].isin([0, 0.18, 0.30])]
    # df = df.loc[df["Precision"].isin([0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.3])]
    sns.set(font_scale=1.5)
    g = sns.FacetGrid(
        df, col="Precision", hue="Predicates", col_wrap=1, height=3.5, aspect=6
    )
    ax = g.map(sns.lineplot, "Combination of the Number of Positive Examples and the Number of Negative Examples per Positive Example", "F-1")
    g.add_legend()
    # prec = df.iloc[0]["prec"]
    # plt.figure(figsize=(24, 20))
    # ax = sns.lineplot(data=df, x="param", y="f1", hue="predicates")
    # plt.show()
    ax.set(xlabel=None, ylabel = 'F-1')
    plt.xticks(rotation=60)
    plt.savefig("tune.pdf", bbox_inches="tight")


def best_param(df):
    sort_df = df.sort_values(by=["F-1"], ascending=False)
    kinds = sort_df["Predicates"].drop_duplicates()
    for _, kind in kinds.items():
        best = sort_df.loc[sort_df["Predicates"] == kind].iloc[0]
        print(best)


def mk_f1_df(stat, theory):
    dic = {
        "Predicates": [],
        "F-1": [],
        "Combination of the Number of Positive Examples and the Number of Negative Examples per Positive Example": [],
        "Precision": [],
    }
    for kind, kind_stat in stat.items():
        theory_stat = kind_stat[theory]
        for pos, pos_stat in theory_stat.items():
            for neg, neg_stat in pos_stat.items():
                for prec, f1 in neg_stat.items():
                    # if 'anonym_rel' in kind:
                    prec = int(prec) / 100
                    dic["Predicates"].append(kind_to_abs(kind))
                    dic["F-1"].append(f1)
                    dic["Combination of the Number of Positive Examples and the Number of Negative Examples per Positive Example"].append(
                        f"P{pos}N{neg}"
                    )
                    dic["Precision"].append(prec)
    df = pd.DataFrame(data=dic)
    print(df)
    best_param(df)
    return df

f_stats = "tune_valid.json"
reader = open(f_stats, "r")
stat = json.load(reader)
theory = "valid/valid"
df = mk_f1_df(stat["f1"], theory)
stat_f1(df)
