pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets
test=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/anonym/tune/MSets/test/rel
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_predc.pl
negs=(1 2 4 8 16 32)
poss=(2 4 8 16 32)

for neg in "${negs[@]}"; do
  for pos in "${poss[@]}"; do
    (for i in {0..9}; do
      dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/anonym/tune/MSets/train/rel/p$pos\n$neg/train$i
      python filter.py --clause $dir/alltac_rule.pl --pred $pred/test$i.eval --test $test/test$i --label $pred/test$i.label --all_predc $all_predc
    done) &
  done
done
