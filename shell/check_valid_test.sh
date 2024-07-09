test1=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/theories/MSets/valid/rel/anonym/p1n32/alltac_rule.pl
valid1=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/valid/valid/rel/anonym/p1n32/good/18/alltac_rule.pl
diff <(sort $test1) <(sort $valid1)
echo 'diff <(sort $test1) <(sort $valid1)'


test2=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/theories/MSets/valid/rel/origin/p1n1/alltac_rule.pl
valid2=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/valid/valid/rel/origin/p1n1/good/18/alltac_rule.pl
diff <(sort $test2) <(sort $valid2)
echo 'diff <(sort $test2) <(sort $valid2)'

test3=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/theories/MSets/valid/prop/origin/p1n1/alltac_rule.pl
valid3=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/valid/valid/prop/origin/p1n1/good/12/alltac_rule.pl 
diff <(sort $test3) <(sort $valid3)
echo 'diff <(sort $test3) <(sort $valid3)'

test4=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/theories/MSets/valid/prop/anonym/p1n1/alltac_rule.pl
valid4=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/tune/Structures/test_theory/valid/valid/prop/anonym/p16n1/good/12/alltac_rule.pl 
diff <(sort $test4) <(sort $valid4)
echo 'diff <(sort $test4) <(sort $valid4)'