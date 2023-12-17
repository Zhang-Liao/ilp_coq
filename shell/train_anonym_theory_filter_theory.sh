kind=rel
anonym=anonym
param=p4n1
descript=''
knn_pred=data/json/ortho/feat/tune/QArith/test_theory
test=data/json/ortho/predicate/anonym/merge/test$descript/
clause=data/json/ortho/feat/tune/QArith/test_theory/theories/ListsLogic/rel/anonym/p4n1/good/20/alltac_rule.pl
theories=('theories/Sorting' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'theories/NArith')
# theories=('theories/NArith' 'theories/Arith' 'theories/Sets' 'theories/MSets')
valid=ListsLogic
bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_rel_id_bk.pl

for theory in ${theories[@]}; do
    (
        python filter.py --clause $clause \
            --pred $knn_pred/$theory.eval \
            --test $test/$theory \
            --label data/json/ortho/feat/merge/$theory.label \
            --bk $bk \
            --info $valid/$kind$descript/$anonym/$param
    ) &
done
