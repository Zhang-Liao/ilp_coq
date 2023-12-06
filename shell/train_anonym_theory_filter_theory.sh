kind=rel
anonym=anonym
param=p2n16
descript=_id
knn_pred=data/json/origin_feat/tune/QArith/test_theory
test=data/json/predicate/$anonym/merge/test$descript/
clause=data/json/predicate/anonym/tune/QArith/train/$kind$descript/p2n16/alltac_rule.pl
theories=('theories/Sorting' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'theories/NArith')
# theories=('theories/NArith' 'theories/Arith' 'theories/Sets' 'theories/MSets')

bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_rel$descript\_bk.pl

for theory in ${theories[@]}; do
    (
        python filter.py --clause $clause \
            --pred $knn_pred/$theory.eval \
            --test $test/$theory \
            --label data/json/origin_feat/merge/$theory.label \
            --bk $bk \
            --info $kind/$anonym$descript/$param
    ) &
done
