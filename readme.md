# ILP for Coq

## Encoding

Rel | Evar | Construct | Ind  | Var | Const | Int | Float
| Prod (_, t, b) | Lambda (_, t, b) | Fix (_, (_, tl, bl))
| CoFix (_, (_, tl, bl))
| Case (ci, pb, b, l)
| LetIn (na, b, t, c)
| Proj (p, c)
| Cast (b, k, t)
| App (h, l)
| Sort | Meta

### anonym

ignore: Int (mis include), Float (mis include), Fix, CoFix, Case, LetIn, Proj, Sort, Meta

## origin

ignore: Int (mis include), Float (mis include), Sort, Meta, App
include: the other

Cannot show all the details of encoding because it is complicate, e.g., only one identidier of Constructor ... To explain, first, show the tree structure, then show encoding by position. Some constructors (App,...) are ignored because they have been indicated by their arguments. Appendix pseudocode shows the structure of Coq, which predicates are used, do not need explain the meaning of each argument. ML community cannot understand anyway.
For anonymous,only keep some constructors.


## do not use mode that has identifiers

goal_node(coq_const,1943,[0,1,0,0,0],coq_QArith_QArith_base_Qpower_positive).
with n type (coq_const), the space is n * number of idx * number of different
identifers = $n^3$.
If we use above for the clause, search space is $n^6$
30000 node heuristic can only generate a clause of 5 atoms.
tac(A,"reflexivity") :-
   goal_node(coq_Init_Logic_iff,A,B,C), goal_node(coq_Init_Logic_iff,A,D,C), is_goal_root(A,D), goal_node(coq_Init_Logic_iff,A,D,E), goal_node(coq_var,A,D,F).

## choose a search strategy

for simpl, assumption, trivial, reflexivity, auto.
* no ident
   * bf. 30 rules.
   * bf open list 10. fewer rules. do not search all the short rules.
   * heuris. Can learn more rules. heuris learn 51 rules.
   * heuris open list 50. can only learn 36 rules and simple structures.
* ident
   * heuris. 51 rules. Can learn one rule for trivial. Fewer rules for reflexivity. Space too large? similar_goal_terms only occurs once.