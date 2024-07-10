# poss=(1 2 4 8 16 32)
# negs=(0 1 2 4 8 16 32 64)
precs=(5 7 8 10 14 15 16 20 21 25 28 32 35)
anonym=origin
kind=repr
theories=('plugins/rtauto' 'theories/FSets' 'theories/Wellfounded' 'plugins/funind' 'plugins/btauto' 'plugins/nsatz' 'theories/MSets')

for theory in "${theories[@]}"; do
    for prec in "${precs[@]}"; do
        rm -r data/json/feat/tune/Structures/test_theory/$theory/valid/$kind/$anonym/p*n*/good/$prec
    done
done