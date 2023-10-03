dat_dir=data/json/predicate/anonym/2percent_split
for i in {1..9}; do
    (python predc_by_cluster.py \
        --cluster data/json/neg/2percent_split/train$i\_pos20.json \
        --neg data/json/neg/2percent_split/train$i\_neg.json \
        --dat $dat_dir/train$i.json \
        --out $dat_dir/train/rel/p32n16/train$i \
        --bias prolog/bias.pl \
        --kind anonym
        )&      
done
