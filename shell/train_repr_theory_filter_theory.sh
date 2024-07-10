train_theory=Structures
anonym=origin
param=p1n1
knn_pred=data/json/feat/tune/$train_theory/test_theory
test=data/json/predicate/$anonym/merge/test/
clause=data/json/feat/tune/Structures/test_theory/valid/valid/repr/origin/p1n1/good/12/alltac_rule.pl
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')

valid=valid
bk=prolog/repr_bk.pl
kind=repr
for theory in ${theories[@]}; do
    (python filter.py --clause $clause \
        --pred $knn_pred/$theory.eval \
        --test $test/$theory \
        --label data/json/feat/merge/$theory.label \
        --bk $bk \
        --info $valid/$kind/$anonym/$param) &
done
