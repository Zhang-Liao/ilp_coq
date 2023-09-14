dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/train/rel1_local/train0
from=$dir/noise0

for n in {2..4}; do
    out=$dir/noise$n
    mkdir $out
    (find $from | xargs -i cp {} $out
    find $out -name "*.b" | xargs -i python change_noise.py --noise $n --file {})&
done