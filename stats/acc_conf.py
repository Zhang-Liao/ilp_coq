import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


# def sub_without_last(a, b):
#     s = np.subtract(a, b)
#     s = [x[:-1] for x in s]
#     return s


def conf(l):
    # print('l', l)
    # print('np.mean(l)', np.mean(l, axis = 0))
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

# rel2_acc = []

# prop_time = []

# rel1_time = []

# rel2_time = []

# knn_mean = np.mean(knn_acc, axis = 0)
# prop_to_knn = sub_without_last(prop_acc, knn_acc)
# rel1_to_knn = sub_without_last(rel1_acc, knn_acc)
# rel2_to_knn = sub_without_last(rel2_acc, knn_acc)
# rel3_to_knn = sub_without_last(rel3_acc, knn_acc)

# print('prop_to_knn', prop_to_knn)

# rel1_to_prop = sub_without_last(rel1_acc, prop_acc)

conf_knn = conf(knn_acc)
conf_prop = conf(prop_acc)
conf_rel1 = conf(rel1_acc)
conf_rel2 = conf(rel2_acc)
conf_rel3 = conf(rel3_acc)

k = list(range(0, 10))

plt.plot(k, conf_knn[0], label="knn mean")
plt.plot(k, conf_prop[0], label="prop")
plt.plot(k, conf_rel1[0], label="position")
plt.plot(k, conf_rel2[0], label="position + eq")
plt.plot(k, conf_rel3[0], label="position + var")

plt.xlabel("lower bound")
plt.ylabel("%")

plt.legend()
plt.savefig("lower_bound.pdf", bbox_inches="tight")

plt.clf()
plt.plot(k, conf_knn[1], label="knn mean")
plt.plot(k, conf_prop[1], label="prop")
plt.plot(k, conf_rel1[1], label="position")
plt.plot(k, conf_rel2[1], label="position + eq")
plt.plot(k, conf_rel3[1], label="position + var")

plt.xlabel("upper bound")
plt.ylabel("%")

plt.legend()
plt.savefig("upper_bound.pdf", bbox_inches="tight")


# print(conf(rel1_to_knn))
# print(conf(rel2_to_knn))
# print(conf(rel1_to_prop))
