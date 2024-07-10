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


def calculate_n(dat, max_cls):
    return math.ceil(dat / max_cls)


def calculate_min(n_label, n_cls, max_cls):
    # Using floor to avoid n_cls * min > n_label
    min_ = math.floor(n_label / n_cls)
    if min_ == max_cls:
        min_ -= 1
    return min_


def init_clusters(n):
    c = []
    for _ in range(n):
        c.append([])
    return c


def split_clusters(clusters, max_cls):
    new_clusters = []
    for c in clusters:
        num = len(c)
        if num < max_cls:
            new_clusters.append(c)
        else:
            k_split = int(num / max_cls)
            if k_split * max_cls != num:
                k_split += 1
            split = np.array_split(c, k_split)
            for s in split:
                s = [int(x) for x in s]
                new_clusters.append(list(s))
    return new_clusters


def run_cluster(exgs, max_cls):
    feats = [e[0] for e in exgs]
    row_is = [e[1] for e in exgs]
    feats = feat_encoder.transform(feats)
    n_label = len(row_is)
    if n_label < max_cls:
        cls = [0] * n_label
        clusters = init_clusters(1)
    else:
        n_cls = calculate_n(n_label, max_cls)
        clf = KMeansConstrained(
            n_clusters=n_cls,
            size_min=calculate_min(n_label, n_cls, max_cls),
            size_max=max_cls,
            random_state=0,
        )
        cls = clf.fit_predict(feats)
        cls = np.ndarray.tolist(cls)
        clusters = init_clusters(len(set(clf.labels_)))
    for node, i in zip(cls, row_is):
        clusters[node].append(i)
    return clusters


def cluster_by_tacs(dat, max_cls):
    cluster = {}
    for tac, states in dat.items():
        # print(states)
        cluster[tac] = run_cluster(states, max_cls)
        # exit()
    return cluster


parser = argparse.ArgumentParser()
parser.add_argument("--feat", type=str)
parser.add_argument("--label", type=str)
parser.add_argument("--max_cluster", type=int)
# MAX_CLUSTER_LEN = 16

opts = parser.parse_args()

feat_encoder = joblib.load("data/json/feat/merge/theories/Structures/feat_encoder.gz")

assert isinstance(feat_encoder, MultiLabelBinarizer)

dat = loader(opts.feat, opts.label)
cluster = cluster_by_tacs(dat, opts.max_cluster)
root, ext = os.path.splitext(opts.feat)

with open(root + f"_pos{opts.max_cluster}.json", "w") as w:
    json.dump(cluster, w)
