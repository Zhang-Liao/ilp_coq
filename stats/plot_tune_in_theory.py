import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# def stat_f1(dfs):
#     for df in dfs:
#         prec = df.iloc[0]["prec"]
#         plt.figure(figsize=(24, 4.8))
#         sns.lineplot(data=df, x="param", y="f1", hue="kind")
        # plt.show()
        # plt.savefig(f"stats/ortho_tune{prec}.png")


def best_param(df):
    sort_df = df.sort_values(by=["f1"], ascending=False)
    kinds = sort_df["kind"].drop_duplicates()
    for _, kind in kinds.items():
        best = sort_df.loc[sort_df["kind"] == kind].iloc[0]
        print(best)


def mk_f1_df(stat, theory, name):
    dic = {"kind": [], "f1": [], "param": [], "prec": []}
    for kind, kind_stat in stat.items():
        theory_stat = kind_stat[theory]
        for pos, pos_stat in theory_stat.items():
            for neg, neg_stat in pos_stat.items():
                for prec, f1 in neg_stat.items():
                    if 'anonym' in kind:
                        dic["kind"].append(f"{kind}_{name}")
                        dic["f1"].append(f1)
                        dic["param"].append(f"p{pos}n{neg}")
                        dic["prec"].append(prec)
    df = pd.DataFrame(data=dic)
    best_param(df)
    return df


def mk_f1_dfs(stat, theory):
    name = theory.split("/")[-1]
    df = mk_f1_df(stat["f1"], theory, name)
    sub_dfs = [y for x, y in df.groupby("prec")]

    # dfs.append(mk_f1_df(stat["f1"], theory, name))
    # dfs.append(mk_f1_df(stat["f1_no_ignored_tac"], theory, f"{name}_nontrivial"))
    return sub_dfs


f_stats = "tune_ortho_logic.json"
reader = open(f_stats, "r")
stat = json.load(reader)
theory = "theories/Logic"
dfs = mk_f1_dfs(stat, theory)
# print(df)
# stat_f1(dfs)
