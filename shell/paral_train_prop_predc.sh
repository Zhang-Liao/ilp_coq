neg_dir=data/json/neg/rand_3000
dat_dir=data/json/predicate/origin/rand_3000
neg_ratios=(1 2 4 8 16 32)
clusters=(2 4 8 16 32)

for i in {0..9}; do
    for neg_ratio in "${neg_ratios[@]}"; do
        (
            for cluster in "${clusters[@]}"; do
                python predc_by_cluster.py \
                    --cluster $neg_dir/train$i\_pos$cluster.json \
                    --neg $neg_dir/train$i\_neg.json \
                    --dat $dat_dir/train$i.json \
                    --out $dat_dir/train/prop/p$cluster\n$neg_ratio/train$i \
                    --bias prolog/prop_bias.pl \
                    --kind prop \
                    --neg_ratio $neg_ratio
                # --only_common
            done
        ) &
    done
done
