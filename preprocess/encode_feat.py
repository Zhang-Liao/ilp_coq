import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting

import argparse
import joblib
import json
from sklearn.preprocessing import LabelEncoder

def mk_label_encoder(encoder, dir):
    feats = set()
    for root, _, files in os.walk(dir):
        for i in range(len(files)):
            f = os.path.join(root, 'split'+str(i)+'.json')
            with open(f, 'r') as reader:
                for l in reader:
                    l = l.strip()
                    if global_setting.lemma_delimiter not in l:
                        l = json.loads(l)
                        for f in l['feats']:
                            feats.add(f[0])
    encoder.fit(list(feats))
    return feats

parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str)
opts = parser.parse_args()
dir = opts.dir
out = os.path.join(dir, 'feat_encoder.gz')
encoder = LabelEncoder()
joblib.dump(mk_label_encoder(encoder, dir), out, 3)