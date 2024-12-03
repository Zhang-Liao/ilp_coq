# ILP for Coq

Paper https://arxiv.org/abs/2411.01188

## Requiremnets

- SWI-Prolog 8.4.2
- pyswip 0.2.11 
- Python 3.11.4

## Data

Download the [dataset](https://drive.google.com/file/d/1vT1ZYX7kpgisasTO3RtEepvU-RevNudB/view?usp=drive_link). Please decompose the dataset in the home directory of the project.

## Explaination
- First, execute `cd ilp_coq`.
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
