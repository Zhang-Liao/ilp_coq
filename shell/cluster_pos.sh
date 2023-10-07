dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/MSets/tune
max_cluster=(1 2 4 8 16 32)

for i in {0..9}; do
    for max in "${max_cluster[@]}"; do
        (
            python preproc/cluster_pos.py \
                --feat $dir/train$i.feat \
                --label $dir/train$i.label \
                --max_cluster $max
        ) &
    done
done

# python cluster_pos.py --feat $dir/split0.feat --label $dir/split0.label
