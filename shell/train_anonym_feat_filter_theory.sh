kind=feat
anonym=anonym
param=p1n32
train_theory=Structures
descript=''
knn_pred=data/json/feat/tune/$train_theory/test_theory
test=data/json/predicate/anonym/merge/test$descript/
clause=data/json/feat/tune/Structures/test_theory/valid/valid/feat/anonym/p1n32/good/18/alltac_rule.pl
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')


valid=valid
bk=prolog/anonym_feat_id_bk.pl

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
