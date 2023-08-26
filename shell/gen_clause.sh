dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/ten_split/predc_auto
# find $dir -name "*.log" | parallel rm {}
find $dir -name "*_rule.pl" | parallel rm {}
find $dir -name "*.pl" | parallel -j 4 swipl {}
# python post_proc_claus.py --dir $dir
find $dir -name "*_rule.pl" | xargs -i cat {} > tmp
mv tmp alltac_rule.pl
