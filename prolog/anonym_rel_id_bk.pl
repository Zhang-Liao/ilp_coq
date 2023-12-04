:- multifile hyp_node/5.

hyp_node(dummy, -1, [], [], dummy).

hyp_typ(hyp_ass).
hyp_typ(hyp_dc).
hyp_typ(hyp_dt).

position_left([X], [Y]) :- !, integer(X), integer(Y), X < Y.
position_left([H|X], [H|Y]) :- position_left(X, Y).

hyp_position_left([Name, Type| Idx1], [Name, Type| Idx2]) :-
    hyp_typ(Type), position_left(Idx1, Idx2).

goal_position_left(Idx1, Idx2) :- position_left(Idx1, Idx2).

above_aux(X, Y) :- dif(X,Y), prefix(X, Y).

% N or _N
goal_above(N, Idx1, Idx2) :-
    above_aux(Idx1, Idx2),
    \+ (
        above_aux(Idx1, Idx3),
        above_aux(Idx3, Idx2),
        goal_node(_Predc, N, Idx3, _Ident)).

hyp_above(N, Idx1, Idx2) :-
    above_aux(Idx1, Idx2),
    \+ (
        above_aux(Idx1, Idx3),
        above_aux(Idx3, Idx2),
        hyp_node(_Predc, N, _Name, Idx3, _Ident)).


nat_idx([]).
nat_idx([H | Tl]) :- integer(H), nat_idx(Tl).

goal_idx(Idx) :- nat_idx(Idx).

hyp_idx([_, Typ| Idx]) :- hyp_typ(Typ), nat_idx(Idx).

goal_term_children_in_goal_term(N, Idx1, Idx2):-
    forall(
        (
            prefix(Idx1, Child1),
            goal_node(Predc, N, Child1, Ident)
        ),
        (
            append(Idx1, RelativeIdx1, Child1),
            append(Idx2, RelativeIdx1, Child2),
            goal_node(Predc, N, Child2, Ident)
        )
    ).


goal_term_children_in_hyp_term(N, Idx1, Idx2) :-
    forall(
        (
            prefix(Idx1, Child1),
            goal_node(Predc, N, Child1, Ident)
        ),
        (
            append(Idx1, RelativeIdx1, Child1),
            append(Idx2, RelativeIdx1, Child2),
            hyp_node(Predc, N, _Name, Child2, Ident)
        )
    ).

hyp_term_children_in_goal_term(N, HypIdx, GoalIdx) :-
    forall(
        (
            prefix(HypIdx, Child1),
            hyp_node(Predc, N, _Name, Child1, Ident)
        ),
        (
            append(HypIdx, RelativeIdx1, Child1),
            append(GoalIdx, RelativeIdx1, Child2),
            goal_node(Predc, N, Child2, Ident)
        )
    ).

eq_goal_term(N, Idx1, Idx2) :-
    dif(Idx1, Idx2),
    goal_term_children_in_goal_term(N, Idx1, Idx2),
    goal_term_children_in_goal_term(N, Idx2, Idx1).

eq_goal_hyp_term(N, GoalIdx, HypIdx) :-
    goal_term_children_in_hyp_term(N, GoalIdx, HypIdx),
    hyp_term_children_in_goal_term(N, HypIdx, GoalIdx).

is_goal_root(N, Idx) :-
\+ (
    prefix(Parent, Idx), 
    dif(Parent, Idx),
    goal_node(_Predc, N, Parent, _Ident)).

is_hyp_root(N, Idx) :-
\+ (
    prefix(Parent, Idx),
    hyp_idx(Parent),
    dif(Parent, Idx),
    hyp_node(_Predc, N, _Name, Parent, _Ident)).

rmv_ele_from_list(_, [], []).
rmv_ele_from_list(X, [X | Tl], Tl).
rmv_ele_from_list(X, [H | Tl1], [H | Tl2]) :-
    dif(X, H),
    rmv_ele_from_list(X, Tl1, Tl2).

dif_lists(L, [], L).

dif_lists([], L, L).

dif_lists([H |Tl], L, Difs) :-
    member(H, L), !, rmv_ele_from_list(H, L, LeftL),
    dif_lists(Tl, LeftL, Difs).

dif_lists([H |Tl], L, [H | Difs]) :- dif_lists(Tl, L, Difs).

% Len < 3 does not work in p4n4 QArith.
similar_lists(L1, L2) :- dif_lists(L1, L2, Dif), length(Dif, Len), Len < 2.

similar_goal_terms(N, Idx1, Idx2) :-
    % \+ (eq_goal_term(N, Idx1, Idx2)),
    dif(Idx1, Idx2),
    findall(
        Child1, 
        (prefix(Idx1, ChildIdx1), goal_node(_Predc1, N, ChildIdx1, Child1)), 
        Children1),
    findall(
        Child2, 
        (prefix(Idx2, ChildIdx2), goal_node(_Predc2, N, ChildIdx2, Child2)), 
        Children2),
    similar_lists(Children1, Children2).

similar_goal_hyp_terms(N, GoalIdx, HypIdx) :-
    findall(
        Child1, 
        (prefix(GoalIdx, ChildIdx1), goal_node(_Predc1, N, ChildIdx1, Child1)), 
        Children1),
    findall(
        Child2, 
        (prefix(HypIdx, ChildIdx2), hyp_node(_Predc2, N, _, ChildIdx2, Child2)), 
        Children2),
    similar_lists(Children1, Children2).