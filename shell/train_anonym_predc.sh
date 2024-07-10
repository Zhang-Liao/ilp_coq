theory=Structures
neg_dir=data/json/feat/merge/theories/$theory
dat_file=data/json/predicate/anonym/merge/theories/$theory.json
out_dir=data/json/predicate/anonym/tune/$theory
# negs=(0 1 2 4 8 16)
# clusters=(1 2 4 8 16 32)
kind=feat

negs=(4)
poss=(4)


for neg_ratio in "${negs[@]}"; do
    (
        for pos in "${poss[@]}"; do
            python predc_by_cluster.py \
                --cluster $neg_dir/$theory\_pos$pos.json \
                --neg $neg_dir/$theory\_neg.json \
                --dat $dat_file \
                --out $out_dir/train/$kind/p$pos\n$neg_ratio \
                --bias prolog/anonym_feat_id_bias.pl \
                --kind anonym \
                --neg_ratio $neg_ratio
        done
    ) &
done
