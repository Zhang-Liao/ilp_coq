import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def stat_f1(dfs):
    for df in dfs:
        prec = df.iloc[0]["prec"]
        plt.figure(figsize=(24, 4.8))
        sns.lineplot(data=df, x="param", y="f1", hue="predicate")
        plt.show()
        plt.savefig(f"tune{prec}.pdf", bbox_inches='tight')


def best_param(df):
    sort_df = df.sort_values(by=["f1"], ascending=False)
    kinds = sort_df["predicate"].drop_duplicates()
    for _, kind in kinds.items():
        best = sort_df.loc[sort_df["predicate"] == kind].iloc[0]
        print(best)


def mk_f1_df(stat, theory):
    dic = {"predicate": [], "f1": [], "param": [], "prec": []}
    for kind, kind_stat in stat.items():
        theory_stat = kind_stat[theory]
        for pos, pos_stat in theory_stat.items():
            for neg, neg_stat in pos_stat.items():
                for prec, f1 in neg_stat.items():
                        if 'anonym' in kind:
                            dic["predicate"].append(f"{kind}")
                            dic["f1"].append(f1)
                            dic["param"].append(f"p{pos}n{neg}")
                            dic["prec"].append(prec)
    df = pd.DataFrame(data=dic)
    print(df)
    best_param(df)
    return df


def mk_f1_dfs(stat, theory):
    # name = theory.split("/")[-1]
    df = mk_f1_df(stat["f1"], theory)
    sub_dfs = [y for x, y in df.groupby("prec")]
    return sub_dfs


f_stats = "/home/zhangliao/ilp_out_coq/ilp_out_coq/tune_valid.json"
reader = open(f_stats, "r")
stat = json.load(reader)
# theory = "theories/ListsLogic"
theory = "valid/valid"
dfs = mk_f1_dfs(stat, theory)
# stat_f1(dfs)