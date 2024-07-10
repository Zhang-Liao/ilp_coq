max_cluster=(1 2 4 8 16 32)

theorey=Structures
dir=data/json/feat/merge/theories/$theorey

for max in "${max_cluster[@]}"; do
    (
        python preproc/cluster_pos.py \
            --feat $dir/$theorey.feat \
            --label $dir/$theorey.label \
            --max_cluster $max
    ) &
done