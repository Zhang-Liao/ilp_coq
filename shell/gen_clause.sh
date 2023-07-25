dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/1000_predc
find $dir -name *.log | parallel -i rm {}
find $dir -name *.rule.pl | parallel -i rm {}
find $dir  -name "*.pl" | parallel -j 10 swipl {} ">" {}.log