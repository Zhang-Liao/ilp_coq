import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str)
args = parser.parse_args()

# dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/'

settings = [':- style_check(-singleton).\n']

def add_setting(file):
    with open(file, 'r') as f:
        clauses = f.readlines()
    dat = settings + clauses
    with open(file, 'w') as f:
        for l in dat:
            f.write(l)

for file in os.listdir(args.dir):
    # print(file)
    if file.endswith('.rule.pl'):
        path = os.path.join(args.dir, file)
        add_setting(path)
