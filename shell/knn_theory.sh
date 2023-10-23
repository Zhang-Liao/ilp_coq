eval() {

    train_x=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets/train$2.feat
    train_y=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets/train$2.label
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

dataset=data/json/origin_feat/merge
theories=('theories/Classes.json' 'plugins/ssr.json' 'theories/Lists.json' 'theories/QArith.json' 'theories/Numbers.json')

for theory in ${theories[@]}; do
    IFS=/ read -ra splits <<<$theory
    kind=${splits[0]}
    # Only test theories parallelly to avoid k-NNs of different train.feat files output to the same .eval file.
    (
        for i in {0..9}; do
            train_dir=data/json/origin_feat/tune/MSets
            train_i=$train_dir/train$i
            train_x=$train.feat
            train_y=$train.label
            out=$train_dir/test_theory/train$i/$kind
            mkdir -p $out
            eval $dataset/$theory $i $out
        done
    ) &

done

# bash -c "pred" 1 2
