theory=Structures
neg_dir=data/json/ortho/feat/merge/theories/$theory
dat_file=data/json/ortho/predicate/anonym/merge/theories/$theory.json
out_dir=data/json/ortho/predicate/anonym/tune/$theory
kind=repr
# negs=(0 1 2 4 8 16)
# clusters=(1 2 4 8 16 32)

# negs=(32 64)
# poss=(1 2 4 8 16 32)


negs=(128 256)
poss=(1 2 4 8 16 32)


for neg_ratio in "${negs[@]}"; do
    (
        for pos in "${poss[@]}"; do
            python predc_by_cluster.py \
                --cluster $neg_dir/$theory\_pos$pos.json \
                --neg $neg_dir/$theory\_neg.json \
                --dat $dat_file \
                --out $out_dir/train/$kind/p$pos\n$neg_ratio \
                --bias prolog/repr_bias.pl \
                --kind anonym \
                --neg_ratio $neg_ratio
        done
    ) &
done
