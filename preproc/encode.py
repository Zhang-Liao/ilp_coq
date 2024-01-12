import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils

import argparse
import joblib
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MultiLabelBinarizer


def encode(dir):
    l_encoder = LabelEncoder()
    f_encoder = MultiLabelBinarizer()
    feats = []
    labels = set()
    for root, dir, files in os.walk(dir):
        for file in files:
            if file.endswith("QArith.json"):
                reader = open(os.path.join(root, file), "r")
                for l in reader:
                    l = l.strip()
                    if utils.not_lemma(l):
                        l = json.loads(l)
                        fs = [f[0] for f in l["feats"]]
                        # for f in l['feats']:
                        feats.append(fs)
                        labels.add(l["tac"])
    f_encoder.fit(list(feats))
    l_encoder.fit(list(labels))
    return f_encoder, l_encoder


parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str)
opts = parser.parse_args()
f_out = os.path.join(opts.dir, "complex_feat_encoder.gz")
# l_out = os.path.join(opts.dir, "label_ortho_encoder.gz")
f_encoder, l_encoder = encode(opts.dir)
print("number of features", len(f_encoder.classes_))
print("number of labels", len(l_encoder.classes_))
joblib.dump(f_encoder, f_out)
# joblib.dump(l_encoder, l_out)
