:- multifile goal_node/4.
:- multifile hyp_node/5.

goal_node(dummy, -1, [], dummy).
hyp_node(dummy, -1, [], [], dummy).
:- consult('/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/common_bk.pl').
