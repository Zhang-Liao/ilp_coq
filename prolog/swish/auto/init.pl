/*
To run do 'induce'
?- induce(Program).
*/
:- use_module(library(aleph)).
:- use_module(library(dialect/xsb/setof)).

:- if(current_predicate(use_rendering/1)).
:- use_rendering(prolog).
:- endif.
:- aleph.
% :- aleph_set(construct_bottom, false).
:- aleph_set(search, heuristic).
:- modeh(1,tac(+nat)).
