import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting

import argparse
import joblib
import json
from sklearn.preprocessing import LabelEncoder

def encode(dir):
    l_encoder = LabelEncoder()
    f_encoder = LabelEncoder ()
    feats = set()
    labels = set()
    for root, _, _ in os.walk(dir):
        for i in range(10):
            f = os.path.join(root, 'split'+str(i)+'.json')
            with open(f, 'r') as reader:
                for l in reader:
                    l = l.strip()
                    if global_setting.lemma_delimiter not in l:
                        l = json.loads(l)
                        for f in l['feats']:
                            feats.add(f[0])
                        labels.add(l['tac'])
        # prevent from recursivly looking into the directories
        break
    f_encoder.fit(list(feats))
    l_encoder.fit(list(labels))
    return f_encoder, l_encoder

parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str)
opts = parser.parse_args()
f_out = os.path.join(opts.dir, 'feat_encoder.gz')
l_out = os.path.join(opts.dir, 'label_encoder.gz')
l_encoder, f_encoder = encode(opts.dir)
joblib.dump(f_encoder, f_out)
joblib.dump(l_encoder, l_out)