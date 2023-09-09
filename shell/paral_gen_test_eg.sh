dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/

for i in {0..19}
do
    (python test_eg_predc.py --test $dir/test$i.json --out $dir/test/prop/test$i --prop)&
done