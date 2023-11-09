pred=data/json/origin_feat/rand_1000
# negs=(1 2 4 8 16 32)
negs=(32)
# poss=(2 4 8 16 32)
poss=(4)
anonym=anonym
kind=rel
test=data/json/predicate/$anonym/rand_1000/test
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_predc.pl

for neg in "${negs[@]}"; do
    for pos in "${poss[@]}"; do
        for i in {0..0}; do
            (
                dir=data/json/predicate/$anonym/rand_1000/train/$kind/p$pos\n$neg/train$i
                python filter.py --clause $dir/alltac_rule.pl --pred $pred/valid$i.eval --test $test/valid$i --label $pred/valid$i.label --all_predc $all_predc --info $kind/$anonym/p$pos\n$neg
            ) &
        done

    done
done
