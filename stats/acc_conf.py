import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def conf(l):
    conf = stats.norm.interval(0.95, loc=np.mean(l, axis=0), scale=stats.sem(l))
    return conf


def to_sec(l):
    return [x[0] * 60 + x[1] for x in l]


def load_acc(f):
    return np.loadtxt(f, delimiter=",", dtype=float)


knn_acc = load_acc("log/knn_acc.csv")[:5]
rel_acc = [
    [14.165, 20.785, 24.152, 26.285, 27.632, 28.639, 29.551, 30.376, 31.062, 31.685],
    [14.312, 23.076, 25.751, 27.4, 28.657, 29.649, 30.481, 31.434, 32.124, 32.775],
    [13.089, 18.796, 21.929, 24.121, 25.45, 26.619, 27.601, 28.359, 28.982, 29.564],
    [17.337, 22.941, 26.595, 28.51, 29.913, 30.905, 31.726, 32.393, 33.128, 33.715],
    [14.101, 19.791, 23.062, 25.193, 26.309, 27.443, 28.465, 29.58, 30.297, 30.957],
    [10.959, 15.278, 18.092, 19.961, 21.634, 23.024, 24.219, 27.046, 29.692, 30.616],
]

prop_acc = [
    [13.618, 19.269, 22.56, 25.027, 26.757, 28.104, 29.149, 30.206, 30.955, 31.685],
    [14.325, 22.393, 24.816, 26.492, 27.864, 29.076, 30.062, 31.106, 31.989, 32.775],
    [12.531, 17.932, 20.771, 23.193, 24.809, 26.114, 27.407, 28.247, 28.894, 29.564],
    [15.86, 21.259, 25.141, 26.509, 27.872, 28.932, 29.833, 32.085, 32.997, 33.715],
    [13.117, 18.389, 21.679, 23.922, 25.411, 26.72, 27.947, 29.318, 30.203, 30.957],
    [11.283, 16.047, 18.928, 20.663, 22.262, 23.517, 24.604, 27.31, 29.827, 30.616],
]

conf_knn = conf(knn_acc)
conf_prop = conf(prop_acc)
conf_rel = conf(rel_acc)

k = list(range(0, 10))

plt.plot(k, conf_knn[0], label="knn lower")
plt.plot(k, conf_prop[0], label="prop ILP lower")
# plt.plot(k, conf_rel1[0], label="position lower")
# plt.plot(k, conf_rel2[0], label="position + eq lower")
plt.plot(k, conf_rel[0], label="rel ILP lower")


plt.plot(k, conf_knn[1], label="knn upper")
plt.plot(k, conf_prop[1], label="prop ILP upper")
plt.plot(k, conf_rel[1], label="rel ILP upper")

plt.xlabel("confidential interval")
plt.ylabel("%")

plt.legend()
plt.savefig("conf_inter.pdf", bbox_inches="tight")
