import json

from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset

from lib import global_options


def anti_to_str(antis):
    l = []
    for r in antis: 
        l.append({
            'subst': r['substs'],
            'del hyps':r['del hyps'],  
            'ins hyps':r['ins hyps']
        })
    return l

def anti_diff_to_str(before, antis):
    if antis == []:
        rs = before + ' Qed'
    else:
        rs = anti_to_str(antis)
    return rs

def anti_full_to_str(before, antis):
    if antis == []:
        rs = before + ' Qed'
    else:
        rs = anti_to_str(antis)
        for i in range(len(rs)): 
            rs[i]['lgg'] = antis[i]['lgg']
    return rs

def tree_diff_change(before, diffs):
    if diffs == []:
        rs = before + ' Qed'
    else:
        rs = []
        for r in diffs: 
            rs.append({
                'change': r['change'],
                'hole':r['hole'],  
            })
    return rs

def tree_diff_patch(before, diffs):
    if diffs == []:
        rs = before + ' Qed'
    else:
        rs = []
        for r in diffs: 
            rs.append({
                'patch': r['patch'],
                'hole':r['hole'],  
            })
    return rs

def to_row (input, tac, fail):
    if fail == ['fail']:
        input = 'fail'
    return {'input':input, 'tactic':tac}

def lm_test (l, feat):
    if feat == global_options.Feat.Before:
        test_input = f"Before:{l['before']} Tactic:"
    elif feat == global_options.Feat.BeforeAfter:
        test_input = f"Before:{l['before']} After:{l['after']} Tactic:"
    elif feat == global_options.Feat.AntiDiff:
        test_input = "Anti:" + json.dumps(anti_diff_to_str(l['before'], l['anti'])) + " Tactic:"
    elif feat == global_options.Feat.AntiFull:
        test_input = "Anti:" + json.dumps(anti_full_to_str(l['before'], l['anti'])) + " Tactic:"
    elif feat == global_options.Feat.TreeDiffChange:
        test_input = "TreeDiff:" + json.dumps(tree_diff_change(l['before'], l['tree diff'])) + " Tactic:"  
    elif feat == global_options.Feat.TreeDiffPatch:
        test_input = "TreeDiff:" + json.dumps(tree_diff_patch(l['before'], l['tree diff'])) + " Tactic:"  
    elif feat == global_options.Feat.ILP:
        test_input = f"{l['before']} Tactic:"
    return test_input

def lm_test_parent (p, feat, st):
    if feat == global_options.Feat.Before:
        test_input = f"Before:{p['before']} Tactic:"
    elif feat == global_options.Feat.BeforeAfter:
        test_input = f"Before:{p['before']} After:{st['after']} Tactic:"
    elif feat == global_options.Feat.AntiDiff:
        test_input = "Anti:" + json.dumps(anti_diff_to_str(p['before'], p['anti'])) + " Tactic:"
    elif feat == global_options.Feat.AntiFull:
        test_input = "Anti:" + json.dumps(anti_full_to_str(p['before'], p['anti'])) + " Tactic:"
    elif feat == global_options.Feat.TreeDiffChange:
        test_input = "TreeDiff:" + json.dumps(tree_diff_change(p['before'], p['tree diff'])) + " Tactic:"          
    elif feat == global_options.Feat.TreeDiffPatch:
        test_input = "TreeDiff:" + json.dumps(tree_diff_patch(p['before'], p['tree diff'])) + " Tactic:"
    return test_input

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
    def __init__(self, path, feat):
        super().__init__()
        self.feat = feat
        self.add_file_data(path, feat)

    def add_file_data(self, path, feat):
        with open(path) as f:
            for l in f:
                l = l.strip()
                if global_options.lemma_delimiter in l:
                    self.data.append({'lemma':l})
                else:
                    l = json.loads(l)
                    test_input = lm_test(l, feat)
                    train_input = test_input + f"{l['tac str'].strip()} {self.end_of_text_token}"
                    self.data.append({'train': train_input, 'test': test_input, 'tactic':l['tac str'].strip()})

class LMParentDataset(CoqDataset):
    def __init__(self, path, feat, k):
        super().__init__()
        self.feat = feat
        self.k = k
        self.add_file_data(path)
        
    def add_file_data(self, path):
        with open(path) as f:
            for l in f:
                l = l.strip()
                if global_options.lemma_delimiter in l:
                    self.data.append({'lemma':l})
                else:                    
                    # i += 1
                    l = json.loads(l)
                    parents = l['parents']
                    if self.k > len(parents):
                        test_input = ""
                        self.data.append({
                            'test': "",
                            'tactic':""})
                    else:
                        parent = parents[self.k - 1]
                        test_input = lm_test_parent(parent, self.feat, l)                      
                        # print('test_input', test_input)
                        # if i == 10:
                            # exit()
                        self.data.append({
                            'test': test_input,
                            'tactic':parent['tac str'].strip()})
