gen() {
  swipl $0 >/dev/null
  echo 'finish' $0
}

export -f gen

negs=(1 2 4 8 16)
poss=(2 4 8 16)

anonym=origin
kind=rel
for neg in "${negs[@]}"; do
  (

    for pos in "${poss[@]}"; do
      dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/rev_ortho/predicate/$anonym/tune/QArith/train/$kind/p$pos\n$neg
      cd $dir
      find $dir -name "*_rule.pl" | parallel rm {}
      time find $dir -name "*.pl" | parallel --timeout 5m -j 10 bash -c gen
      echo ":- style_check(-singleton)." >tmp_rule.pl
      find . -name "*_rule.pl" | xargs -i cat {} >>tmp_rule.pl
      cd -
      python post_proc_rule.py --file $dir/tmtmp_rule.plp
      mv $dir/tmp_rule.pl $dir/alltac_rule.pl
    done
  ) &
done
