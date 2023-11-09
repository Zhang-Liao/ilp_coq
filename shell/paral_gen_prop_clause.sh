gen() {
  swipl $0 >/dev/null
  echo 'finish' $0
}

export -f gen

# negs=(1 2 4 8 16 32)
# poss=(2 4 8 16 32)

negs=(16)
poss=(4)

for neg in "${negs[@]}"; do
  for pos in "${poss[@]}"; do
    for i in {0..9}; do
      (
        dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/origin/rand_1000/train/prop/p$pos\n$neg/train$i
        cd $dir
        rm alltac_rule.pl
        time find $dir -name "*.pl" | parallel --timeout 10m -j 10 bash -c gen
        echo ":- style_check(-singleton)." >tmp
        find . -name "*_rule.pl" | xargs -i cat {} >>tmp
        cd -
        python clean_rule.py --file $dir/tmp
        mv $dir/tmp $dir/alltac_rule.pl
      ) &
    done
  done
done
