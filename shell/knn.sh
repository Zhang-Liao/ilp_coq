train_x=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/split0.feat
train_y=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/split0.label
# test_x=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/100.feat
test_x=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ten_split/split8.feat

/home/zhangliao/ilp_out_coq/ilp_out_coq/ocaml/_build/default/bin/main.exe \
-train_x $train_x -train_y $train_y -test_x $test_x