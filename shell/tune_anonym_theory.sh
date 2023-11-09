pred=data/json/origin_feat/tune/QArith/test_theory/theories/Lists.eval
label=data/json/origin_feat/merge/theories/Lists.label
all_predc=/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/anonym_predc.pl
negs=(1 2 4 8 16 32)
poss=(2 4 8 16 32)
anonym=anonym
kind=rel
test=data/json/predicate/$anonym/merge/test/theories/Lists
for neg in "${negs[@]}"; do
    for pos in "${poss[@]}"; do
        (
            dir=data/json/predicate/$anonym/tune/QArith/train/$kind/p$pos\n$neg
            python filter.py --clause $dir/alltac_rule.pl --pred $pred --test $test --label $label --all_predc $all_predc --info $kind/$anonym/p$pos\n$neg
        ) &
    done
done
