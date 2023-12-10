hyp_typ(hyp_ass).
hyp_typ(hyp_dc).
hyp_typ(hyp_dt).

position_left([X], [Y]) :- !, integer(X), integer(Y), X < Y.
position_left([H|X], [H|Y]) :- position_left(X, Y).

hyp_position_left([Name, Type| Idx1], [Name, Type| Idx2]) :-
    hyp_typ(Type), position_left(Idx1, Idx2).

goal_position_left(Idx1, Idx2) :- position_left(Idx1, Idx2).

above_aux(X, Y) :- dif(X,Y), prefix(X, Y).

nat_idx([]).
nat_idx([H | Tl]) :- integer(H), nat_idx(Tl).

goal_idx(Idx) :- nat_idx(Idx).

hyp_idx([_, Typ| Idx]) :- hyp_typ(Typ), nat_idx(Idx).

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

eq_goal_term(N, Idx1, Idx2) :-
    dif(Idx1, Idx2),
    goal_term_children_in_goal_term(N, Idx1, Idx2),
    goal_term_children_in_goal_term(N, Idx2, Idx1).

eq_goal_hyp_term(N, GoalIdx, HypIdx) :-
    goal_term_children_in_hyp_term(N, GoalIdx, HypIdx),
    hyp_term_children_in_goal_term(N, HypIdx, GoalIdx).
