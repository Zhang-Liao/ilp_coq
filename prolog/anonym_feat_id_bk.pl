:- multifile goal_node/4.
:- multifile hyp_node/5.

goal_node(dummy, -1, [], dummy).
hyp_node(dummy, -1, [], [], dummy).

:- consult('/home/zhangliao/ilp_out_coq/ilp_out_coq/prolog/common_bk.pl').

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
            append(Idx1, RelativeIdx, Child1),
            append(Idx2, RelativeIdx, Child2),
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
            append(HypIdx, RelativeIdx, Child1),
            append(GoalIdx, RelativeIdx, Child2),
            goal_node(Predc, N, Child2, Ident)
        )
    ).

hyp_term_children_in_hyp_term(N, HypIdx1, HypIdx2) :-
    forall(
        (
            prefix(HypIdx1, Child1),
            hyp_node(Predc, N, Name1, Child1, Ident)
        ),
        (
            append(HypIdx1, RelativeIdx, Child1),
            append(HypIdx2, RelativeIdx, Child2),
            dif(Name1, Name2),
            dif(HypIdx1, HypIdx2),
            hyp_node(Predc, N, Name2, Child2, Ident)
        )
    ).

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


similar_goal_terms(N, Idx1, Idx2) :-
    \+ prefix(Idx1, Idx2),
    \+ prefix(Idx2, Idx1),
    \+ (eq_goal_term(N, Idx1, Idx2)),
    findall(
        Child1,
        (prefix(Idx1, ChildIdx1), goal_node(_Predc1, N, ChildIdx1, Child1)),
        Children1),
    findall(
        Child2,
        (prefix(Idx2, ChildIdx2), goal_node(_Predc2, N, ChildIdx2, Child2)),
        Children2),
    similar_lists(Children1, Children2).