poss=(1 2 4 8 16 32)
negs=(0 1 2 4 8 16 32 64)

train_theory=Structures
anonym=anonym
kind=prop
for neg in "${negs[@]}"; do
  (
    for pos in "${poss[@]}"; do
      file=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/predicate/$anonym/tune/$train_theory/train/$kind/p$pos\n$neg/alltac_rule.pl
      tune=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/valid/valid/$kind/$anonym/p$pos\n$neg/alltac_rule.pl
      echo pos $pos neg $neg
      diff <(sort $file) <(sort $tune)
    done
  )
done
