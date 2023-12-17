knn_pred=data/json/ortho/feat/tune/QArith/test_theory
bk=prolog/prop_bk.pl
negs=(1 2 4 8 16)
poss=(2 4 8 16 32)

anonym=origin
kind=prop
test=data/json/ortho/predicate/$anonym/merge/test/
theories=('theories/ListsLogic')
for theory in "${theories[@]}"; do
    for neg in "${negs[@]}"; do

        for pos in "${poss[@]}"; do
            (

                dir=data/json/ortho/predicate/$anonym/tune/QArith/train/$kind/p$pos\n$neg
                python filter.py --clause $dir/alltac_rule.pl \
                    --pred $knn_pred/$theory.eval \
                    --test $test/$theory \
                    --label data/json/ortho/feat/merge/$theory.label \
                    --bk $bk \
                    --info $kind/$anonym/p$pos\n$neg
            ) &

        done

    done
done
