dir=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/theories/MSets

echo "number of proof states"
grep -r -v "^#lemma" $dir | wc -l

echo intros
grep -r "\"intros\"" $dir | wc -l

echo simpl
grep -r "\"simpl\"" $dir | wc -l

echo auto
grep -r "\"auto\"" $dir | wc -l

echo reflexivity
grep -r "\"reflexivity\"" $dir | wc -l

echo assumption
grep -r "\"assumption\"" $dir | wc -l

echo trivial
grep -r "\"trivial\"" $dir | wc -l
