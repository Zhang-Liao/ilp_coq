import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)

opts = parser.parse_args()

assert(opts.file.endswith('.b'))

with open(opts.file, 'r') as r:
    dat = r.readlines()
    for i in range(len(dat)):
        l = dat[i]
        if re.match(':- set\(evalfn, .+\)\.\n', l):
            dat[i] = f'%{l}'
            break

with open(opts.file, 'w') as w:
    w.writelines(dat)