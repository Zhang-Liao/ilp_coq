dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/rand_train_test

for i in {2..2}
do
    (python preproc/neg.py --feat $dir/train$i.feat --label $dir/train$i.label)&
done