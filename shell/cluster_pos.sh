dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/rand_train_test

for i in {0..19}
do
    (python cluster_pos.py --feat $dir/train$i.feat --label $dir/train$i.label)&
done