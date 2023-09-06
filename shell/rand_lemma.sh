# find theories/ plugins/ -name "*.json" | xargs grep -h "#lemma" > lemmas
dir=data/rand_lemmas
for i in {0..19}
do
    shuf $dir/lemmas > tmp
    head -n 1137 tmp > $dir/train$i
    tail -n 1137 tmp > $dir/test$i
done