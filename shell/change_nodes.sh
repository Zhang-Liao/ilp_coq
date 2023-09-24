dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/rand_train_test/train/prop_local/train0
from=$dir/noise0
nodes=30000
out=$dir/noswa$nodes
mkdir $out
(find $from | xargs -i cp {} $out
find $out -name "*.b" | xargs -i python change_nodes.py --nodes $nodes --file {})&