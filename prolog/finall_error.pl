:-style_check(-discontiguous).
predc1(1,[0]).
predc2(1,[0,1]).
predc2(1,[0,1,0]).
predc2(1,[0,2]).
predc2(1,[0,2,0]).

predc1(2,[0]).
predc2(2,[0,1]).
predc1(2,[0,1,0]).
predc2(2,[0,2]).
predc1(2,[0,2, 0]).

predc1(3,[0]).
predc2(3,[0,3]).
predc1(3,[0,4]).

predc1(4,[0]).
predc1(4,[0,3]).
predc2(4,[0,4]).


:- modeh(2, tac(+nat, "assumption")).
% :- modeb(3, predc1(+nat, -goal_idx)).
:- modeb(3, predc2(+nat, -goal_idx)).


:- determination(tac/2, predc1/2).
:- determination(tac/2, predc2/2).

coq_goal_predc(predc1).

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

myprefix([H], []).
myprefix([H|Tl1], [H|Tl2]) :- myprefix(Tl1,Tl2).

% succ(N, Idx, P, RelativeIdx) :-
%     print('before determination predicate'), nl,
%     determination(tac/2, P/2),
%     print('after determination predicate'), nl,
%     % coq_goal_predc(P),
%     prefix(Idx, NodeIdx),
%     Fact =.. [P, N, NodeIdx],
%     Fact,
%     append(Idx, RelativeIdx, NodeIdx).

% mysucc(N, Idx, P, RelativeIdx) :-
%     print('before determination predicate'), nl,
%     P = 'none', RelativeIdx = [1],
%     print('after determination predicate'), nl.
% Error: cannot invoke functor in findall?
subterm(N, Idx, SubTerm) :-
    p_message('before check goal idx'),
    goal_idx(Idx),
    % !,
    p_message('after check goal idx'),
    findall(
        (P, RelativeIdx),
        ( print('before succ'), nl
        , coq_goal_predc(P)
        % coq_goal_predc(P),
        , Fact =.. [P, N, NodeIdx]
        , print('before fact'), nl
        , print(fact(Fact)), nl
        , Fact
        , print(myprefix(Idx, NodeIdx))
        , myprefix(Idx, NodeIdx)
        , print('after fact'), nl
        , append(Idx, RelativeIdx, NodeIdx)
        , print('after succ'), nl),
    Nodes),
    p_message('after findall'),
    Nodes \== [],
    % print(Nodes),
    sort(2, @<, Nodes, SubTerm).

eq_subterm(N, Idx1, Idx2) :-
    % p_message('before dif'),
    dif(Idx1, Idx2),
    subterm(N, Idx1, T1),
    subterm(N, Idx2, T2),
    T1 = T2.

:- modeb(3, eq_subterm(+nat, +goal_idx, +goal_idx)).
:- determination(tac/2, eq_subterm/3).

:- set(construct_bottom, false).
:- set(refine, auto).
:- set(search, heuristic).
% :- set(openlist, 20).
:- set(verbosity, 1).
:- set(clauselength, 5).

:- set(evalfn, user).
:- set(nodes, 100).
% :- set(explore, true).
% prune(tac(X)) :- nonvar(X).
% prune((tac(X) :- _)) :- nonvar(X).

only_head(_C :- true).

cost(Clause, [P, N, _L], Cost) :-
((only_head(Clause); P is 0) -> Cost is inf; Cost is N - P), !.
:- set(noise, 0).
