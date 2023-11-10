knn_pred=data/json/origin_feat/tune/QArith/test_theory
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_predc.pl
negs=(1 2 4 8 16 32)
poss=(2 4 8 16 32)
anonym=origin
kind=rel
test=data/json/predicate/$anonym/merge/test/
# theories=('theories/Classes' 'theories/Lists' 'theories/Numbers')
theories=('theories/Sorting' 'theories/Numbers')
for theory in "${theories[@]}"; do
    for neg in "${negs[@]}"; do
        (

            for pos in "${poss[@]}"; do

                dir=data/json/predicate/$anonym/tune/QArith/train/$kind/p$pos\n$neg
                python filter.py --clause $dir/alltac_rule.pl \
                    --pred $knn_pred/$theory.eval \
                    --test $test/$theory \
                    --label data/json/origin_feat/merge/$theory.label \
                    --all_predc $all_predc \
                    --info $kind/$anonym/p$pos\n$neg

            done
        ) &
    done
done
