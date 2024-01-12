theories=('theories/Logic' 'theories/ZArith' 'theories/Classes')
origin=data/json/ortho/feat/merge
dest=$origin/valid

mkdir $dest
rm $dest/*
for theory in ${theories[@]}; do
        cat $origin/$theory.label >> $dest/valid.label
        cat $origin/$theory.feat >> $dest/valid.feat
        cat $origin/$theory.json >> $dest/valid.json
done