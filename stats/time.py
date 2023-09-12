
import numpy as np

def load_time(f):
    tm = np.loadtxt(f, delimiter=",", dtype=float)
    tm[:, 0] *= 60
    # return tm[:, 0]
    return np.mean((tm[:, 0] + tm[:, 1])/3600)

prop = load_time("log/prop_tm.csv")
rel1 = load_time("log/rel1_tm.csv")
rel2 = load_time("log/rel2_tm.csv")
rel3 = load_time("log/rel3_tm.csv")
print(prop)
print(rel1)
print(rel2)
print(rel3)

