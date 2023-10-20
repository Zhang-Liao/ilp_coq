#!/bin/bash
dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets
for i in {0..9}; do
    (
        python preproc/preproc.py --file $dir/train$i.json
        python preproc/preproc.py --file $dir/test$i.json
    )
done
