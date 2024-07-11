gen() {
  swipl $0 >/dev/null
  echo 'finish' $0
}


export -f gen
# poss=(1 2 4 8 16 32)
# negs=(0 1 2 4 8 16 32 64)
poss=(4)
negs=(4)

train_theory=Structures
anonym=origin
kind=repr
for neg in "${negs[@]}"; do
  (
    for pos in "${poss[@]}"; do
      dir=data/json/predicate/$anonym/tune/$train_theory/train/$kind/p$pos\n$neg
      cd $dir
      find . -name "*_rule.pl" | parallel rm {}
      time find . -name "*.pl" | parallel --timeout 10m -j 5 bash -c gen
      echo ":- style_check(-singleton)." >tmp
      find . -name "*_rule.pl" | xargs -i cat {} >>tmp
      cd -
      python post_proc_rule.py --file $dir/tmp
      mv $dir/tmp $dir/alltac_rule.pl
    done
  ) &
done
