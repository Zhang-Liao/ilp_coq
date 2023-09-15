% only left, above, dif, no coq var
in_case_no_goal_predc_exist(-1,[]).
goal_predc(in_case_no_goal_predc_exist).
in_case_no_hyp_predc_exist(-1,-1,[]).
hyp_predc(in_case_no_hyp_predc_exist).

hyp_typ(hyp_ass).
hyp_typ(hyp_dc).
hyp_typ(hyp_dt).

position_left([X], [Y]) :- !, integer(X), integer(Y), X < Y.
position_left([H|X], [H|Y]) :- position_left(X, Y).

hyp_position_left([Name, Type| Idx1], [Name, Type| Idx2]) :-
    hyp_typ(Type), position_left(Idx1, Idx2).

goal_position_left(Idx1, Idx2) :- position_left(Idx1, Idx2).

position_above(X, Y) :- dif(X,Y), prefix(X, Y).

nat_idx([]).
nat_idx([H | Tl]) :- integer(H), nat_idx(Tl).

goal_idx(Idx) :- nat_idx(Idx).

hyp_idx([_, Typ| Idx]) :- hyp_typ(Typ), nat_idx(Idx).


% :- modeh(1, tac(+nat, #string)).
:- modeb(3, dif(+string, +string)).
:- modeb(3, dif(+hyp_idx, +hyp_idx)).
:- modeb(3, dif(+goal_idx, +goal_idx)).
:- modeb(3, goal_position_left(+goal_idx, +goal_idx)).
:- modeb(3, hyp_position_left(+hyp_idx, +hyp_idx)).
:- modeb(3, position_above(+goal_idx, +goal_idx)).
:- modeb(3, position_above(+hyp_idx, +hyp_idx)).

:- determination(tac/2, goal_position_left/2).
:- determination(tac/2, hyp_position_left/2).
:- determination(tac/2, position_above/2).
:- determination(tac/2, dif/2).

:- set(construct_bottom, false).
:- set(refine, auto).
:- set(search, heuristic).
:- set(openlist, 50).
:- set(verbosity, 0).
:- set(clauselength, 32).

% :- set(nodes, 8000).

% :- set(noise, 0).
