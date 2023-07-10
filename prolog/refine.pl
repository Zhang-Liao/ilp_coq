/*
To run do 'induce'
?- induce(Program).
*/
:- use_module(library(aleph)).
:- use_module(library(dialect/xsb/setof)).

:- if(current_predicate(use_rendering/1)).
:- use_rendering(prolog).
:- endif.
:- aleph.
:- aleph_set(construct_bottom, false).
:- aleph_set(refine, user).
:- style_check(-discontiguous).
:-begin_bg.
syn_member(X, [Y | _]) :- X == Y.
syn_member(X, [_ | Tl]) :- syn_member(X, Tl).

input_vars_aux([], []).

input_vars_aux([H|Tl], Vars) :-
    H == true, !,
    input_vars_aux(Tl, Vars).

input_vars_aux([H|Tl], [V|Vars]) :-
    H = tac(V, _), !,
    input_vars_aux(Tl, Vars).

input_vars_aux([H|Tl], [V|Vars]) :-
    body_pred(P),
    H =.. [P, _, V], !,
    input_vars_aux(Tl, Vars).

input_vars(List, Vars):-
    input_vars_aux(List, VarsDup),
    term_variables(VarsDup, Vars).

output_vars_aux([], []).

output_vars_aux([H|Tl], Vars) :-
    H = true, !,
    output_vars_aux(Tl, Vars).

output_vars_aux([H|Tl], [V|Vars]) :-
    H = tac(_, V), !,
    output_vars_aux(Tl, Vars).

output_vars_aux([H|Tl], [V|Vars]) :-
    body_pred(P),
    H =.. [P, _, V], !,
    output_vars_aux(Tl, Vars).

output_vars(List, Vars):-
    output_vars_aux(List, VarsDup),
    term_variables(VarsDup, Vars).

refine(aleph_false, (tac(_) :- true)).

refine(tac(N) :- Body1, Clause):-
    comma_list(Body1, Atoms),
    body_predc(P),
    NewAtom =.. [P, N, _],
    not(syn_member(NewAtom, Atoms)),
    comma_list(Body2, [NewAtom| Atoms]),
    Clause = (tac(N):- Body2).

:-end_bg.