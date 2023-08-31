import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)
opts = parser.parse_args()

assert(opts.file.endswith('.b'))

with open(opts.file, 'r') as r:
    dat = r.readlines()

for i in range(len(dat)):
    line = dat[i]
    if re.match(':- set\(noise, [0-9]+\)\.\n', line):
        dat[i] = f':- set(noise, 0).\n'
        break

with open(opts.file, 'w') as w:
    w.writelines(dat)