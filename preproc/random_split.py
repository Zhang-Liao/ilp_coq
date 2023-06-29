import os
import sys
from pathlib import Path
sys.path.append(os.path.dirname(sys.path[0]))
from lib import global_setting
from lib import utils

lemma_split_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/lemma_split'
dataset = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/syn_vertical2'
out_dir = os.path.join(dataset, 'ten_split')
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
    
def load_split_lemmas():
    split_lemmmas = []
    for root, _, files in os.walk(lemma_split_dir):
        for i in range(len(files)):
            with open(os.path.join(root, 'split'+str(i)+'.txt'), 'r') as f:
                split_lemmmas.append(list(map(lambda x: x.strip(), f.readlines())))
    return split_lemmmas

def stats(data):
    lemma_num = len(data)
    state_num = 0
    for lemma in data:
        state_num += len(lemma)
    return lemma_num, state_num
    # print('lemma number', lemma_num)
    # print('state number', state_num)

def output_lemma(data, lemma, split_lemmas):
    flag = True
    for i in range(len(split_lemmas)):
        split_lemma = split_lemmas[i]
        if lemma in split_lemma:
            utils.output_lemma_aux(lemma, data, os.path.join(out_dir, 'split'+str(i)+".json"))
            flag = False
    if flag:
        print(lemma+"not in any split")

split_lemmas = load_split_lemmas()
for root, _, files in os.walk(dataset):
    for file in files:
        lemma_states = []
        if Path(file).suffix == '.json':
            path = os.path.join(root, file)
            with open(path, 'r') as reader:
                for line in reader:
                    line = line.strip()
                    if global_setting.lemma_delimiter not in line:
                        lemma_states.append(line)
                    else:
                        if lemma_states != []:
                            # print('append lemma with', len(lemma_states), 'states')
                            output_lemma(lemma_states, lemma, split_lemmas)
                        lemma = utils.lemma_name(line)
                        lemma_states = []
                # the last lemma in a file
                if lemma_states != []:
                    output_lemma(lemma_states, lemma, split_lemmas)