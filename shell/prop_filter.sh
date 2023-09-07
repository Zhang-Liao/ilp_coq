clause='/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto/neg10/prop/alltac_rule.pl'
pred='/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split/eval/train_split0/split8.eval'
test='/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split8/test_predc/prop'
label='/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/ten_split/split8.label'
all_predc='/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_prop_predc.pl'
python filter.py --clause $clause --pred $pred --test $test --label $label --all_predc $all_predc