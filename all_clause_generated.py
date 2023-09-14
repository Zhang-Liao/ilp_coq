import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)
opts = parser.parse_args()

assert(opts.file.endswith('_rule.pl'))
completed = 1

if not os.path.exists(opts.file):
    completed = 0
else:
    with open(opts.file) as r:
        for l in r:
            l = l.strip()
            if l.startswith('tac(') & l.endswith(').'):
                completed = 0
                break

if completed == 0:
    base = opts.file[:-8]
    bk = base + '.b'

    with open(bk, 'r') as r:
        dat = r.readlines()

    for i in range(len(dat)):
        line = dat[i]
        if re.match(':- set\(noise, [0-9]+\)\.\n', line):
            noise = line.split('set(noise,')[1]
            noise = int(noise.split(').')[0])
            noise += 1
            dat[i] = f':- set(noise, {noise}).\n'
            # dat[i] = f'set(noise, 1000)\n'
            break

    with open(bk, 'w') as w:
        w.writelines(dat)

print(completed)