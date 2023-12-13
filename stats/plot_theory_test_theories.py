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


ilp_stat_f = "/home/zhangliao/ilp_out_coq/ilp_out_coq/stats/ortho/ortho_test.json"
ilp_stat = json.load(open(ilp_stat_f, "r"))

f1_df = mk_f1_df(ilp_stat)
sns.barplot(data=f1_df, x="theory", y="f1", hue="predc")
# plt.show()
plt.savefig("stats/ortho/test.pdf")
