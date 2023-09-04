
import torch

from lib.global_options import *
from lib import utils

class Train:
    def __init__(self, model, loader, optimizer, scheduler, tokenizer, batch_size, device, task):
        self.model = model 
        self.epoch = 0
        self.loader = loader
        self.optimizer = optimizer
        self.scheduler = scheduler 
        self.tokenizer = tokenizer
        self.batch_size = batch_size
        self.device = device
        self.task = task
        torch.manual_seed(4391)

    def train(self):
        sum_loss = 0
        proc_seq_count = 0
        batch_num = len(self.loader)
        lemma_num = 0
        for _, batch in enumerate(self.loader):
            if 'lemma' in batch.keys():
                lemma_num += 1
            else:
                input_ids = self.tokenizer(batch['train'], truncation = 'longest_first', return_tensors = 'pt').to(self.device)
                # print('self.tokenizer.decode(input_ids)', self.tokenizer.batch_decode(input_ids['input_ids']))
                outputs = self.model(**input_ids, labels = input_ids['input_ids'])
                loss, _ = outputs[:2]
                loss.backward()
                step_loss = loss.detach().data
                sum_loss += step_loss

                proc_seq_count = proc_seq_count + 1
                if proc_seq_count == self.batch_size:
                    proc_seq_count = 0    
                    self.optimizer.step()
                    self.scheduler.step() 
                    self.optimizer.zero_grad()
                    self.model.zero_grad()


        # print('sum_loss', sum_loss)
        # print('sum_loss.item()', sum_loss.item())
        avg_loss = sum_loss.item()/(batch_num - lemma_num)
        print(f"avg loss {avg_loss}")
        return avg_loss
