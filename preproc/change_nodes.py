import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)
parser.add_argument("--nodes", type=int)

opts = parser.parse_args()

assert(opts.file.endswith('.b'))

with open(opts.file, 'r') as r:
    dat = r.readlines()
    for i in range(len(dat)):
        l = dat[i]
        if re.match(':- set\(nodes, .+\)\.\n', l):
            dat[i] = f':- set(nodes, {opts.nodes}).\n'
            break

with open(opts.file, 'w') as w:
    w.writelines(dat)