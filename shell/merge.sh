#!/bin/bash
dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split
for i in {0..0}
do
    end_id=$((`expr $i + 7`%10))
    # echo "i: "$i" end id: "$end_id
    if [ $end_id -gt $i ]
    then
        cat $dir/split[$i-$end_id].feat > $dir/split$i\_$end_id.feat
        cat $dir/split[$i-$end_id].label > $dir/split$i\_$end_id.label
    else
        cat $dir/split[$i-9].feat $dir/split[0-$end_id].feat > $dir/split$i\_$end_id.feat
        cat $dir/split[$i-9].label $dir/split[0-$end_id].label > $dir/split$i\_$end_id.label
    fi
done
