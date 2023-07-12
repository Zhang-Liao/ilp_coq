
above(X, Y) :- nonvar(X), nonvar(Y), dif(X, Y), prefix(X, Y).
below(X, Y) :- nonvar(X), nonvar(Y), dif(X, Y), prefix(Y, X).

vertical(X, Y) :- nonvar(X), nonvar(Y), dif(X, Y), prefix(X, Y).
vertical(X, Y) :- nonvar(X), nonvar(Y), dif(X, Y), prefix(Y, X).

horizon([X], [Y]) :- nonvar(X), nonvar(Y), dif(X, Y).
horizon([H|X], [H|Y]) :- nonvar(X), nonvar(Y), dif(X, Y), horizon(X, Y).

% intro(1).
goal_nat(1, [0]).
goal_plus(1, [0, 1]).
hyps_plus(1, a, [a, 0]).
hyps_plus(1, a, [a, 0, 1]).
goal_nat(2, [0]).
goal_plus(2, [0, 1]).
hyps_plus(2, a, [a, 0]).
hyps_plus(2, a, [a, 1]).

% difference ?
intro1(V1) :- hyps_plus(V1, V2, V3), hyps_plus(V1, V2, V4), vertical(V3, V4).
intro2(V1) :- hyps_plus(V1, V2, V3), hyps_plus(V1, V2, V4), above(V3, V4).
intro3(V1) :- hyps_plus(V1, V2, V3), hyps_plus(V1, V2, V4), below(V3, V4).