predc_kind=rel
anonym=origin
param=p4n4
knn_pred=data/json/origin_feat/tune/MSets/test_theory
test_predc=data/json/predicate/origin/merge/test/prop
train_predc=data/json/predicate/$anonym/tune/MSets/train/$predc_kind/$param
# theories=('theories/Classes' 'plugins/ssr' 'theories/Lists' 'theories/QArith' 'theories/Numbers')
theories=('plugins/ssr')

all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/all_predc.pl

for theory in ${theories[@]}; do
    for i in {0..9}; do
        (python filter.py --clause $train_predc/train$i/alltac_rule.pl \
            --pred $knn_pred/train$i/$theory.eval \
            --test $test_predc/$theory \
            --label data/json/origin_feat/merge/$theory.label \
            --all_predc $all_predc \
            --info $predc_kind/$anonym/$param) &
    done
done
