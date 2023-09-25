gen() {
  swipl $0 >/dev/null
  echo 'finish' $0
}

export -f gen

dir=data/json/predicate/rand_train_test/train/rel/pos50neg10/train2
pred=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test2.eval
label=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test/test2.label
test=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/test/rel/test2
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_predc.pl

cd $dir
find . -name "*_rule.pl" | parallel rm {}

time find . -name "*.pl" | parallel --timeout 10m -j 40 bash -c gen

echo ":- style_check(-singleton)." > tmp
find . -name "*_rule.pl" | xargs -i cat {} >> tmp
cd -

python clean_rule.py --file $dir/tmp
mv $dir/tmp $dir/alltac_rule.pl
python filter.py --clause $dir/alltac_rule.pl --pred $pred --test $test --label $label --all_predc $all_predc