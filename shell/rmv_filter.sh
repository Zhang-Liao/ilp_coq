dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/2percent_split
for i in {0..9}; do
    curr_dir=$dir/test$i
    # mv $curr_dir/filter/* $curr_dir/
    rm -r $curr_dir/filter    
done
