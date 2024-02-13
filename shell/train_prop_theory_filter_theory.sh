train_theory=Structures
anonym=origin
param=p1n1
knn_pred=data/json/ortho/feat/tune/$train_theory/test_theory
test=data/json/ortho/predicate/$anonym/merge/test/
clause=data/json/ortho/feat/tune/Structures/test_theory/valid/valid/prop/origin/p1n1/good/10/alltac_rule.pl
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')
valid=valid
bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/prop_bk.pl
kind=prop
for theory in ${theories[@]}; do
    (python filter.py --clause $clause \
        --pred $knn_pred/$theory.eval \
        --test $test/$theory \
        --label data/json/ortho/feat/merge/$theory.label \
        --bk $bk \
        --info $valid/$kind/$anonym/$param) &
done
