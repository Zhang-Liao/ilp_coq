import json
import os
import sys

from torch.utils.data import Dataset

sys.path.append(os.path.dirname(sys.path[0]))
from lib import utils


def to_row (input, tac, fail):
    if fail == ['fail']:
        input = 'fail'
    return {'input':input, 'tactic':tac}

def lm_test (l):
    return f"Before:{l['before']} Tactic:"

def lm_test_parent (p):
    return f"Before:{p['before']} Tactic:"

class CoqDataset(Dataset):
    def __init__(self):
        super().__init__()
        self.data = []
        self.end_of_text_token = "<|endoftext|>"
        
    def __len__(self):
        return len(self.data)              

    def __getitem__(self, item):
        return self.data[item]

class LMDataset(CoqDataset):
    def __init__(self, path):
        super().__init__()
        self.add_file_data(path)

    def add_file_data(self, path):
        with open(path) as f:
            for l in f:
                l = l.strip()
                if utils.LEMMA in l:
                    self.data.append({'lemma':l})
                else:
                    l = json.loads(l)
                    test_input = lm_test(l)
                    train_input = test_input + f"{l['tac str'].strip()} {self.end_of_text_token}"
                    self.data.append({'train': train_input, 'test': test_input, 'tactic':l['tac str'].strip()})
