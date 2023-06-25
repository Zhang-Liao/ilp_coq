#!/bin/bash
dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split
for i in {0..9}
do
    python preproc/preproc.py --file $dir/split$i.json&
done