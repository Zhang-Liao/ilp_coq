for i in {0..0}; do
    (python predc_by_cluster.py --cluster data/json/neg/rand_train_test/train$i\_pos.json \
        --neg data/json/neg/rand_train_test/train$i\_neg.json \
        --dat data/json/predicate/rand_train_test/train$i.json \
        --out data/json/predicate/rand_train_test/train/rel1_local/train$i \
        --bias /home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/rel1_bias.pl \
        # --var
        )&

    # (python predc.py \
    #     --neg data/json/neg/rand_train_test/train$i\_neg.json \
    #     --dat data/json/predicate/rand_train_test/train$i.json \
    #     --out data/json/predicate/rand_train_test/train/no_clst/rel1/train$i \
    #     --bias /home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/rel1_bias.pl \
    #     )&        
done
