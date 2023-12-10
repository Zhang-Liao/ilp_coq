knn_pred=data/json/ortho/feat/tune/QArith/test_theory
negs=(1 2 4 8 16 32)
poss=(2 4 8 16 32)

anonym=anonym
descript=''
train_descrip=$descript
bk=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_rel_id_bk.pl
kind=rel
test=data/json/ortho/predicate/$anonym/merge/test$descript/
theories=('theories/Lists')
for theory in "${theories[@]}"; do
    for neg in "${negs[@]}"; do
        for pos in "${poss[@]}"; do
            (
                dir=data/json/ortho/predicate/$anonym/tune/QArith/train/$kind$train_descrip/p$pos\n$neg
                python filter.py --clause $dir/alltac_rule.pl \
                    --pred $knn_pred/$theory.eval \
                    --test $test/$theory \
                    --label data/json/ortho/feat/merge/$theory.label \
                    --bk $bk \
                    --info $kind/$anonym$descript/p$pos\n$neg
            ) &
        done
    done
done
