kind=prop
anonym=anonym
param=p2n1
descript=''
knn_pred=data/json/ortho/feat/tune/QArith/test_theory
test=data/json/ortho/predicate/$anonym/merge/test$descript/
valid=valid
clause=data/json/ortho/feat/tune/QArith/test_theory/valid/valid/prop/anonym/p2n1/good/15/alltac_rule.pl
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')
# theories=('theories/PArith' 'theories/Numbers' 'plugins/btauto' 'theories/Arith' 'theories/Strings')
bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_prop_bk.pl

for theory in ${theories[@]}; do
    (
        python filter.py --clause $clause \
            --pred $knn_pred/$theory.eval \
            --test $test/$theory \
            --label data/json/ortho/feat/merge/$theory.label \
            --bk $bk \
            --info $valid/$kind$descript/$anonym/$param
    )&
done
