anonym=origin
param=p2n2
knn_pred=data/json/ortho/feat/tune/QArith/test_theory
test=data/json/ortho/predicate/$anonym/merge/test/
clause=data/json/ortho/feat/tune/QArith/test_theory/theories/ListsLogic/prop/origin/p2n2/good/15/alltac_rule.pl
theories=('theories/Sorting' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'theories/NArith')

bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/prop_bk.pl

for theory in ${theories[@]}; do
    (python filter.py --clause $clause \
        --pred $knn_pred/$theory.eval \
        --test $test/$theory \
        --label data/json/ortho/feat/merge/$theory.label \
        --bk $bk \
        --info prop/$anonym/$param) &
done
