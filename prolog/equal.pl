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

% succ(Idx, N, (P, RelativeIdx)) :-
%     modeb(P), Fact =.. [P, N, NodeIdx], Fact,
%     prefix(Idx, NodeIdx),
%     append(Idx, RelativeIdx, NodeIdx).

% subterm(Idx, N, SubTerm) :-
%     goal_idx(Idx), !,
%     findall(Node,
%         (print('find node'), nl, succ(Idx, N, Node)),
%         Nodes),
%     Nodes \== [],
%     % print(Nodes),
%     sort(2, @<, Nodes, SubTerm).

node(Idx, N, P, RelativeIdx) :-
    modeb(P), Fact =.. [P, N, NodeIdx], Fact,
    prefix(Idx, NodeIdx),
    append(Idx, RelativeIdx, NodeIdx).

eq_subterm(Idx1, Idx2, N) :-
    dif(Idx1, Idx2),
    forall(
        node(Idx1, N, Predc, RelativeIdx1),
        node(Idx2, N, Predc, RelativeIdx1)),
    forall(
        node(Idx2, N, Predc, RelativeIdx2),
        node(Idx1, N, Predc, RelativeIdx2)).
% subterm([0], 1).
% eq_subterm([0], [1], 1). true
% eq_subterm([0], [2], 1). false
