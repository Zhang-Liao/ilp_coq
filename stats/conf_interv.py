import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def sub_without_last(a, b):
    s = np.subtract(a, b)
    s = [x[:-2] for x in s]
    return s


def conf(l):
    return stats.norm.interval(confidence=0.95, loc=np.mean(l), scale=stats.sem(l))


def to_sec(l):
    return [x[0] * 60 + x[1] for x in l]


def load_acc(f):
    return np.loadtxt(f, delimiter=",", dtype=float)


knn_acc = load_acc("log/knn_acc.csv")[:5]

prop_acc = load_acc("log/prop_acc.csv")

rel1_acc = load_acc("log/rel1_acc.csv")

rel2_acc = load_acc("log/rel2_acc.csv")

# rel2_acc = []

# prop_time = []

# rel1_time = []

# rel2_time = []


prop_to_knn = sub_without_last(prop_acc, knn_acc)
rel1_to_knn = sub_without_last(rel1_acc, knn_acc)
rel2_to_knn = sub_without_last(rel2_acc, knn_acc)


# rel1_to_prop = sub_without_last(rel1_acc, prop_acc)

conf_prop_knn = conf(prop_to_knn)
conf_rel1_knn = conf(rel1_to_knn)
conf_rel2_knn = conf(rel2_to_knn)

plt.plot(k, ilp, label="ILP + kNN")
plt.plot(k, knn, label="kNN")

# naming the x axis
plt.xlabel("lower bound")
plt.ylabel("%")

plt.legend()
plt.savefig("results.pdf", bbox_inches="tight")


# print(conf(rel1_to_knn))
# print(conf(rel2_to_knn))
# print(conf(rel1_to_prop))
