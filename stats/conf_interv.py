import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def sub_without_last(a, b):
    s = np.subtract(a, b)
    s = [x[:-1] for x in s]
    return s


def conf(l):
    # print('l', l)
    # print('np.mean(l)', np.mean(l, axis = 0))
    conf = stats.norm.interval(0.95, loc=np.mean(l, axis = 0), scale=stats.sem(l))
    return (np.append(conf[0], [0]), np.append(conf[1], [0]))

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

knn_mean = np.mean(knn_acc, axis = 0)
prop_to_knn = sub_without_last(prop_acc, knn_acc)
rel1_to_knn = sub_without_last(rel1_acc, knn_acc)
rel2_to_knn = sub_without_last(rel2_acc, knn_acc)
rel3_to_knn = sub_without_last(rel3_acc, knn_acc)

# print('prop_to_knn', prop_to_knn)

# rel1_to_prop = sub_without_last(rel1_acc, prop_acc)

conf_prop_knn = conf(prop_to_knn)
conf_rel1_knn = conf(rel1_to_knn)
conf_rel2_knn = conf(rel2_to_knn)
conf_rel3_knn = conf(rel3_to_knn)

k = list(range(0, 10))
# print(knn_acc)
# print('knn mean', np.mean(knn_acc))
plt.plot(k, knn_mean, label="knn mean")
plt.plot(k, np.add(conf_prop_knn[0], knn_mean), label="prop")
plt.plot(k, np.add(conf_rel1_knn[0], knn_mean), label="position")
plt.plot(k, np.add(conf_rel2_knn[0], knn_mean), label="position + eq")
plt.plot(k, np.add(conf_rel3_knn[0], knn_mean), label="position + var")

plt.xlabel("lower bound")
plt.ylabel("%")

plt.legend()
plt.savefig("lower_bound.pdf", bbox_inches="tight")

plt.clf()
plt.plot(k, knn_mean, label="knn mean")
plt.plot(k, np.add(conf_prop_knn[1], knn_mean), label="prop")
plt.plot(k, np.add(conf_rel1_knn[1], knn_mean), label="position")
plt.plot(k, np.add(conf_rel2_knn[1], knn_mean), label="position + eq")
plt.plot(k, np.add(conf_rel3_knn[1], knn_mean), label="position + var")

plt.xlabel("upper bound")
plt.ylabel("%")

plt.legend()
plt.savefig("upper_bound.pdf", bbox_inches="tight")


# print(conf(rel1_to_knn))
# print(conf(rel2_to_knn))
# print(conf(rel1_to_prop))
