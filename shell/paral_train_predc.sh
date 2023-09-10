for i in {0..5}; do
    (python predc_by_cluster.py --cluster data/json/neg/rand_train_test/train$i\_pos.json \
        --neg data/json/neg/rand_train_test/train$i\_neg.json \
        --dat data/json/predicate/rand_train_test/train$i.json \
        --out data/json/predicate/rand_train_test/train/rel1/train$i \
        --bias /home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/rel1_bias.pl \
        --prop)&
done
