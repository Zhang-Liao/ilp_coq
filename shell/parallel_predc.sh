for i in {0..1}; do
    (python predc_by_cluster.py --cluster data/json/neg/rand_train_test/train$i\_pos.json \
        --neg data/json/neg/rand_train_test/train$i\_neg.json \
        --dat data/json/predicate/rand_train_test/train$i.json \
        --out data/json/predicate/rand_train_test/predc/neg10rel/train$i)&
done
