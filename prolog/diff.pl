% alldif([]).
% alldif([E|Es]) :-
%    maplist(dif(E), Es),
%    alldif(Es).

dif_vars(V, Vs) :- maplist(dif(V), Vs).

goal_predc(p1).
goal_predc(p2).

goal_idxs_aux([], []).

goal_idxs_aux([Hd|Tl], [Idx|Idxs]) :-
    Hd =.. [P, _, Idx],
    goal_predc(P), goal_idxs_aux(Tl, Idxs).

goal_idxs(Atoms, Idxs) :-
    goal_idxs_aux(Atoms, IdxsDup),
    term_variables(IdxsDup, Idxs).

% :- goal_idxs([p1(X, P1), p2(X, P2)], Idxs).

hyp_predc(h1).
hyp_predc(h2).

hyp_idxs_aux([], _, []) :- !.

hyp_idxs_aux([Hd|Tl], Name1, [Idx|Idxs]) :-
    Hd =.. [P, _, Name2, Idx],
    hyp_predc(P),
    Name1 == Name2, !,
    hyp_idxs_aux(Tl, Name1, Idxs).

hyp_idxs_aux([_|Tl], Name, Idxs) :- hyp_idxs_aux(Tl, Name, Idxs).

hyp_idxs(Atoms, Name, Idxs) :-
    hyp_idxs_aux(Atoms, Name, IdxsDup),
    term_variables(IdxsDup, Idxs).

% :- hyp_idxs([h1(N, H1, P1), h2(N, H2, P2)], H1, Idxs).


