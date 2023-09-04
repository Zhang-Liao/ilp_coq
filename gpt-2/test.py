import os
from time import ctime

from transformers import GPT2LMHeadModel
from transformers import GPT2TokenizerFast
from torch import load
from torch.utils.data import DataLoader

from lib.global_options import * 
from loader import *
import tester

max_seq_len = 1024
batch_size = 32
device = 'cuda'
model_name = 'gpt2'
data_dir = '/home/zhanglia/tac_seman/gpt-2/data/redundant/ten_split'
test_f = 'split0_7.json'
test_path = os.path.join(data_dir, test_f)
tac_len = 50
epochs = 1
task = Task.LMHeadGen
model_path = ''

feat = Feat.TreeDiffPatch
generate_args = {
    'num_beams': 3,
    'num_return_sequences' : 1,
}

log = {
    'feat': str(feat),
    'test path': str(test_path),
    'generate args': generate_args,
    'epochs': epochs,
    'tac_len': tac_len,
    'batch_size': batch_size,
    'model': model_name,
    'model_path':model_path
}

def load_tokenizer(model_name):
    token_dir = model_name
    config = {
        'truncation_side' : 'left'
    }
    tokenizer = GPT2TokenizerFast.from_pretrained(token_dir, **config)
    # print(vars(tokenizer))
    # exit() 
    return tokenizer

# test_dataset = LMDataset(test_path, feat)
test_dataset = LMParentDataset(test_path, feat, 1)

model = GPT2LMHeadModel.from_pretrained(model_name)
model.load_state_dict(load(model_path))
    
    
model = model.to(device)
tokenizer = load_tokenizer(model_name)
# tokenizer.pad_token = tokenizer.eos_token
# print('model', model_path)
# print('task', task)
# print('feat', feat)
# print('test path', test_path)

test_loader = DataLoader(test_dataset, batch_size = 1, shuffle = False) 
tester_ = tester.Test(model, test_loader, tokenizer, task, tac_len, max_epochs = epochs, generate_args = generate_args, log = log)
tester_.test()
