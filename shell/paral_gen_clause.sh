gen() {
  swipl $0 >/dev/null
  echo 'finish' $0
}

export -f gen

# pred=data/json/origin_feat/2percent_split
# test=data/json/predicate/anonym/2percent_split/test/anonym/rel
# all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_predc.pl

negs=(1 2 4 8 16 32)
poss=(2 4 8 16 32)

# for neg in "${negs[@]}"; do
neg=1
for pos in "${poss[@]}"; do
  for i in {0..9}; do
    (
      # echo $i $neg $pos
      dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/anonym/tune/MSets/train/rel/p$pos\n$neg/train$i
      cd $dir
      # find . -name "*_rule.pl" | parallel echo {}
      # find . -name "*_rule.pl" | parallel rm {}
      time find $dir -name "*.pl" | parallel --timeout 10m -j 10 bash -c gen
      echo ":- style_check(-singleton)." >tmp
      find . -name "*_rule.pl" | xargs -i cat {} >>tmp
      cd -
      python clean_rule.py --file $dir/tmp
      mv $dir/tmp $dir/alltac_rule.pl
      # python filter.py --clause $dir/alltac_rule.pl --pred $pred/test$i.eval --test $test/test$i --label $pred/test$i.label --all_predc $all_predc
    ) &
  done
done
# done
