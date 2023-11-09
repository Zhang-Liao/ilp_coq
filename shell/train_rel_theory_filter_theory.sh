predc_kind=rel
anonym=origin
param=p32n16
knn_pred=data/json/origin_feat/tune/QArith/test_theory
test_predc=data/json/predicate/$anonym/merge/test/
clause=data/json/predicate/$anonym/tune/QArith/train/$predc_kind/$param/alltac_rule.pl
theories=('theories/Numbers')
# theories=('plugins/ssr')

all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_predc.pl

for theory in ${theories[@]}; do
    (python filter.py --clause $clause \
        --pred $knn_pred/$theory.eval \
        --test $test_predc/$theory \
        --label data/json/origin_feat/merge/$theory.label \
        --all_predc $all_predc \
        --info $predc_kind/$anonym/$param)
done
