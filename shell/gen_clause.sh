loop_gen() {
  complete=0
  file_len=${#0}
  file_base_end=$(($file_len - 3))
  file_base=${0:0:file_base_end}
  rule_file="${file_base}_rule.pl"
  if [[ ! $0 =~ "18259" ]]; then
    ( while [ $complete == 0 ]; do
      swipl $0 >/dev/null
      complete=$(python all_clause_generated.py --file "${rule_file}")
    done )
  fi
  echo 'finish' $0
}

export -f loop_gen
dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto/no_cluster2

# find $dir -name "*.b" | parallel python init_noise.py --file {}
# find $dir -name "*_rule.pl" | parallel rm {}
# find $dir -name "*.pl" | parallel -j 40 bash -c loop_gen
echo ":- style_check(-singleton).\n" > tmp
find $dir -name "*_rule.pl" | xargs -i cat {} >> tmp
mv tmp $dir/alltac_rule.pl
