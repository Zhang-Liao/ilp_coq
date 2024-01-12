max_cluster=(2 4 8 16 32)

dir=data/json/ortho/feat/merge/theories/QArith

for max in "${max_cluster[@]}"; do
    (
        python preproc/cluster_pos.py \
            --feat $dir/QArith.feat \
            --label $dir/QArith.label \
            --max_cluster $max
    ) &
done