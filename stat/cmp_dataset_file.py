import os
import sys

data1 = set()
data2 = set()

with open('/home/zhangliao/ilp_out_coq/data/json_log') as f:
    for l in f:
        l = l.strip()
        l = l.split('.')
        data1.add(l[0])

with open('/home/zhangliao/ilp_out_coq/data/sexpr_log') as f:
    for l in f:
        l = l.strip()
        l = l.split('.')
        data2.add(l[0])

print('data1 - data2')
print(data1 - data2)
print('data2 - data1')
print(data2 - data1)
