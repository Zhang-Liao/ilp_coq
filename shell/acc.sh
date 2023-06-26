pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/split8.eval
label=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/split8.label

python stat/acc.py --pred $pred --label $label
