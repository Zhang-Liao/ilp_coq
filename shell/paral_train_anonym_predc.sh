neg_dir=data/json/neg/MSets/tune
dat_dir=data/json/predicate/anonym/tune/MSets
neg_ratios=(1 2 4 8 16 32)
clusters=(1 2 4 8 16 32)
for i in {0..9}; do
    for neg_ratio in "${neg_ratios[@]}"; do
        for cluster in "${clusters[@]}"; do
            # echo $i $neg_ratio $cluster
            (
                python predc_by_cluster.py \
                    --cluster $neg_dir/train$i\_pos$cluster.json \
                    --neg $neg_dir/train$i\_neg.json \
                    --dat $dat_dir/train$i.json \
                    --out $dat_dir/train/rel/p$cluster\n$neg_ratio/train$i \
                    --bias prolog/bias.pl \
                    --kind anonym \
                    --neg_ratio $neg_ratio
            ) &
        done
    done
done
