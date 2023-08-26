f0(0).
f1(1).

tac(X, "simpl") :- f0(X).

tac(X, "auto") :- f1(X).