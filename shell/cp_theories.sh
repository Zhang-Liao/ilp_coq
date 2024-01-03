theories=('theories/Logic' 'theories/ZArith' 'theories/Classes' 'theories/FSets' 'plugins/rtauto')
origin=data/json/ortho/feat/merge
dest=data/json/ortho/feat/tune/QArith/test_theory/rand_valid
rm $dest/*
for theory in ${theories[@]}; do
        # cp $origin/$theory.* $dest/
        cat $origin/$theory.label >> $dest/valid.label
        cat $origin/$theory.feat >> $dest/valid.feat
        cat $origin/$theory.json >> $dest/valid.json
done