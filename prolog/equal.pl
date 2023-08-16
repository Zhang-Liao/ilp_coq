feat1(1, [0]).
feat2(1, [0,1]).
feat3(1, [0,2,3]).
feat3(1, [0,2,1]).

feat1(1, [1]).
feat2(1, [1,1]).
feat3(1, [1,2,3]).
feat3(1, [1,2,1]).
feat3(1, [2,2]).

modeb(feat1).
modeb(feat2).
modeb(feat3).

nat_idx([]).
nat_idx([H | Tl]) :- integer(H), nat_idx(Tl).

goal_idx(Idx) :- nat_idx(Idx).

position_above(X, Y) :- dif(X,Y), prefix(X, Y).

succ(Idx, N, (P, RelativeIdx)) :-
    modeb(P), Fact =.. [P, N, NodeIdx], Fact,
    prefix(Idx, NodeIdx),
    append(Idx, RelativeIdx, NodeIdx).

subterm(Idx, N, SubTerm) :-
    goal_idx(Idx), !,
    findall(Node,
        succ(Idx, N, Node),
        Nodes),
    Nodes \== [],
    % print(Nodes),
    sort(2, @<, Nodes, SubTerm).

eq_subterm(Idx1, Idx2, N) :-
    dif(Idx1, Idx2),
    subterm(Idx1, N, T1),
    subterm(Idx2, N, T2),
    T1 = T2.

% subterm([0], 1).
% eq_subterm([0], [1], 1).
% eq_subterm([0], [2], 1).
