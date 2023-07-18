only_head(_C :- true).

cost(Clause, [P, N, _L], Cost) :-
  ((only_head(Clause); P is 0) -> Cost is inf; Cost is N - P), !.

syn_member(X, [Y | _]) :- X == Y.
syn_member(X, [_ | Tl]) :- syn_member(X, Tl).

hyp_names_aux([], []).

hyp_names_aux([H|Tl], [N|Names]) :-
    hyp_predc(P),
    H =.. [P, _, N, _], !,
    hyp_names_aux(Tl, Names).

hyp_names(List, Names) :-
    hyp_names_aux(List, NamesDup),
    term_variables(NamesDup, Names).

refine(false, (tac(_) :- true)).

refine(tac(N) :- Body1, Clause):-
    comma_list(Body1, Atoms),
    body_predc(P),
    NewAtom =.. [P, N, _],
    not(syn_member(NewAtom, Atoms)),
    comma_list(Body2, [NewAtom| Atoms]),
    Clause = (tac(N):- Body2).

refine(tac(N) :- Body1, Clause):-
    comma_list(Body1, Atoms),
    hyp_predc(P),
    hyp_names(Atoms, UsedNames),
    member(NewName, [_ | UsedNames]),
    NewAtom =.. [P, N, NewName, _],
    not(syn_member(NewAtom, Atoms)),
    comma_list(Body2, [NewAtom| Atoms]),
    Clause = (tac(N):- Body2).