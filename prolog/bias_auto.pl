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

node(N, Idx, P, RelativeIdx) :-
    goal_predc(P),
    Fact =.. [P, N, NodeIdx], Fact,
    prefix(Idx, NodeIdx),
    append(Idx, RelativeIdx, NodeIdx).

node(N, Idx, Predc, RelativeIdx) :-
    hyp_predc(Predc),
    Fact =.. [Predc, N, _Name, NodeIdx], Fact,
    prefix(Idx, NodeIdx),
    append(Idx, RelativeIdx, NodeIdx).

eq_subterm(N, Idx1, Idx2) :-
    dif(Idx1, Idx2),
    forall(
        node(N, Idx1, Predc, RelativeIdx1),
        node(N, Idx2, Predc, RelativeIdx1)),
    forall(
        node(N, Idx2, Predc, RelativeIdx2),
        node(N, Idx1, Predc, RelativeIdx2)).

% :- modeh(1, tac(+nat, #string)).
:- modeb(3, dif(+string, +string)).
:- modeb(3, dif(+hyp_idx, +hyp_idx)).
:- modeb(3, dif(+goal_idx, +goal_idx)).
:- modeb(3, goal_position_left(+goal_idx, +goal_idx)).
:- modeb(3, hyp_position_left(+hyp_idx, +hyp_idx)).
:- modeb(3, position_above(+goal_idx, +goal_idx)).
:- modeb(3, position_above(+hyp_idx, +hyp_idx)).
:- modeb(3, hyp_coq_var(+nat, -string, +string, -hyp_idx)).
:- modeb(3, goal_coq_var(+nat, +string, -goal_idx)).
:- modeb(3, eq_subterm(+nat, +goal_idx, +goal_idx)).
:- modeb(3, eq_subterm(+nat, +hyp_idx, +hyp_idx)).
:- modeb(3, eq_subterm(+nat, +goal_idx, +hyp_idx)).

:- determination(tac/2, goal_position_left/2).
:- determination(tac/2, hyp_position_left/2).
:- determination(tac/2, position_above/2).
:- determination(tac/2, hyp_coq_var/4).
:- determination(tac/2, goal_coq_var/3).
:- determination(tac/2, dif/2).
:- determination(tac/2, eq_subterm/3).

:- set(construct_bottom, false).
:- set(refine, auto).
:- set(search, heuristic).
:- set(openlist, 50).
:- set(verbosity, 0).
:- set(clauselength, 32).

:- set(evalfn, user).
:- set(nodes, 8000).

only_head(tac(A, B)).

cost(Clause, [P, N, _L], Cost) :-
  ((only_head(Clause); P is 0) -> Cost is inf; Cost is N - P), !.