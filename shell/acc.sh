pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/QArith/test_theory/plugins/setoid_ring.eval
label=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/QArith/test_theory/plugins/setoid_ring.label
python stats/acc.py --pred $pred --label $label
