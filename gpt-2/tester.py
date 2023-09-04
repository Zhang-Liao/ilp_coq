from datetime import datetime
import glob
import os
from unittest import loader

import torch
from time import ctime
from sklearn.metrics import accuracy_score

from lib import utils
from lib.global_options import *
from loader import *

class Test:
    def __init__(self, model, loader, tokenizer, task, tac_len, max_epochs = None, output_suffix = [], generate_args = None, log = {}):
        self.model = model 
        self.epoch = 0
        self.loader = loader 
        self.tokenizer = tokenizer
        self.task = task
        self.max_epochs = max_epochs
        self.tac_len = tac_len
        self.best_acc = -1
        self.smallest_loss = 1000
        self.generate_args = generate_args
        self.log = log    
        curDT = datetime.now()
        date_time = curDT.strftime("%m-%d-%Y-%H:%M:%S")

        self.pred_folder = os.path.join('pred', str(self.task), str(self.loader.dataset.feat), date_time)

        self.model_folder = os.path.join("trained_model", str(self.task), str(self.loader.dataset.feat), date_time, *output_suffix)

        self.log['model_folder'] = self.model_folder
        self.log['acc'] = []

    
    def shift_preds(self, k, preds):
        lemma_preds = []
        preds_ = []
        for p in preds:
            if global_options.lemma_delimiter in p:
                preds_ += utils.shift_lemma_preds(k, lemma_preds)
                lemma_preds = []
                preds_.append(p)
            else:
                lemma_preds.append(p)
        preds_ += utils.shift_lemma_preds(k, lemma_preds)
        return preds_

    def save_model(self, date_time):
        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)
        
        models = glob.glob(f'{self.model_folder}/*/*.pt')
        for m in models:
            os.remove(m)

        model_folder = os.path.join(self.model_folder, date_time)
        os.mkdir(model_folder)

        torch.save(self.model.state_dict(), os.path.join(model_folder, f"e{self.epoch}.pt"))

    def output(self, preds_lemma):

        curDT = datetime.now()
        date_time = curDT.strftime("%m-%d-%Y-%H:%M:%S")
        
        self.save_model(date_time)
    
        pred_folder = os.path.join(self.pred_folder, date_time)
        pred_file = os.path.join(pred_folder, f"e{self.epoch}.pred")
        os.makedirs(pred_folder)
        if isinstance(self.loader.dataset, LMParentDataset):
          preds_lemma = self.shift_preds(self.loader.dataset.k, preds_lemma)

        with open(pred_file, 'a') as f:
            for p in preds_lemma:
                f.write(f"{p}\n")   


    def to_tac (self, line):
        # print('line', line)
        tac0 = line.split('Tactic:')[1].strip()
        end_of_text_token = self.loader.dataset.end_of_text_token
        # print('tac0', tac0)
        if end_of_text_token in tac0:
            tac1 = tac0.split(end_of_text_token)[0].strip()
        else: 
            tac1 = tac0
        return tac1

    # test language model
    def pred_lm(self, batch):
        # if self.epoch == self.max_epochs -1:
        input_ids = self.tokenizer(
            batch['test'], 
            return_tensors = 'pt', 
            max_length = self.tokenizer.model_max_length - self.tac_len,
            truncation=True)
        
        input_ids_ = input_ids['input_ids'].to('cuda')
        outputs = self.model.generate(
            inputs = input_ids_, 
            max_length = self.tokenizer.model_max_length, 
            pad_token_id = self.tokenizer.eos_token_id,
            **self.generate_args
            )
        pred = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        pred = list((dict.fromkeys([self.to_tac(p) for p in pred])).keys())
        pred = '\t'.join(pred)
        # print('pred', pred_)
        return pred

    def pred_one(self):
        preds = []
        labels = []
        preds_lemma = []
        lemma_num = 0
        for _, row in enumerate(self.loader):
            if 'lemma' in row.keys():
                lemma_num += 1
                preds_lemma.append(row['lemma'][0])
            else:   
                # print(row)
                # exit()
                if row['test'] == ['']:
                    pred = ""
                else:
                    pred = self.pred_lm(row)
                preds.append(pred)
                preds_lemma.append(pred)
                labels = labels + row['tactic']

        self.log['test state'] = len(self.loader)
        acc = accuracy_score(preds, labels)
        self.log['acc'].append(acc)

        if acc > self.best_acc:   
            self.best_acc = acc
            self.output(preds_lemma)
        return acc

    def test(self):
        self.model.eval()
        self.log['start test'] = ctime()
        with torch.no_grad():
            acc = self.pred_one()
        self.log['end test'] = ctime()
        with open(os.path.join(self.pred_folder, 'log.json'), 'w') as w:
            json.dump(self.log, w, indent=4)    
        return acc