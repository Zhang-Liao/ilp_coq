dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/1000
find $dir -name "*.log" | parallel rm {}
find $dir -name "*.rule.pl" | parallel rm {}
find $dir -name "*.pl" | parallel -j 4 swipl {} ">" {}.log