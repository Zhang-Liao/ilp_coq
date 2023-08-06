import os
import sys
from pathlib import Path
sys.path.append(os.path.dirname(sys.path[0]))

dataset = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat'
out = 'file_order'

order = []
for root, _, files in os.walk(dataset):
    for file in files:
        if Path(file).suffix == '.json':
            path = os.path.join(root, file)
            # print(path)
            rel_path = os.path.relpath(path, dataset)
            order.append(rel_path)

with open(out, 'w') as w:
    for f in order:
        w.write(f + '\n')