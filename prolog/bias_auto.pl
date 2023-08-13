name_equal(X, Y) :- X = Y.

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

:- modeb(3, name_equal(+string, +string)).
:- modeb(3, dif(+string, +string)).
:- modeb(3, dif(+hyp_idx, +hyp_idx)).
:- modeb(3, dif(+goal_idx, +goal_idx)).
:- modeb(3, goal_position_left(+goal_idx, +goal_idx)).
:- modeb(3, hyp_position_left(+hyp_idx, +hyp_idx)).
:- modeb(3, position_above(+goal_idx, +goal_idx)).
:- modeb(3, position_above(+hyp_idx, +hyp_idx)).
:- modeb(3, hyp_coq_var(+nat, -string, +string, -hyp_idx)).
:- modeb(3, goal_coq_var(+nat, +string, -goal_idx)).

:- determination(tac/1, goal_position_left/2).
:- determination(tac/1, hyp_position_left/2).
:- determination(tac/1, position_above/2).
:- determination(tac/1, hyp_coq_var/4).
:- determination(tac/1, goal_coq_var/3).

:- set(construct_bottom, false).
:- set(refine, auto).
:- set(search, heuristic).
:- set(openlist, 5).
:- set(verbosity, 0).
:- set(clauselength, 8).

:- set(evalfn, user).
% :- set(noise, 100).
% :- set(explore, true).
% prune(tac(X)) :- nonvar(X).
% prune((tac(X) :- _)) :- nonvar(X).

only_head(_C :- true).

cost(Clause, [P, N, _L], Cost) :-
  ((only_head(Clause); P is 0) -> Cost is inf; Cost is N - P), !.