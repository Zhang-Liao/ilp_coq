theory=QArith
neg_dir=data/json/ortho/feat/merge/theories/$theory
dat_file=data/json/ortho/predicate/origin/merge/theories/$theory.json
out_dir=data/json/ortho/predicate/origin/tune/$theory
kind=rel
neg_ratios=(1 2 4 8 16)
# clusters=(2 4 8 16)
clusters=(32)

for neg_ratio in "${neg_ratios[@]}"; do
    (
        for cluster in "${clusters[@]}"; do
            python predc_by_cluster.py \
                --cluster $neg_dir/$theory\_pos$cluster.json \
                --neg $neg_dir/$theory\_neg.json \
                --dat $dat_file \
                --out $out_dir/train/$kind/p$cluster\n$neg_ratio \
                --bias prolog/rel_noid_bias.pl \
                --kind origin \
                --neg_ratio $neg_ratio
        done
    ) &
done
