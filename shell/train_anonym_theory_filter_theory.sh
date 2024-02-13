kind=rel
anonym=anonym
param=p1n32
train_theory=Structures
descript=''
knn_pred=data/json/ortho/feat/tune/$train_theory/test_theory
test=data/json/ortho/predicate/anonym/merge/test$descript/
clause=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/valid/valid/rel/anonym/p1n32/good/15/alltac_rule.pl
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')
valid=valid
bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_rel_id_bk.pl

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
