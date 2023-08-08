import os
import sys
from pathlib import Path
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting

labels = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split'
out = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/all.label'

tacs = set()
for i in range(10):
    file = os.path.join(labels, f'split{i}.label')
    with open(file, 'r') as r :
        for t in r:
            if global_setting.lemma_delimiter not in t :
                tacs.add(t.strip())
    # print(tacs)

with open(out, 'w') as w:
    for t in tacs:
        w.write(t + '\n')