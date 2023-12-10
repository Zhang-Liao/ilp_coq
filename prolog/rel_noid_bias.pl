:- consult('/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/rel_noid_bk.pl').

:- modeb(*, dif(+string, +string)).
:- modeb(*, dif(+hyp_idx, +hyp_idx)).
:- modeb(*, dif(+goal_idx, +goal_idx)).
:- modeb(*, goal_position_left(+goal_idx, +goal_idx)).
:- modeb(*, hyp_position_left(+hyp_idx, +hyp_idx)).
:- modeb(*, goal_above(+nat, +goal_idx, +goal_idx)).
:- modeb(*, hyp_above(+nat, +hyp_idx, +hyp_idx)).
:- modeb(*, is_goal_root(+nat, +goal_idx)).
:- modeb(*, is_hyp_root(+nat, +hyp_idx)).
:- modeb(*, eq_goal_term(+nat, +goal_idx, +goal_idx)).
:- modeb(*, eq_goal_hyp_term(+nat, +goal_idx, +hyp_idx)).
:- modeb(*, similar_goal_terms(+nat, +goal_idx, +goal_idx)).
% :- modeb(*, similar_goal_hyp_terms(+nat, +goal_idx, +hyp_idx)).

:- determination(tac/2, dif/2).
:- determination(tac/2, goal_position_left/2).
:- determination(tac/2, hyp_position_left/2).
:- determination(tac/2, goal_above/3).
:- determination(tac/2, hyp_above/3).
:- determination(tac/2, is_goal_root/2).
:- determination(tac/2, is_hyp_root/2).
:- determination(tac/2, eq_goal_term/3).
:- determination(tac/2, eq_goal_hyp_term/3).
:- determination(tac/2, similar_goal_terms/3).
% :- determination(tac/2, similar_goal_hyp_terms/3).

:- set(construct_bottom, false).
:- set(refine, auto).
:- set(search, heuristic).
:- set(verbosity, 0).
:- set(clauselength, 1000).
:- set(depth, 1000).

:- set(nodes, 30000).
