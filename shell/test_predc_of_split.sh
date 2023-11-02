# dataset=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/origin

for i in {1..9}; do
    (
        kind=anonym
        dataset=data/json/predicate/anonym/rand_lines
        # swipl $0 >/dev/null
        # rel_path=${0#$dataset}
        # echo $rel_path
        out_dir=$dataset/test/valid$i
        # echo $dataset/$1
        python test_eg_predc.py --test $dataset/valid$i.json --out $out_dir --kind $kind
    ) &
done
