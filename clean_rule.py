import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)

opts = parser.parse_args()

with open(opts.file, 'r') as r:
    dat = []
    for l in r:
        if not re.match('tac\(.+\)\.\n', l):
            dat.append(l)

with open(opts.file, 'w') as w:
    w.writelines(dat)