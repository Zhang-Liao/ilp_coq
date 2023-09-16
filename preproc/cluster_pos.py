import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))

import argparse
import joblib
from k_means_constrained import KMeansConstrained
import math
import numpy as np
# from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer

from lib import utils

MAX_CLUSTER_LEN = 50


def loader(feat_f, label_f):
    labels = []
    feats = []
    with open(label_f, "r") as reader:
        for l in reader:
            l = l.strip()
            labels.append(l)

    with open(feat_f, "r") as reader:
        for l in reader:
            l = l.strip()
            if utils.not_lemma(l):
                fs = l.split()
                fs = [int(f) for f in fs]
                feats.append(fs)
            else:
                feats.append(l)
    dat = zip(feats, labels)
    dat_by_tac = {}
    i = 0
    for feat, label in dat:
        if utils.not_lemma(label):
            if label not in dat_by_tac.keys():
                dat_by_tac[label] = [(feat, i)]
            else:
                dat_by_tac[label].append((feat, i))
        i += 1
    return dat_by_tac


def calculate_n(dat):
    n = dat / MAX_CLUSTER_LEN
    if n < 1:
        return 1
    else:
        return round(n)


def calculate_n2(dat):
    return math.ceil(dat / MAX_CLUSTER_LEN)


def calculate_min(dat):
    return math.floor(dat / MAX_CLUSTER_LEN)


def init_clusters(n):
    c = []
    for _ in range(n):
        c.append([])
    return c


def split_clusters(clusters):
    new_clusters = []
    for c in clusters:
        num = len(c)
        if num < MAX_CLUSTER_LEN:
            new_clusters.append(c)
        else:
            k_split = int(num / MAX_CLUSTER_LEN)
            if k_split * MAX_CLUSTER_LEN != num:
                k_split += 1
            split = np.array_split(c, k_split)
            for s in split:
                s = [int(x) for x in s]
                new_clusters.append(list(s))
    return new_clusters


def run_cluster(exgs):
    feats = [e[0] for e in exgs]
    row_is = [e[1] for e in exgs]
    feats = feat_encoder.transform(feats)
    n_label = len(row_is)
    if n_label < MAX_CLUSTER_LEN:
        cls = [0] * n_label
        clusters = init_clusters(1)
    else:
        clf = KMeansConstrained(
            n_clusters=calculate_n2(n_label),
            size_min=calculate_min(n_label),
            size_max=MAX_CLUSTER_LEN,
            random_state=0,
        )
        cls = clf.fit_predict(feats)
        cls = np.ndarray.tolist(cls)
        clusters = init_clusters(len(set(clf.labels_)))
    for node, i in zip(cls, row_is):
        clusters[node].append(i)
        # print(cls)
        # exit(0)
    # kmeans = KMeans(n_clusters=calculate_n(len(labels)), random_state=0, n_init="auto")
    # kmeans.fit(feats)
    # num_class = max(kmeans.labels_) + 1
    # clusters = init_clusters(num_class)
    # for i_class, i_row in zip(list(kmeans.labels_), labels):
    #     clusters[i_class].append(i_row)
    # clusters = split_clusters(clusters)
    # clusters = [c for c in clusters if c != []]
    return clusters


def cluster_by_tacs(dat):
    cluster = {}
    for tac, states in dat.items():
        # print(states)
        cluster[tac] = run_cluster(states)
        # exit()
    return cluster


parser = argparse.ArgumentParser()
parser.add_argument("--feat", type=str)
parser.add_argument("--label", type=str)
opts = parser.parse_args()

feat_encoder = joblib.load(
    "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/feat_encoder.gz"
)
# feat_f = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/split0_7.feat"
# label_f = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/split0_7.label"

assert isinstance(feat_encoder, MultiLabelBinarizer)

dat = loader(opts.feat, opts.label)
cluster = cluster_by_tacs(dat)
root, ext = os.path.splitext(opts.feat)

with open(root + "_pos_eq50.json", "w") as w:
    json.dump(cluster, w)
