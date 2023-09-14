loop_gen() {
  complete=0
  file_len=${#0}
  file_base_end=$(($file_len - 3))
  file_base=${0:0:file_base_end}
  rule_file="${file_base}_rule.pl"
  while [ $complete == 0 ]; do
      swipl $0 >/dev/null
      complete=$(python /home/zhangliao/ilp_out_coq/ilp_out_coq/all_clause_generated.py --file "${rule_file}")
  done 
  echo 'finish' $0
}

export -f loop_gen
dir=data/json/predicate/rand_train_test/train/rel1_test/train0

cd $dir
# find $dir -name "*.b" | parallel python init_noise.py --file {}
find . -name "*_rule.pl" | parallel rm {}
time find . -name "*.pl" | parallel --timeout 1m -j 40 bash -c loop_gen
# cd -
# echo ":- style_check(-singleton)." > tmp
# find $dir -name "*_rule.pl" | xargs -i cat {} >> tmp
# mv tmp $dir/alltac_rule.pl

