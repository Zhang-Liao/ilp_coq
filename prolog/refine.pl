only_head(_C :- true).

cost(Clause, [P, N, _L], Cost) :-
  ((only_head(Clause); P is 0) -> Cost is inf; Cost is N - P), !.

syn_mem(X, [Y | _]) :- X == Y.
syn_mem(X, [_ | Tl]) :- syn_mem(X, Tl).

not_syn_mem(L, X) :- not(syn_mem(X, L)).

hyp_names_aux([], []).

hyp_names_aux([H|Tl], [N|Names]) :-
    H =.. [P, _, N, _],
    hyp_predc(P), !,
    hyp_names_aux(Tl, Names).

hyp_names_aux([_|Tl], Names) :- hyp_names_aux(Tl, Names).

hyp_names(List, Names) :-
    hyp_names_aux(List, NamesDup),
    term_variables(NamesDup, Names).

idxs_in_same_term(A1, A2, Idx1, Idx2) :-
    A1 =.. [P1, _, Idx1],
    A2 =.. [P2, _, Idx2],
    goal_predc(P1), goal_predc(P2).

idxs_in_same_term(A1, A2, Idx1, Idx2) :-
    A1 =.. [P1, _, Name, Idx1],
    A2 =.. [P2, _, Name, Idx2],
    hyp_predc(P1), hyp_predc(P2).

dif_vars(V, Vs) :- maplist(dif(V), Vs).

goal_idxs_aux([], []).

goal_idxs_aux([Hd|Tl], [Idx|Idxs]) :-
    Hd =.. [P, _, Idx],
    goal_predc(P), goal_idxs_aux(Tl, Idxs).

goal_idxs_aux([_|Tl], [_|Idxs]) :- goal_idxs_aux(Tl, Idxs).

goal_idxs(Atoms, Idxs) :-
    goal_idxs_aux(Atoms, IdxsDup),
    term_variables(IdxsDup, Idxs).

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

position_left([X], [Y]) :- !, X < Y.
position_left([H|X], [H|Y]) :- position_left(X, Y).

position_above(X, Y) :- dif(X,Y), prefix(X, Y).

newclause(Atoms1, NewAtoms, Head, Clause) :-
    % maplist(dif(V), Vs).
    % not(syn_mem(NewAtom, Atoms1)),
    % maplist(not_syn_mem(NewAtom, Atoms))
    % avoid including left(A, B) twice
    maplist(not_syn_mem(Atoms1), NewAtoms),
    (Atoms1 = [true] ->
        comma_list(Body2, NewAtoms)
    ;   append(Atoms1, NewAtoms, Atoms2),
        comma_list(Body2, Atoms2)),
    Clause = (Head:- Body2).

refine(false, (tac(_) :- true)).

% refine(tac(N) :- Body, Clause):-
%     comma_list(Body, Atoms),
%     goal_predc(P),
%     NewAtom =.. [P, N, NewIdx],
%     goal_idxs(Atoms, Idxs),
%     ((Body = true; Idxs = []) ->
%         newclause(Atoms, [NewAtom], tac(N), Clause)
%         ; newclause(Atoms, [dif_vars(NewIdx, Idxs), NewAtom], tac(N), Clause)).

refine(tac(N) :- Body, Clause):-
    comma_list(Body, Atoms),
    hyp_predc(P),
    hyp_names(Atoms, UsedNames),
    member(NewName, [_ | UsedNames]),
    NewAtom =.. [P, N, NewName, NewIdx],
    hyp_idxs(Atoms, NewName, Idxs),
    ((Body = true; Idxs = []) ->
        newclause(Atoms, [NewAtom], tac(N), Clause)
        ; newclause(Atoms, [dif_vars(NewIdx, Idxs), NewAtom], tac(N), Clause)).

% refine(tac(N) :- Body, Clause):-
%     comma_list(Body, Atoms),
%     member(A1, Atoms),
%     member(A2, Atoms),
%     dif(A1, A2),
%     idxs_in_same_term(A1, A2, Idx1, Idx2),
%     ( NewAtom =.. [position_left, Idx1, Idx2]
%     ; NewAtom =.. [position_above, Idx1, Idx2]),
%     newclause(Atoms, [NewAtom], tac(N), Clause).
