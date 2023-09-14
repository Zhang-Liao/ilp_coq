import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)
parser.add_argument("--noise", type=int)

opts = parser.parse_args()

assert(opts.file.endswith('.b'))

with open(opts.file, 'r') as r:
    dat = r.readlines()

assert(re.match(':- set\(noise, [0-9]+\)\.\n', dat[-1]))
dat[-1] = f':- set(noise, {opts.noise}).\n'

with open(opts.file, 'w') as w:
    w.writelines(dat)