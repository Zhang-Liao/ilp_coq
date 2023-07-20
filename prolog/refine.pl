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

get_idxs(A1, A2, Idx1, Idx2) :-
    A1 =.. [P1, _, Idx1],
    A2 =.. [P2, _, Idx2],
    body_predc(P1), body_predc(P2).

get_idxs(A1, A2, Idx1, Idx2) :-
    A1 =.. [P1, _, _, Idx1],
    A2 =.. [P2, _, _, Idx2],
    hyp_predc(P1), hyp_predc(P2).

position_left([X], [Y]) :- !, X < Y.
position_left([H|X], [H|Y]) :- position_left(X, Y).

position_above(X, Y) :- dif(X,Y), prefix(X, Y).

newclause(Atoms1, NewAtom, Head, Clause) :-
    not(syn_member(NewAtom, Atoms1)),
    (Atoms1 = [true] ->
        Body2 = NewAtom
    ;   append(Atoms1, [NewAtom], Atoms2),
        comma_list(Body2, Atoms2)),
    Clause = (Head:- Body2).

refine(false, (tac(_) :- true)).

refine(tac(N) :- Body, Clause):-
    comma_list(Body, Atoms),
    body_predc(P),
    NewAtom =.. [P, N, _],
    newclause(Atoms, NewAtom, tac(N), Clause).

refine(tac(N) :- Body, Clause):-
    comma_list(Body, Atoms),
    hyp_predc(P),
    hyp_names(Atoms, UsedNames),
    member(NewName, [_ | UsedNames]),
    NewAtom =.. [P, N, NewName, _],
    newclause(Atoms, NewAtom, tac(N), Clause).

refine(tac(N) :- Body, Clause):-
    comma_list(Body, Atoms),
    member(A1, Atoms),
    member(A2, Atoms),
    dif(A1, A2),
    get_idxs(A1, A2, Idx1, Idx2),
    ( NewAtom =.. [position_left, Idx1, Idx2]
    ; NewAtom =.. [position_above, Idx1, Idx2]),
    newclause(Atoms, NewAtom, tac(N), Clause).
