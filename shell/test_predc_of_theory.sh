
theories=('theories/Sorting' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'valid/valid')
# theories=('valid/valid')
# theories=('theories/PArith' 'theories/Numbers' 'plugins/btauto' 'theories/Arith' 'theories/Strings')
gen() {
    kind=origin
    dataset=data/json/ortho/predicate/$kind/merge
    out_dir=$dataset/test/$1
    python test_eg_predc.py --test $dataset/$1.json --out $out_dir --kind $kind
}

export -f gen

for theory in ${theories[@]}; do
    (gen $theory)&
done
