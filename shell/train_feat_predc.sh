theory=Structures
neg_dir=data/json/feat/merge/theories/$theory
dat_file=data/json/predicate/origin/merge/theories/$theory.json
out_dir=data/json/predicate/origin/tune/$theory
kind=feat

negs=(0 1 2 4 8 16 32 64)
poss=(1 2 4 8 16 32)

for neg in "${negs[@]}"; do
    (
        for pos in "${poss[@]}"; do
            python predc_by_cluster.py \
                --cluster $neg_dir/$theory\_pos$pos.json \
                --neg $neg_dir/$theory\_neg.json \
                --dat $dat_file \
                --out $out_dir/train/$kind/p$pos\n$neg \
                --bias prolog/feat_noid_bias.pl \
                --kind origin \
                --neg_ratio $neg
        done
    ) &
done
