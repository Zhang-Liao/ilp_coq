#!/bin/bash
dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test
for i in {0..19}
do
    python preproc/preproc.py --file $dir/train$i.json&
    python preproc/preproc.py --file $dir/test$i.json&
done