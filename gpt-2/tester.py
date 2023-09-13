from datetime import datetime
import glob
import os
import sys

from sklearn.metrics import accuracy_score
import torch
from time import ctime
from torch import nn

sys.path.append(os.path.dirname(sys.path[0]))
from loader import *


class Test:
    def __init__(
        self,
        model,
        loader,
        tokenizer,
        tac_len,
        device,
        max_epochs=None,
        generate_args=None,
        log={},
    ):
        self.model = model
        self.epoch = 0
        self.loader = loader
        self.tokenizer = tokenizer
        self.max_epochs = max_epochs
        self.tac_len = tac_len
        self.lowerest_loss = float("+inf")
        self.lowerest_loss = 1000
        self.generate_args = generate_args
        self.log = log
        curDT = datetime.now()
        date_time = curDT.strftime("%m-%d-%Y-%H:%M:%S")

        self.pred_folder = os.path.join("pred", date_time)

        self.model_folder = os.path.join("trained_gpt", date_time)
        os.mkdir(self.model_folder)
        os.mkdir(self.pred_folder)
        self.log["model_folder"] = self.model_folder
        self.log["acc"] = []
        self.device = device

    def save_model(self):
        curDT = datetime.now()
        date_time = curDT.strftime("%m-%d-%Y-%H:%M:%S")

        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)

        models = glob.glob(f"{self.model_folder}/*/*.pt")
        for m in models:
            os.remove(m)

        model_folder = os.path.join(self.model_folder, date_time)
        os.mkdir(model_folder)

        torch.save(
            self.model.state_dict(), os.path.join(model_folder, f"e{self.epoch}.pt")
        )

    # def output(self, preds_lemma):
    #     pred_folder = os.path.join(self.pred_folder, date_time)
    # pred_file = os.path.join(pred_folder, f"e{self.epoch}.pred")
    # os.makedirs(pred_folder)

    # with open(pred_file, 'a') as f:
    #     for p in preds_lemma:
    #         f.write(f"{p}\n")

    def to_tac(self, line):
        # print('line', line)
        tac0 = line.split("Tactic:")[1].strip()
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
            batch["test"],
            return_tensors="pt",
            max_length=self.tokenizer.model_max_length - self.tac_len,
            truncation=True,
        )

        input_ids_ = input_ids["input_ids"].to("cuda")
        outputs = self.model.generate(
            inputs=input_ids_,
            max_length=self.tokenizer.model_max_length,
            pad_token_id=self.tokenizer.eos_token_id,
            **self.generate_args,
        )
        pred = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        pred = list((dict.fromkeys([self.to_tac(p) for p in pred])).keys())
        pred = '\t'.join(pred)
        return pred

    def pred_one(self):
        preds = []
        labels = []
        preds_lemma = []
        lemma_num = 0
        for _, row in enumerate(self.loader):
            if "lemma" in row.keys():
                lemma_num += 1
                preds_lemma.append(row["lemma"][0])
            else:
                # print(row)
                # exit()
                if row["test"] == [""]:
                    pred = ""
                else:
                    pred = self.pred_lm(row)
                preds.append(pred)
                preds_lemma.append(pred)
                labels = labels + row["tactic"]

        self.log["test state"] = len(self.loader)
        acc = accuracy_score(preds, labels)
        self.log["acc"].append(acc)

        if acc > self.lowerest_loss:
            self.lowerest_loss = acc
            self.save_model()
        return acc

    def valid(self):
        self.model.eval()
        self.log["start test"] = ctime()
        with torch.no_grad():
            acc = self.pred_one()
        self.log["end test"] = ctime()
        with open(os.path.join(self.pred_folder, "log.json"), "w") as w:
            json.dump(self.log, w, indent=4)
        return acc

    # def valid(self):
    #     self.model.eval()
    #     sum_loss = 0
    #     lemma_num = 0
    #     batch_num = 0
    #     with torch.no_grad():
    #         for _, batch in enumerate(self.loader):
    #             if "lemma" in batch.keys():
    #                 lemma_num += 1
    #             else:
    #                 self.pred_lm(batch)
    #                 batch_num += 1
    #                 input_ids = self.tokenizer(
    #                     batch["train"], truncation="longest_first", return_tensors="pt"
    #                 ).to(self.device)
    #                 # print('self.tokenizer.decode(input_ids)', self.tokenizer.batch_decode(input_ids['input_ids']))
    #                 outputs = self.model(**input_ids, labels=input_ids["input_ids"])
    #                 batch_loss, _ = outputs[:2]
    #                 sum_loss += batch_loss.detach().data

    #     avg_loss = sum_loss.item() / (batch_num - lemma_num)
    #     print(f"avg loss {avg_loss}")

    #     if avg_loss < self.lowerest_loss:
    #         self.lowerest_loss = avg_loss
    #         self.save_model()
    #     return avg_loss
