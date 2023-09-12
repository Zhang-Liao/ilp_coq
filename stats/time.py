
import numpy as np

def to_sec(l):
    return [x[0] * 60 + x[1] for x in l]

def load_time(f):
    tm = np.loadtxt(f, delimiter=",", dtype=float)
    tm[:, 0] *= 60
    # return tm[:, 0]
    return tm[:, 0] + tm[:, 1]

prop = load_time("log/prop_tm.csv")
rel1 = load_time("log/rel1_tm.csv")
rel2 = load_time("log/rel2_tm.csv")
# rel3_acc = load_time("log/rel3_acc.csv")
print(prop)
print(rel1)
print(rel2)

