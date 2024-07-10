train_theory=Structures
knn_pred=data/json/feat/tune/$train_theory/test_theory

negs=(0 1 2 4 8 16 32 64)
poss=(1 2 4 8 16 32)

descript=''
bk=prolog/anonym_feat_id_bk.pl
test=data/json/predicate/anonym/merge/test/
theories=('valid/valid')
for theory in "${theories[@]}"; do
    for neg in "${negs[@]}"; do
        for pos in "${poss[@]}"; do
            (
                dir=data/json/predicate/anonym/tune/$train_theory/train/feat$descript/p$pos\n$neg
                python filter.py --clause $dir/alltac_rule.pl \
                    --pred $knn_pred/$theory.eval \
                    --test $test/$theory \
                    --label data/json/feat/merge/$theory.label \
                    --bk $bk \
                    --info feat$descript/anonym/p$pos\n$neg
            ) &
        done
    done
done
