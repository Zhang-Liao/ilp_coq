import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def kind_to_abs(k):
    if k == "anonym_rel":
        return "AR"
    elif k == "anonym_prop":
        return "AP"
    elif k == "origin_prop":
        return "OP"
    elif k == "origin_rel":
        return "OR"


def stat_f1(df):
    # for df in dfs:
    df = df.loc[df["precision"].isin([0, 0.1, 0.3])]
    g = sns.FacetGrid(
        df, col="precision", hue="predicate", col_wrap=1, height=3.5, aspect=5
    )
    g.map(sns.lineplot, "combination of the number of positive examples and the number of negative examples per positive example", "F-1")
    g.add_legend()
    # prec = df.iloc[0]["prec"]
    # plt.figure(figsize=(24, 20))
    # ax = sns.lineplot(data=df, x="param", y="f1", hue="predicate")
    # plt.show()
    # ax.set(xlabel=None, ylabel = 'F-1')
    plt.xticks(rotation=45)
    plt.savefig("tune.pdf", bbox_inches="tight")


def best_param(df):
    sort_df = df.sort_values(by=["F-1"], ascending=False)
    kinds = sort_df["predicate"].drop_duplicates()
    for _, kind in kinds.items():
        best = sort_df.loc[sort_df["predicate"] == kind].iloc[0]
        print(best)


def mk_f1_df(stat, theory):
    dic = {
        "predicate": [],
        "F-1": [],
        "combination of the number of positive examples and the number of negative examples per positive example": [],
        "precision": [],
    }
    for kind, kind_stat in stat.items():
        theory_stat = kind_stat[theory]
        for pos, pos_stat in theory_stat.items():
            for neg, neg_stat in pos_stat.items():
                for prec, f1 in neg_stat.items():
                    # if 'anonym' in kind:
                    prec = int(prec) / 100
                    dic["predicate"].append(kind_to_abs(kind))
                    dic["F-1"].append(f1)
                    dic["combination of the number of positive examples and the number of negative examples per positive example"].append(
                        f"pos{pos}neg{neg}"
                    )
                    dic["precision"].append(prec)
    df = pd.DataFrame(data=dic)
    print(df)
    best_param(df)
    return df


# def mk_f1_dfs(stat, theory):
# name = theory.split("/")[-1]
# df = mk_f1_df(stat["f1"], theory)
# sub_dfs = [y for x, y in df.groupby("prec")]
# return sub_dfs


f_stats = "tune_valid.json"
reader = open(f_stats, "r")
stat = json.load(reader)
theory = "valid/valid"
df = mk_f1_df(stat["f1"], theory)
stat_f1(df)
