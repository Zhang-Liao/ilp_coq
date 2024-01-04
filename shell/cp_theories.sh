theories=('theories/Logic' 'theories/ZArith' 'theories/Classes' 'theories/FSets' 'plugins/rtauto')
origin=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/predicate/origin/merge
dest=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/predicate/origin/merge/rand_valid

mkdir $dest
rm $dest/*
for theory in ${theories[@]}; do
        # cat $origin/$theory.label >> $dest/valid.label
        # cat $origin/$theory.feat >> $dest/valid.feat
        cat $origin/$theory.json >> $dest/valid.json
done