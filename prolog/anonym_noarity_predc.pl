:- multifile hyp_predc/1.
:- multifile goal_predc/1.
:- multifile hyp_coq_Init_Logic_iff/3.
:- multifile hyp_coq_lambda/3.
:- multifile hyp_coq_Init_Logic_eq/3.
:- multifile hyp_coq_const/3.
:- multifile hyp_coq_Init_Logic_not/3.
:- multifile hyp_coq_int/3.
:- multifile hyp_coq_prod/3.
:- multifile hyp_coq_rel/3.
:- multifile hyp_coq_Init_Logic_or/3.
:- multifile hyp_coq_var/3.
:- multifile hyp_coq_ind/3.
:- multifile hyp_coq_Init_Logic_and/3.
:- multifile hyp_coq_evar/3.
:- multifile hyp_coq_construct/3.
:- multifile goal_coq_Init_Logic_iff/2.
:- multifile goal_coq_Init_Logic_or/2.
:- multifile goal_coq_evar/2.
:- multifile goal_coq_ind/2.
:- multifile goal_coq_rel/2.
:- multifile goal_coq_Init_Logic_not/2.
:- multifile goal_coq_prod/2.
:- multifile goal_coq_var/2.
:- multifile goal_coq_construct/2.
:- multifile goal_coq_lambda/2.
:- multifile goal_coq_Init_Logic_and/2.
:- multifile goal_coq_int/2.
:- multifile goal_coq_const/2.
:- multifile goal_coq_Init_Logic_eq/2.
hyp_coq_Init_Logic_iff(-1, none, []).
hyp_coq_lambda(-1, none, []).
hyp_coq_Init_Logic_eq(-1, none, []).
hyp_coq_const(-1, none, []).
hyp_coq_Init_Logic_not(-1, none, []).
hyp_coq_int(-1, none, []).
hyp_coq_prod(-1, none, []).
hyp_coq_rel(-1, none, []).
hyp_coq_Init_Logic_or(-1, none, []).
hyp_coq_var(-1, none, []).
hyp_coq_ind(-1, none, []).
hyp_coq_Init_Logic_and(-1, none, []).
hyp_coq_evar(-1, none, []).
hyp_coq_construct(-1, none, []).
goal_coq_Init_Logic_iff(-1, []).
goal_coq_Init_Logic_or(-1, []).
goal_coq_evar(-1, []).
goal_coq_ind(-1, []).
goal_coq_rel(-1, []).
goal_coq_Init_Logic_not(-1, []).
goal_coq_prod(-1, []).
goal_coq_var(-1, []).
goal_coq_construct(-1, []).
goal_coq_lambda(-1, []).
goal_coq_Init_Logic_and(-1, []).
goal_coq_int(-1, []).
goal_coq_const(-1, []).
goal_coq_Init_Logic_eq(-1, []).

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

node(N, Idx, P, RelativeIdx) :-
    goal_predc(P),
    Fact =.. [P, N, NodeIdx], Fact,
    prefix(Idx, NodeIdx),
    append(Idx, RelativeIdx, NodeIdx).

node(N, Idx, Predc, RelativeIdx) :-
    hyp_predc(Predc),
    Fact =.. [Predc, N, _Name, NodeIdx], Fact,
    prefix(Idx, NodeIdx),
    append(Idx, RelativeIdx, NodeIdx).

eq_subterm(N, Idx1, Idx2) :-
    dif(Idx1, Idx2),
    forall(
        node(N, Idx1, Predc, RelativeIdx1),
        node(N, Idx2, Predc, RelativeIdx1)),
    forall(
        node(N, Idx2, Predc, RelativeIdx2),
        node(N, Idx1, Predc, RelativeIdx2)).