import os
import random

dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/rand_lemmas'
# f_lemmas = ''

with open(os.path.join(dir, 'lemmas'), 'r') as r:
    lemmas = r.readlines()

for i in range(20):
    with open(os.path.join(dir, f'train{i}'), 'r') as r:
        train = set(r.readlines())

    with open(os.path.join(dir, f'test{i}'), 'r') as r:
        test = set(r.readlines())

    tmp_lemmas = lemmas.copy()
    random.shuffle(tmp_lemmas)        
    tmp_lemmas = set(tmp_lemmas)
    left = tmp_lemmas.difference(train.union(test))
    valid = list(left)[:1137]    
    
    with open(os.path.join(dir, f'valid{i}'), 'w') as w:
        w.writelines(valid)
