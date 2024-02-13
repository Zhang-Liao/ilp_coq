# max_cluster=(1 2 4 8 16 32)
# max_cluster=(64 128)
max_cluster=(256)

theorey=Structures
dir=data/json/ortho/feat/merge/theories/$theorey

for max in "${max_cluster[@]}"; do
    (
        python preproc/cluster_pos.py \
            --feat $dir/$theorey.feat \
            --label $dir/$theorey.label \
            --max_cluster $max
    ) &
done