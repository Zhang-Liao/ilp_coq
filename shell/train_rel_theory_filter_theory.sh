anonym=origin
param=p2n1
knn_pred=data/json/ortho/feat/tune/QArith/test_theory
test=data/json/ortho/predicate/$anonym/merge/test/
clause=data/json/ortho/feat/tune/QArith/test_theory/theories/ListsLogic/rel/origin/p2n1/good/15/alltac_rule.pl
theories=('theories/Sorting' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'theories/NArith')
valid=ListsLogic
bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/rel_noid_bk.pl

for theory in ${theories[@]}; do
    (python filter.py --clause $clause \
        --pred $knn_pred/$theory.eval \
        --test $test/$theory \
        --label data/json/ortho/feat/merge/$theory.label \
        --bk $bk \
        --info $valid/rel/$anonym/$param) &
done
