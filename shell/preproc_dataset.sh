dataset=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/merge

find $dataset/plugins $dataset/theories -name "*.json" | xargs -i python preproc/preproc.py --file {}
