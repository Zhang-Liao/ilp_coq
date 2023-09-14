noise=1
from=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/train/rel1_local/train0
out=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/train/rel1_noise1/train0

mkdir $out
find $from | xargs -i cp {} $out
find $out -name "*.b" | xargs -i python change_noise.py --noise $noise --file {}