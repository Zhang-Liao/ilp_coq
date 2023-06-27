pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/split8.eval
label=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/split8.label
train=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/split0.feat
python stat/acc.py --pred $pred --label $label --train $train
