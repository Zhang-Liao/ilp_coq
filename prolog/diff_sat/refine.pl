only_head(_C :- true).

cost(Clause, [P, N, _L], Cost) :-
  ((only_head(Clause); P is 0) -> Cost is inf; Cost is N - P), !.

myplus(A, B) :- A > B.
test_map(A) :- maplist(myplus(A), [1,2]).

dif_vars(V, Vs) :- maplist(dif(V), Vs).

% dif_vars_aux(V, [], []).

% dif_vars_aux(V, [Hd| Tl], [Dif|Difs]) :-
%     Dif = dif(V, Hd), !, dif_vars_aux(V, Tl, Difs).

% dif_vars(V, Vs, Difs) :-
%     dif_vars_aux(V, Vs, List),
%     comma_list(Difs, List).

refine(false, Clause) :-
    Clause = (tac(A) :- coq_setoid_ring_ring_theory_srsub(A,B,C), dif_vars(D, B), prod(A,D,E)).

% refine(false, Clause) :-
%     Clause = (tac(A) :- coq_setoid_ring_ring_theory_srsub(A,B,C), dif(D,B), dif(D, A), prod(A,D,E)).

% refine(false, Clause) :-
%     Clause = (tac(A) :- coq_setoid_ring_ring_theory_srsub(A,B,C), dif(D, A), prod(A,D,E)).


% refine(false, Clause) :-
%     Clause = (tac(A) :- coq_setoid_ring_ring_theory_srsub(A,B,C), dif(D, B), prod(A,D,E)).

% refine(false, Clause) :-
%     Clause = (tac(A) :- coq_setoid_ring_ring_theory_srsub(A,B,C), prod(A,D,E)).

% refine(false, Clause) :-
%     Clause = (tac(A) :- coq_setoid_ring_ring_theory_srsub(A,B,C), test_map(7), prod(A,D,E)).

