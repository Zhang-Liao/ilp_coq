pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test
test=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/test/prop
# all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_predc.pl
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_rel2_predc.pl
# all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_prop_predc.pl
for i in {0..5}; do
  dir=data/json/predicate/rand_train_test/train/rel2/train$i
  # dir=data/json/predicate/rand_train_test/predc/neg10rel/train$i
  (python filter.py --clause $dir/alltac_rule.pl --pred $pred/test$i.eval --test $test/test$i --label $pred/test$i.label --all_predc $all_predc)&
done
