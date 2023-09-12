import os
import re

dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto/neg10/rel1'

total = 0

for filename in os.listdir(dir):
    if os.path.splitext(filename)[-1] == '.b':
        with open(os.path.join(dir, filename), 'r') as r:
            dat = r.readlines()
        line = dat[-1]
        assert(re.match(':- set\(noise, [0-9]+\)\.\n', line))
        noise = line.split('set(noise,')[1]
        noise = int(noise.split(').')[0])
        total += noise

print(total)