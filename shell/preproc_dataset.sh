# dataset=/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/ortho/feat/merge

# find $dataset/plugins $dataset/theories -name "*.json" | xargs -i python preproc/preproc.py --file {}
python preproc/preproc.py --file data/json/no_ortho/origin_feat/theories/Init/Logic.json
