knn_pred=data/json/origin_feat/tune/QArith/test_theory
# negs=(1 2 4 8 16 32)
# poss=(2 4 8 16 32)

negs=(4)
poss=(2)

anonym=anonym
descript=_id
train_descrip=$descript
bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_rel$descript\_bk.pl
kind=rel
test=data/json/predicate/$anonym/merge/test$descript/
# theories=('theories/Sorting' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'theories/NArith')
theories=('theories/Lists')
for theory in "${theories[@]}"; do
    for neg in "${negs[@]}"; do
        for pos in "${poss[@]}"; do
            (
                dir=data/json/predicate/$anonym/tune/QArith/train/$kind$train_descrip/p$pos\n$neg
                python filter.py --clause $dir/alltac_rule.pl \
                    --pred $knn_pred/$theory.eval \
                    --test $test/$theory \
                    --label data/json/origin_feat/merge/$theory.label \
                    --bk $bk \
                    --info $kind/$anonym$descript\_debug/p$pos\n$neg
            ) &
        done
    done
done
