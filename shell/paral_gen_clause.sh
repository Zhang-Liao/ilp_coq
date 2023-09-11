loop_gen() {
  complete=0
  file_len=${#0}
  file_base_end=$(($file_len - 3))
  file_base=${0:0:file_base_end}
  rule_file="${file_base}_rule.pl"
  while [ $complete == 0 ]; do
    # swipl $0
    swipl $0 >/dev/null
    complete=$(python all_clause_generated.py --file "${rule_file}")
  done
  echo 'finish' $0
}

export -f loop_gen

pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test
test=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/test/prop
# all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_predc.pl
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_prop_predc.pl

for i in {3..5}; do
  dir=data/json/predicate/rand_train_test/train/rel2/train$i
  # dir=data/json/predicate/rand_train_test/predc/neg10rel/train$i
 
  find $dir -name "*.b" | parallel python init_noise.py --file {}

  find $dir -name "*_rule.pl" | parallel rm {}
  { time find $dir -name "*.pl" | parallel --timeout 20m -j 40 bash -c loop_gen ; } 2> $dir/timelog
  echo ":- style_check(-singleton)." > $dir/tmp
  find $dir -name "*_rule.pl" | xargs -i cat {} >> $dir/tmp
  mv $dir/tmp $dir/alltac_rule.pl
  # (python filter.py --clause $dir/alltac_rule.pl --pred $pred/test$i.eval --test $test/test$i --label $pred/test$i.label --all_predc $all_predc)&
done
