# ILP for Coq

- To reproduce the graphs and table in Section 5, run `bash shell/results.sh`. The results and graphs are presented in the home directory of the project.
- To learn rules, run
  - `bash shell/gen_anonym_feat_clause.sh`
  - `bash shell/gen_anonym_repr_clause.sh`
  - `bash shell/gen_origin_feat_clause.sh`
  - `bash shell/gen_origin_repr_clause.sh`
- To evaluate in the validation dataset, run
  - `bash shell/tune_anonym_feat_theory.sh`
  - `bash shell/tune_anonym_repr_theory.sh`
  - `bash shell/tune_origin_feat_theory.sh`
  - `bash shell/tune_origin_repr_theory.sh`
- To test the learned rules in the test dataset, run
  - `bash shell/train_anonym_feat_filter_theory.sh`
  - `bash shell/train_anonym_repr_filter_theory.sh`
  - `bash shell/train_origin_feat_filter_theory.sh`
  - `bash shell/train_origin_repr_filter_theory.sh`
