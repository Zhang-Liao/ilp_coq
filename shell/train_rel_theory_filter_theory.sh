anonym=origin
param=p4n1
knn_pred=data/json/ortho/feat/tune/QArith/test_theory
test=data/json/ortho/predicate/$anonym/merge/test/
clause=data/json/ortho/feat/tune/QArith/test_theory/valid/valid/rel/origin/p4n1/good/10/alltac_rule.pl
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')
valid=valid
bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/rel_noid_bk.pl

for theory in ${theories[@]}; do
    (python filter.py --clause $clause \
        --pred $knn_pred/$theory.eval \
        --test $test/$theory \
        --label data/json/ortho/feat/merge/$theory.label \
        --bk $bk \
        --info $valid/rel/$anonym/$param) &
done
