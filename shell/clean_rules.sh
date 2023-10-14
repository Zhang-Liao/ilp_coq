dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/anonym/tune/MSets/train/rel/

find $dir -name alltac_rule.pl | xargs -i python clean_rule.py --file {}
# for neg in "${negs[@]}"; do
#     for pos in "${poss[@]}"; do
#         (for i in {0..9}; do
#             dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/anonym/tune/MSets/train/rel/p$pos\n$neg/train$i
#             python clean_rule.py --file $
#         done) &
#     done
# done
