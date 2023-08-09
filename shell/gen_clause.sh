dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/split0/predc_auto
# find $dir -name "*.log" | parallel rm {}
# find $dir -name "*.rule.pl" | parallel rm {}
# find $dir -name "*.pl" | parallel -j 4 swipl {} ">" {}.log
python post_proc_claus.py --dir $dir