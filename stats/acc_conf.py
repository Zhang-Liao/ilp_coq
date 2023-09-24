import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def conf(l):
    conf = stats.norm.interval(0.95, loc=np.mean(l, axis = 0), scale=stats.sem(l))
    return conf

def to_sec(l):
    return [x[0] * 60 + x[1] for x in l]


def load_acc(f):
    return np.loadtxt(f, delimiter=",", dtype=float)


knn_acc = load_acc("log/knn_acc.csv")[:5]
prop_acc = load_acc("log/prop_acc.csv")
rel1_acc = load_acc("log/rel1_acc.csv")
rel2_acc = load_acc("log/rel2_acc.csv")
rel3_acc = load_acc("log/rel3_acc.csv")

conf_knn = conf(knn_acc)
conf_prop = conf(prop_acc)
conf_rel1 = conf(rel1_acc)
conf_rel2 = conf(rel2_acc)
conf_rel3 = conf(rel3_acc)

k = list(range(0, 10))

plt.plot(k, conf_knn[0], label="knn mean lower")
plt.plot(k, conf_prop[0], label="prop lower")
# plt.plot(k, conf_rel1[0], label="position lower")
# plt.plot(k, conf_rel2[0], label="position + eq lower")
plt.plot(k, conf_rel1[0], label="position + var lower")


plt.plot(k, conf_knn[1], label="knn mean upper")
plt.plot(k, conf_prop[1], label="prop upper")
plt.plot(k, conf_rel1[1], label="position upper")

plt.xlabel("confidential interval")
plt.ylabel("%")

plt.legend()
plt.savefig("conf_inter.pdf", bbox_inches="tight")
