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

gen() {
  swipl $0 >/dev/null
  echo 'finish' $0
}

export -f loop_gen
export -f gen

for i in {2..4}; do
  dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/train/rel1_local/train0/noise$i
  # dir=data/json/predicate/rand_train_test/train/no_clst/rel1/train$i
  # find $dir -name "*.b" | parallel python init_noise.py --file {}
  cd $dir
  find $dir -name "*_rule.pl" | parallel rm {}
  # { time find $dir -name "*.pl" | parallel --timeout 20m -j 40 bash -c loop_gen ; } 2> $dir/timelog
  { time find $dir -name "*.pl" | parallel --timeout 5m -j 40 bash -c gen ; } 2> $dir/timelog
  echo ":- style_check(-singleton)." > $dir/tmp
  find $dir -name "*_rule.pl" | xargs -i cat {} >> $dir/tmp
  mv $dir/tmp $dir/alltac_rule.pl
done
