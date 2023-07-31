name_equal(X, Y) :- X = Y.
position_left([X], [Y]) :- !, integer(X), integer(Y), X < Y.
position_left([H|X], [H|Y]) :- position_left(X, Y).
position_above(X, Y) :- dif(X,Y), prefix(X, Y).

nat_idx([]).
nat_idx([H | Tl]) :- integer(H), nat_idx(Tl).
goal_idx(Idx) :- nat_idx(Idx).

hyp_typ(hyp_ass).
hyp_typ(hyp_dc).
hyp_typ(hyp_dt).
hyp_idx([_, Typ| Idx]) :- hyp_typ(Typ), nat_idx(Idx).

:- modeb(3, name_equal(+string, +string)).
:- modeb(3, dif(+string, +string)).
:- modeb(3, dif(+hyp_idx, +hyp_idx)).
:- modeb(3, dif(+goal_idx, +goal_idx)).
:- modeb(3, position_left(+goal_idx, +goal_idx)).
:- modeb(3, position_left(+hyp_idx, +hyp_idx)).
:- modeb(3, position_above(+goal_idx, +goal_idx)).
:- modeb(3, position_above(+hyp_idx, +hyp_idx)).

:- determination(tac/1, position_left/2).
:- determination(tac/1, position_above/2).

:- set(construct_bottom, false).
:- set(refine, auto).
:- set(search, heuristic).
:- set(openlist, 5).
:- set(verbosity, 0).
:- set(clauselength, 8).

% :- set(evalfn, user).
% :- set(noise, 100).
% :- set(explore, true).
% prune(tac(X)) :- nonvar(X).
% prune((tac(X) :- _)) :- nonvar(X).