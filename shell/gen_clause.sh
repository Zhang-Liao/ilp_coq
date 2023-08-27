loop_gen() {
  complete=1
  file_len=${#0}
  file_base_end=$(($file_len - 3))
  file_base=${0:0:file_base_end}
  rule_file="${file_base}_rule.pl"
  while [ $complete == 1 ]; do
    swipl $0
    complete=$(python all_clause_generated.py --file "${rule_file}")
    echo $rule_file
    echo $complete
  done
}

export -f loop_gen
dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto
# find $dir -name "*.log" | parallel rm {}
# find $dir -name "*_rule.pl" | parallel rm {}
# find $dir -name "*.pl" | parallel -j 4 swipl {}
# python post_proc_claus.py --dir $dir
# find $dir -name "*_rule.pl" | xargs -i cat {} >tmp
find $dir -name "*.pl" | xargs -d'\n' -t -n1 bash -c 'loop_gen'
# mv tmp alltac_rule.pl
