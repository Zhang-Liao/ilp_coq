:- multifile goal_node/3.
:- multifile hyp_node/4.

goal_node(dummy, -1, []).
hyp_node(dummy, -1, dummy, []).
:- consult('/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/common_bk.pl').
