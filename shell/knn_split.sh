dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/tune/MSets
for i in {0..9}; do
    (
        # train_x=$dir/train$i.feat
        # train_y=$dir/train$i.label
        # test_x=$dir/test$i.feat
        # knn/_build/default/bin/main.exe -train_x $train_x -train_y $train_y -test_x $test_x
        python stats/acc.py --pred $dir/test$i.eval --label $dir/test$i.label
    ) &

done
