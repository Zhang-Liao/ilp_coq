import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


f_stats = "theory_stat.json"
stat = json.load(open(f_stats, "r"))
dat = {"predc": [], "f1": [], "theory": []}
for kind, kind_stat in stat["f1"].items():
    for theory, theory_stat in kind_stat.items():
        theory = theory.split("/")[-1]
        f1s = list(theory_stat.values())
        dat["predc"].append(kind)
        dat["f1"].append(np.average(f1s))
        dat["theory"].append(theory)
df = pd.DataFrame(data=dat)
# print(df)
sns.barplot(data=df, x="theory", y="f1", hue="predc")
plt.show()
