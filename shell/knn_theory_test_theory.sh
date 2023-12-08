eval() {

    train_x=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/$2/$2.feat
    train_y=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/$2/$2.label
    file=${1%".json"}
    test_x=$file.feat
    test_y=$file.label
    pred_y=$file.eval

    IFS=/ read -ra splits <<<$pred_y
    only_pred_name=${splits[-1]}
    knn/_build/default/bin/main.exe -train_x $train_x -train_y $train_y -test_x $test_x
    cp $pred_y $3
    python stats/acc.py --pred $3/$only_pred_name --label $test_y
}

export -f eval

dataset=data/json/ortho/feat/merge
theories=('theories/Lists.json' 'theories/Init.json' 'plugins/setoid_ring.json' 'theories/Vectors.json' 'theories/NArith' 'theories/Sorting')

train_theory=QArith
for theory in ${theories[@]}; do
    IFS=/ read -ra splits <<<$theory
    kind=${splits[0]}
    (
        train_dir=data/json/ortho/feat/tune/$train_theory
        train_x=$train.feat
        train_y=$train.label
        out=$train_dir/test_theory/$kind
        mkdir -p $out
        eval $dataset/$theory $train_theory $out
    ) &

done
