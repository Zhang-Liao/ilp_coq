for i in {1..1}; do
    (python predc_by_cluster.py --cluster data/json/neg/rand_train_test/train$i\_pos10.json \
        --neg data/json/neg/rand_train_test/train$i\_neg.json \
        --dat data/json/predicate/anonym/rand_train_test/train$i.json \
        --out data/json/predicate/anonym/rand_train_test/train/p10n40/train$i \
        --bias /home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/bias.pl \
        --kind anonym
        )&      
done
