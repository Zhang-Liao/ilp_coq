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

gen() {
  swipl $0 >/dev/null
  echo 'finish' $0
}

export -f loop_gen
export -f gen

dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/train/rel1_noise1/train0
pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test0.eval
label=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test0.label
test=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/test/prop/test0
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_rel1_predc.pl

cd $dir
# find $dir -name "*.b" | parallel python init_noise.py --file {}
# find . -name "*_rule.pl" | parallel rm {}
# time find . -name "*.pl" | parallel --timeout 20m -j 40 bash -c loop_gen
# time find . -name "*.pl" | parallel --timeout 5m -j 40 bash -c gen

# echo ":- style_check(-singleton)." > tmp
# find $dir -name "*_rule.pl" | xargs -i cat {} >> tmp
# mv tmp $dir/alltac_rule.pl

cd -
python filter.py --clause $dir/alltac_rule.pl --pred $pred --test $test --label $label --all_predc $all_predc