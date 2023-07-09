import json
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting

from pyswip import Prolog

prolog = Prolog()

def tac2predc(t):
    return "{}".format(t)

def encode(dir, out):
    for root, _, _ in os.walk(dir):
        for i in range(10):
            f = os.path.join(root, 'split'+str(i)+'.json')
            with (open(f, 'r') as reader, open(out, 'a') as w):
                for l in reader:
                    l = l.strip()
                    if global_setting.lemma_delimiter not in l:
                        l = json.loads(l)
                        prolog.assertz(tac2predc(l['tac']))
                        # w.write(tac2predc(l['tac']))

dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split'
out = os.path.join(dir, 'tac.pl')

if os.path.exists(out):
    os.remove(out)

encode(dir, out)