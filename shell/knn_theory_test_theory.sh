eval() {

    train_x=$3.feat
    train_y=$3.label
    test_x=$1.feat
    test_y=$1.label
    pred_y=$1.eval

    IFS=/ read -ra splits <<<$pred_y
    only_pred_name=${splits[-1]}
    knn/_build/default/bin/main.exe -train_x $train_x -train_y $train_y -test_x $test_x
    cp $pred_y $2
    python stats/acc.py --pred $2/$only_pred_name --label $test_y
}

export -f eval

dataset=data/rev_ortho/feat/
merge_dir=$dataset/merge
# theories=('theories/Lists' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'theories/NArith' 'theories/Sorting')
# theories=('theories/PArith' 'theories/Numbers' 'plugins/btauto' 'theories/Arith' 'theories/Strings')
theories=('valid/valid' 'theories/Lists' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'theories/NArith' 'theories/Sorting')

train_theory=theories/QArith
IFS=/ read -ra train_theory_splits <<<$train_theory
train_name=${train_theory_splits[1]}
for theory in ${theories[@]}; do
    IFS=/ read -ra splits <<<$theory
    kind=${splits[0]}
    (
        train_dir=$dataset/tune/$train_name
        out=$train_dir/test_theory/$kind
        mkdir -p $out
        eval $merge_dir/$theory $out $merge_dir/$train_theory
    ) &
done
