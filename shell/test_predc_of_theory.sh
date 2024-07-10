
# theories=('theories/Sorting' 'theories/NArith' 'theories/Init' 'plugins/setoid_ring' 'theories/Vectors' 'valid/valid')
# theories=('valid/valid')
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')

gen() {
    kind=origin
    dataset=data/json/predicate/$kind/merge
    out_dir=$dataset/test/$1
    python test_eg_predc.py --test $dataset/$1.json --out $out_dir --kind $kind
}

export -f gen

for theory in ${theories[@]}; do
    (gen $theory)&
done
