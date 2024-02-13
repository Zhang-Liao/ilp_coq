theories=('theories/PArith' 'theories/Relations' 'theories/Bool' 'theories/Logic' 'theories/Lists')
origin=data/json/ortho/predicate/origin/merge
dest=$origin/valid

mkdir $dest
rm $dest/*
for theory in ${theories[@]}; do
        cat $origin/$theory.label >> $dest/valid.label
        cat $origin/$theory.feat >> $dest/valid.feat
        cat $origin/$theory.json >> $dest/valid.json
done