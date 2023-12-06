# noarity=_noarity
descript=_id
knn_pred=data/json/origin_feat/tune/QArith/test_theory
bk=prolog/anonym_prop_bk.pl

negs=(1 2 4 8 16 32)
poss=(2 4 8 16 32)

anonym=anonym
kind=prop
test=data/json/predicate/$anonym/merge/test$descript/
# theories=('theories/Sorting' 'theories/NArith' 'theories/Init' 'theories/Vectors' 'plugins/setoid_ring')
theories=('theories/Lists')

for theory in "${theories[@]}"; do
    for neg in "${negs[@]}"; do
        for pos in "${poss[@]}"; do
            (
                dir=data/json/predicate/$anonym/tune/QArith/train/$kind/p$pos\n$neg
                python filter.py --clause $dir/alltac_rule.pl \
                    --pred $knn_pred/$theory.eval \
                    --test $test/$theory \
                    --label data/json/origin_feat/merge/$theory.label \
                    --bk $bk \
                    --info prop/$anonym$descript/p$pos\n$neg
            ) &
        done
    done
done
