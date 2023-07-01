import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting
import json
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MultiLabelBinarizer

feat_encoder = joblib.load('/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/feat_encoder.gz')
label_encoder = joblib.load('/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/label_encoder.gz')
feat_file = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/split0.feat"
label_file = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/split0.label"

assert(isinstance(label_encoder, LabelEncoder))
assert(isinstance(feat_encoder, MultiLabelBinarizer))

root, ext = os.path.splitext(feat_file)

print('number of feat', len(feat_encoder.classes_))
print('number of label', len(label_encoder.classes_))

dict = {}
labels = []
feats = []
with open(label_file, 'r') as reader:
    for l in reader:
        l = l.strip()
        if global_setting.lemma_delimiter not in l:
            labels.append(l)
    labels = label_encoder.transform(labels)

with open(feat_file, 'r') as reader:
    for l in reader:
        l = l.strip()
        if global_setting.lemma_delimiter not in l:
            fs = l.split()
            fs = [int(f) for f in fs]
            feats.append(fs)
    feats = feat_encoder.transform(feats)

def get_negs(ids, labels, label):
    negs = []
    n = 0
    for id, label2 in zip(ids, labels):
        if label2 != label:
            negs.append(int(id))
            n += 1
            if n == 10:
                break
    return negs

def update_dic(tac, negs):
    negs = set(negs)
    if tac not in dict.keys():
        dict[tac] = negs
    else:
        dict[tac] = dict[tac].union(negs)

neigh = KNeighborsClassifier(n_neighbors=1, metric='jaccard', n_jobs=5)
neigh.fit(feats, labels)
kneighs_arr = neigh.kneighbors(feats, 500, False)
for i in range(len(labels)):
    tac = label_encoder.inverse_transform([labels[i]])[0]    
    kneighs = kneighs_arr[i]
    k_labels = labels[kneighs]
    negs = get_negs(kneighs, k_labels, labels[i])
    update_dic(tac, negs)
    # neg_labels = label_encoder.inverse_transform(labels[negs])
    # print('negs', negs)
    # print('neg_labels', neg_lables)
    # print('current label', curr_label)
    # print()

for key, negs in dict.items():
    dict[key] = list(negs)

out = root + "_neg.json"
with open(out, 'w') as w:
    json.dump(dict, w)  
