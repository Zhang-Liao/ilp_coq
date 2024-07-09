poss=(1 2 4 8 16 32)
negs=(0 1 2 4 8 16 32 64)
precs=(5 7 8 10 14 15 16 20 21 25 28 32 35)
anonym=origin
kind=feat
test=data/json/ortho/predicate/$anonym/merge/test/
theories=('valid/valid')

for neg in "${negs[@]}"; do
    for pos in "${poss[@]}"; do
        for prec in "${precs[@]}"; do
            rm -r data/json/feat/tune/Structures/test_theory/valid/valid/$kind/$anonym/p$pos\n$neg/good/$prec
        done
    done
done
