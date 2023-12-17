
theories=('theories/Sorting' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'theories/NArith')

# theories=('theories/ListsLogic.json')

gen() {
    kind=prop
    dataset=data/json/ortho/predicate/origin/merge
    out_dir=$dataset/test/$1
    python test_eg_predc.py --test $dataset/$1.json --out $out_dir --kind $kind
}

export -f gen

for theory in ${theories[@]}; do
    gen $theory &
done
