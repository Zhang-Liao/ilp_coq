import json
import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))

import argparse
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MultiLabelBinarizer

from lib import utils


feat_encoder = joblib.load('data/json/feat/merge/theories/Structures/feat_encoder.gz')
label_encoder = joblib.load('data/json/feat/merge/theories/Structures/label_encoder.gz')

assert(isinstance(label_encoder, LabelEncoder))
assert(isinstance(feat_encoder, MultiLabelBinarizer))

print('number of feat', len(feat_encoder.classes_))
print('number of label', len(label_encoder.classes_))

def read(f_feat, f_label):
    labels = []
    feats = []
    with open(f_label, 'r') as reader:
        for l in reader:
            l = l.strip()
            if utils.not_lemma(l):
                labels.append(l)
        labels = label_encoder.transform(labels)

    with open(f_feat, 'r') as reader:
        for l in reader:
            l = l.strip()
            if utils.not_lemma(l):
                fs = l.split()
                fs = [int(f) for f in fs]
                feats.append(fs)
        feats = feat_encoder.transform(feats)
    return feats, labels

def get_negs(ids, labels, label):
    negs = []
    n = 0
    for id, label2 in zip(ids, labels):
        if label2 != label:
            negs.append(int(id))
            n += 1
            # if n == 300:
            #     break
    return negs

def update_dic(i, tac, negs, dict):
    if tac not in dict.keys():
        dict[tac] = {i : negs}
    else:
        dict[tac][i] = negs

def exg_row_ids_map(f_label):
    mp = []
    with open(f_label, 'r') as reader:
        row_id = 0
        for l in reader:
            l = l.strip()
            if utils.not_lemma(l):
                mp.append(row_id)
            row_id += 1
    return mp

def map_exg_row_ids(dict, mp):
    new_dict = {}
    for tac, pos_negs_dict in dict.items():
        new_pos_negs = {}
        for pos, negs in pos_negs_dict.items():
            new_pos_negs[mp[pos]] = [mp[n] for n in negs]
        new_dict[tac] = new_pos_negs
    return new_dict

parser = argparse.ArgumentParser()
parser.add_argument("--feat", type=str)
parser.add_argument("--label", type=str)
opts = parser.parse_args()

root, ext = os.path.splitext(opts.label)

dict = {}
feats, labels = read(opts.feat, opts.label)
neigh = KNeighborsClassifier(n_neighbors=1, metric='jaccard', n_jobs=10)
neigh.fit(feats, labels)
kneighs_arr = neigh.kneighbors(feats, 300, False)
for i in range(len(labels)):
    tac = label_encoder.inverse_transform([labels[i]])[0]
    kneighs = kneighs_arr[i]
    k_labels = labels[kneighs]
    negs = get_negs(kneighs, k_labels, labels[i])
    update_dic(i, tac, negs, dict)

out = root + "_neg.json"

mp = exg_row_ids_map(opts.label)
dict = map_exg_row_ids(dict, mp)
# print(dict)
with open(out, 'w') as w:
    json.dump(dict, w)
