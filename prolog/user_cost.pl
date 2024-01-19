:- set(evalfn,user).
cost(_Clause,[P,N,L],Cost):-
   L = 1 -> Cost = inf;
   (Cost = N - P).