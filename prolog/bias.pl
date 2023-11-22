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

goal_node(N, Idx, P, RelativeIdx) :-
    goal_predc(P),
    prefix(Idx, NodeIdx),
    Fact =.. [P, N, NodeIdx], Fact,
    % print(Fact), nl,
    append(Idx, RelativeIdx, NodeIdx).

hyp_node(N, Idx, Predc, RelativeIdx) :-
    hyp_predc(Predc),
    Fact =.. [Predc, N, _Name, NodeIdx], Fact,
    prefix(Idx, NodeIdx),
    append(Idx, RelativeIdx, NodeIdx).

eq_goal_term(N, Idx1, Idx2) :-
    dif(Idx1, Idx2),
    forall(
        goal_node(N, Idx1, Predc, RelativeIdx1),
        goal_node(N, Idx2, Predc, RelativeIdx1)),
    forall(
        goal_node(N, Idx2, Predc, RelativeIdx2),
        goal_node(N, Idx1, Predc, RelativeIdx2)).

eq_hyp_term(N, Idx1, Idx2) :-
    dif(Idx1, Idx2),
    forall(
        hyp_node(N, Idx1, Predc, RelativeIdx1),
        hyp_node(N, Idx2, Predc, RelativeIdx1)),
    forall(
        hyp_node(N, Idx2, Predc, RelativeIdx2),
        hyp_node(N, Idx1, Predc, RelativeIdx2)).


eq_goal_hyp_term(N, GoalIdx, HypIdx) :-
    forall(
        goal_node(N, GoalIdx, GoalPredc1, RelativeIdx1),
        (
            goal_predc_to_hyp_predc(GoalPredc1, HypPredc1),
            hyp_node(N, HypIdx, HypPredc1, RelativeIdx1)
        )
    ),
    forall(
        goal_node(N, HypIdx, HypPredc2, RelativeIdx2),
        (
            goal_predc_to_hyp_predc(GoalPredc2, HypPredc2),
            hyp_node(N, GoalIdx, GoalPredc2, RelativeIdx2)
        )
    ).

is_goal_root(N, Idx) :-
    \+ (
        goal_predc(P),
        prefix(NodeIdx, Idx), dif(NodeIdx, Idx),
        Fact =.. [P, N, NodeIdx], Fact).

% :- modeh(1, tac(+nat, #string)).
:- modeb(*, dif(+string, +string)).
:- modeb(*, dif(+hyp_idx, +hyp_idx)).
:- modeb(*, dif(+goal_idx, +goal_idx)).
:- modeb(*, goal_position_left(+goal_idx, +goal_idx)).
:- modeb(*, hyp_position_left(+hyp_idx, +hyp_idx)).
:- modeb(*, position_above(+goal_idx, +goal_idx)).
:- modeb(*, position_above(+hyp_idx, +hyp_idx)).
:- modeb(20, eq_goal_term(+nat, +goal_idx, +goal_idx)).
:- modeb(20, eq_hyp_term(+nat, +hyp_idx, +hyp_idx)).
:- modeb(20, eq_goal_hyp_term(+nat, +goal_idx, +hyp_idx)).
:- modeb(20, is_goal_root(+nat, +goal_idx)).


:- determination(tac/2, goal_position_left/2).
:- determination(tac/2, hyp_position_left/2).
:- determination(tac/2, position_above/2).
:- determination(tac/2, is_goal_root/2).
:- determination(tac/2, eq_goal_term/3).
:- determination(tac/2, eq_hyp_term/3).
:- determination(tac/2, eq_goal_hyp_term/3).

:- set(construct_bottom, false).
:- set(refine, auto).
:- set(search, heuristic).
:- set(openlist, 50).
:- set(verbosity, 0).
:- set(clauselength, 100).
:- set(depth, 1000).

:- set(nodes, 15000).
