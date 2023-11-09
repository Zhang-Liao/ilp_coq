for i in {1..5}; do
    (python predc_by_cluster.py --cluster data/json/neg/rand_train_test/train$i\_pos20.json \
        --neg data/json/neg/rand_train_test/train$i\_neg.json \
        --dat data/json/predicate/anonym/rand_train_test/train$i.json \
        --out data/json/predicate/anonym/rand_train_test/train/prop/p20n20/train$i \
        --bias /home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/prop_bias.pl \
        --kind anonym
        )&      
done
