clause=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/rules/prop
pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test0.eval
test=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/test/prop/test0
label=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test0.label
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_prop_predc.pl
tac=simpl
python stat_tac_filter.py --clause $clause --pred $pred --test $test --label $label --all_predc $all_predc --tac simpl