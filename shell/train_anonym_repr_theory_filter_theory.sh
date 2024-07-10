kind=repr
anonym=anonym
param=p16n1
descript=''
train_theory=Structures
knn_pred=data/json/feat/tune/$train_theory/test_theory
test=data/json/predicate/$anonym/merge/test$descript/
valid=valid
clause=data/json/feat/tune/Structures/test_theory/valid/valid/repr/anonym/$param/good/12/alltac_rule.pl
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')

bk=prolog/anonym_repr_bk.pl

for theory in ${theories[@]}; do
    (
        python filter.py --clause $clause \
            --pred $knn_pred/$theory.eval \
            --test $test/$theory \
            --label data/json/feat/merge/$theory.label \
            --bk $bk \
            --info $valid/$kind$descript/$anonym/$param
    )&
done
