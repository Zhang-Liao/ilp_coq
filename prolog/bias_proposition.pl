hyp_coq_var(-1, "", "", []).
goal_coq_var(-1, "", []).

hyp_typ(hyp_ass).
hyp_typ(hyp_dc).
hyp_typ(hyp_dt).

nat_idx([]).
nat_idx([H | Tl]) :- integer(H), nat_idx(Tl).

goal_idx(Idx) :- nat_idx(Idx).

hyp_idx([_, Typ| Idx]) :- hyp_typ(Typ), nat_idx(Idx).

:- modeb(3, hyp_coq_var(+nat, -string, +string, -hyp_idx)).
:- modeb(3, goal_coq_var(+nat, +string, -goal_idx)).

:- set(construct_bottom, false).
:- set(refine, auto).
:- set(search, heuristic).
:- set(openlist, 50).
:- set(verbosity, 0).
:- set(clauselength, 32).

:- set(evalfn, user).
:- set(nodes, 8000).

only_head(tac(_N, _T)).

cost(Clause, [P, N, _L], Cost) :-
  ((only_head(Clause); P is 0) -> Cost is inf; Cost is N - P), !.