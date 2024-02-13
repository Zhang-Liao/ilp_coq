kind=prop
anonym=anonym
param=p1n1
descript=''
train_theory=Structures
knn_pred=data/json/ortho/feat/tune/$train_theory/test_theory
test=data/json/ortho/predicate/$anonym/merge/test$descript/
valid=valid
clause=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/valid/valid/prop/anonym/p1n1/good/10/alltac_rule.pl
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')
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
