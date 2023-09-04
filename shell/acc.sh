pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split/06-27-2023-10:26:47/split8.eval
label=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split/split8.label
python stats/acc.py --pred $pred --label $label
