noarity=_noarity
predc_kind=rel
anonym=anonym
param=p16n16
knn_pred=data/json/origin_feat/tune/QArith/test_theory
test_predc=data/json/predicate/$anonym/merge/test$noarity/
clause=data/json/predicate/$anonym/tune/QArith/train/$predc_kind$noarity/$param/alltac_rule.pl
theories=('theories/Sorting' 'theories/Numbers' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors')

all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym$noarity\_predc.pl

for theory in ${theories[@]}; do
    (python filter.py --clause $clause \
        --pred $knn_pred/$theory.eval \
        --test $test_predc/$theory \
        --label data/json/origin_feat/merge/$theory.label \
        --all_predc $all_predc \
        --info $predc_kind/$anonym/$param) &
done
