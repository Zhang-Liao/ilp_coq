# dataset=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/predicate/origin

theories=('theories/Classes.json' 'plugins/ssr.json' 'theories/Lists.json' 'theories/QArith.json' 'theories/Numbers.json')

gen() {
    kind=anonym
    dataset=data/json/predicate/anonym/merge
    # swipl $0 >/dev/null
    # rel_path=${0#$dataset}
    rel_path=${1%".json"}
    # echo $rel_path
    out_dir=$dataset/test/$kind/$rel_path
    echo $dataset/$1
    python test_eg_predc.py --test $dataset/$1 --out $out_dir --kind $kind
}

export -f gen

for theory in ${theories[@]}; do
    gen $theory &
done
