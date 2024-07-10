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
dataset=data/json/feat/
merge_dir=$dataset/merge
theories=('valid/valid' 'plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')

train_theory=theories/Structures
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
    )&
done
