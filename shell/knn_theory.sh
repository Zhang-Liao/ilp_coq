pred() {

    train_x=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets/train$2.feat
    train_y=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets/train$2.label
    file=${1%".json"}
    test_x=$file.feat
    pred_y=$file.eval
    knn/_build/default/bin/main.exe -train_x $train_x -train_y $train_y -test_x $test_x
    cp $pred_y $3
}

export -f pred

dataset=data/json/origin_feat/merge
theory=theories/Arith.json
IFS=/ read -ra ADDR <<<$theory
kind=${ADDR[0]}

for i in {0..0}; do
    train_dir=data/json/origin_feat/tune/MSets
    train_i=$train_dir/train$i
    train_x=$train.feat
    train_y=$train.label
    out=$train_dir/test/train$i/$kind
    mkdir -p $out
    # find $theory/$subdir -name "*.json" | parallel pred {} $i
    pred $dataset/$theory $i $out
    # echo $theory/$subdir
    # python move_knn_eval.py --source $theory/$subdir --dest $out
done

# bash -c "pred" 1 2
