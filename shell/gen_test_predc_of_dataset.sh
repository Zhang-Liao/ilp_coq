dataset=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/origin

gen() {
    dataset=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/origin
    # swipl $0 >/dev/null
    rel_path=${0#$dataset}
    rel_path=${rel_path%".json"}
    echo $rel_path
    out_dir=$dataset/testall/prop/$rel_path
    python test_eg_predc.py --test $0 --out $out_dir --kind prop
}

export -f gen

# file=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/origin/theories/Arith

find $dataset/theories -name "*.json" | xargs -i bash -c gen {}

# find $dataset/plugins $dataset/theories -name "*.json" | xargs -i bash -c gen {}
