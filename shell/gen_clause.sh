dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc
find /home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc  -name "*.rule.pl" | xargs -i rm {}
find /home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc  -name "*.pl" | xargs -i swipl {}