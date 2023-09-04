import os
from time import ctime

from transformers import GPT2LMHeadModel
from transformers import GPT2TokenizerFast
from torch.utils.data import DataLoader
from torch.optim import AdamW
import transformers

sys.path.append(os.path.dirname(sys.path[0]))
from loader import *
import trainer
import tester

generate_args = {
    'num_beams': 3,
    'num_return_sequences' : 1,
}

device = 'cuda'
epochs = 25
tac_len = 50
warm_ratio = 0.2
eta = 3e-4
batch_size = 32
model_name = 'gpt2' 
data_dir = '/home/zhanglia/tac_seman/gpt-2/data/2023/tree_diff/id_hash/ten_split'
train_f = 'split0_7.json'
test_f = 'split8.json'
train_path = os.path.join(data_dir, train_f)
test_path = os.path.join(data_dir, test_f)

log = {
    'test path': str(test_path),
    'generate args': generate_args,
    'epochs': epochs,
    'tac_len': tac_len,
    'warm_ratio': warm_ratio,
    'eta' : eta, 
    'batch_size': batch_size,
    'model': model_name,
    'train_path': train_path
}

print(log)

def init_trainier(train_dataset, tokenizer, model):
    train_loader = DataLoader(train_dataset, batch_size = 1, shuffle = True)

    optimizer = AdamW(model.parameters(), lr = eta)
    total_steps = int((len(train_dataset)/batch_size) * epochs)
    scheduler = transformers.get_linear_schedule_with_warmup(
        optimizer, 
        num_warmup_steps= int(warm_ratio * total_steps),  
        num_training_steps = total_steps)
    trainer_ = trainer.Train(model, train_loader, optimizer, scheduler, tokenizer, batch_size, device)
    return trainer_

def eval(train_dataset, tokenizer, test_dataset, model):
    model = model.to(device)
    trainer_ = init_trainier(train_dataset, tokenizer, model)
    test_loader = DataLoader(test_dataset, batch_size = 1, shuffle = False) 
    tester_ = tester.Test(model, test_loader, tokenizer, tac_len, max_epochs = epochs, generate_args = generate_args, log = log)
    train_loss = []
    test_acc = []
    for epoch in range(epochs):
        print(f"EPOCH {epoch} started" + '=' * 30)
        trainer_.epoch = epoch
        print ("Start training:", ctime())
        tr_loss = trainer_.train()
        train_loss.append(tr_loss)
        print ("End training:", ctime())
        tester_.model = trainer_.model
        tester_.epoch = epoch
        print ("Start testing:", ctime())
        tt_acc = tester_.test()
        test_acc.append(tt_acc)
        print ("End testing:", ctime())
        
    log['train_loss'] = train_loss
    log['test_acc'] = test_acc     
    with open(os.path.join(tester_.pred_folder, 'eval.json'), 'w') as w:
        json.dump(log, w, indent=4)          
    print('train_loss', train_loss)
    print('test_acc', test_acc)     
    
def init_truncate():
    return 'left'

def load_tokenizer(gpt, trunc):
    token_dir = gpt
    config = {
        'truncation_side' : trunc
    }
    tokenizer = GPT2TokenizerFast.from_pretrained(token_dir, **config)
    # print(vars(tokenizer))
    return tokenizer


train_dataset = LMDataset(train_path)
test_dataset = LMDataset(test_path)

model = GPT2LMHeadModel.from_pretrained(model_name)
    
tokenizer = load_tokenizer(model_name, init_truncate())
eval(train_dataset, tokenizer, test_dataset,model)


