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

heads of are the same as leaves

### anonym

#### leaf

let atom_to_predc_and_id tm =
match tm with
| Rel -> ("coq_rel", Some "coq_rel")
| Evar -> ("coq_evar", Some "coq_evar")
| Construct (c, _u) -> "coq_construct", Some id
| Ind (i, _u) -> "coq_ind", Some id
| Var id -> ("coq_var", Some (Names.Id.to_string id))
| Const (c, _u) -> "coq_const", Some id

#### coq constructor

| Prod -> "coq_prod"
| Lambda (_, t, b) -> "coq_lambda"
| Case (ci, pb, b, l) -> "coq_case"

### origin

#### origin leaf

| Rel _-> "coq_rel"
| Evar _-> "coq_evar"
| Construct (c, _u) -> constructor2s c
| Ind (i, _u) -> inductive2s i
| Var id -> "coq_var_" ^ id2s id
| Const (c,_u) -> constant2s c
| Int n -> "coq_int"
| Float n -> "coq_float"
| Sort _-> "coq_sort"
| Meta _-> "coq_meta"

#### origin coq constructor

| Prod _-> "coq_prod"
| Lambda _-> "coq_lambda"
| Fix _-> "coq_fix"
| CoFix _-> "coq_cofix"
| Case _-> "coq_case"
| LetIn _-> "coq_letin"
| Proj _-> "coq_proj"
| Cast _-> "coq_cast"
| App _-> "coq_app"

## choose a search strategy

for simpl, assumption, trivial, reflexivity, auto.

* no ident
  * bf. 30 rules.
  * bf open list 10. fewer rules. do not search all the short rules.
  * heuris. Can learn more rules. heuris learn 51 rules.
  * heuris open list 50. can only learn 36 rules and simple structures.
* ident
  * heuris. 51 rules. Can learn one rule for trivial. Fewer rules for reflexivity. Space too large? similar_goal_terms only occurs once.

## bk

### do not use mode that has identifiers

goal_node(coq_const,1943,[0,1,0,0,0],coq_QArith_QArith_base_Qpower_positive).
with n type (coq_const), the space is n _number of idx_ number of different
identifers = $n^3$.
If we use above for the clause, search space is $n^6$
30000 node heuristic can only generate a clause of 5 atoms.
tac(A,"reflexivity") :-
   goal_node(coq_Init_Logic_iff,A,B,C), goal_node(coq_Init_Logic_iff,A,D,C), is_goal_root(A,D), goal_node(coq_Init_Logic_iff,A,D,E), goal_node(coq_var,A,D,F).

### use identifiers

train in QArith, valid in Lists. If do not use:

* anonym_rel best at p16n16. f1 = 0.216. work for simpl, intros, auto, assumption.
  * But auto, assumption has a lot of FP. use identifiers?
  * reflexivity does not work. no equal_goal_terms are learned.
similar_goal_terms ignore equal_goal_terms. May also be related to do not use identifiers.
  * seldom predict assumption.
* anonym_prop best at p16n32. f1=0.214. only work for simpl, intros

## filter

Do not contain reorder because after removing bad rules, reoredred predictions are different.

## orthogonalization

Even if in the validation dataset anonym_rel can learn good rules, but in theories/Init, "exact eq_refl" occurs for 511 times and can also be solved by auto. Cause a lot of false positives. If replace "exact eq_refl" to "auto", the performance will be very good. In plugins/setoid_ring, false positives are caused by using "reflexivity" and "trivial" to replace "auto". In theories/vectors, "reflexivity" cause problems.
But in setoid_ring, seems not due to orthogo. in setoid_ring, a lot of reflexivity. Also intros with low precision (0.16) in Lists work well here (f1, 0.37).

why hard written replace reflexivity, trivial, assumption with auto?
running takes a lot of time, sometimes cannot be finished in time.

## predicates

### intros

Seems very difficult to learn rules with high precision, too many choices.
intros :- prod, is_root. can be applied with many states. destruct, unfold, induction ... a lof of intros with arguments ...

## do not work after orthogonalization

still exists some very simple rules that causes a lot of FP.

1. higher precision? -> work now
2. valid in two sets?

## why too many neg pos does work?

Our BK can only capture a small part of the usage of tactics.

tac(A,"auto",7) :-
    goal_node(coq_const,A,B,C), is_goal_root(A,B), hyp_node(coq_const,A,D,E,C), is_hyp_root(A,E), eq_goal_hyp_term(A,B,E).
"TP": 24, "FP": 3, "FN": 943, "TN": 2618, "precision": 0.8888889

## f1 in test dataset

in "theories/Vectors": 0.2278481, lower than other theories. The tactics used there are quite nontrivial.
score not high in sorting: auto in sorting is difficult to learn
"state":"T : Tree, X0 : (forall (a : A) (T1 T2 : Tree), leA_Tree a T1 -> leA_Tree a T2 -> is_heap T1 -> P T1 -> is_heap T2 -> P T2 -> P (Tree_Node a T1 T2)), X : (P Tree_Leaf), P : (Tree -> Type), singletonBag := (SingletonBag eqA eqA_dec) : (A -> multiset A), emptyBag := (EmptyBag A) : (multiset A), leA_antisym : (forall x y : A, leA x y -> leA y x -> eqA x y), leA_trans : (forall x y z : A, leA x y -> leA y z -> leA x z), leA_refl : (forall x y : A, eqA x y -> leA x y), eqA_dec : (forall x y : A, {eqA x y} + {~ eqA x y}), leA_dec : (forall x y : A, {leA x y} + {leA y x}), gtA := (fun x y : A => ~ leA x y) : (A -> A -> Prop), eqA : (relation A), leA : (relation A), A : Type |- (is_heap Tree_Leaf -> P Tree_Leaf)

## case studies

tac(A,"simpl",6) :-
    goal_node(coq_const,A,B,C), goal_node(coq_const,A,D,E), goal_above(A,D,B), goal_node(coq_var,A,F,G), goal_above(A,B,F), goal_node(coq_construct,A,H,I), goal_above(A,B,H).

tac(A,"auto",16) :-
    hyp_node(coq_const,A,B,C,D), is_hyp_root(A,C), goal_node(coq_const,A,E,D), eq_goal_hyp_term(A,E,C), is_goal_root(A,E).

data/json/ortho/feat/tune/QArith/test_theory/theories/Lists/rel/anonym/p16n4/alltac_rule.pl
8450c7_rule.pl:   goal_node(coq_ind,A,B,C), hyp_node(coq_ind,A,D,E,F), goal_node(coq_Init_Logic_eq,A,G,H), is_goal_root(A,G),
zhangliao@dai-05:~/ilp_out_coq/ilp_out_coq/data/json/ortho/predicate/anonym/tune/QArith/train/rel/p16n4$ cat 8450c7.f
{"state":"H : (0 <= Z.neg n)%Z, n : positive, a : Z |- ((0 ?= Z.neg n)%Z = Gt)","hyps":[["coq_ind","Coq.Numbers.BinNums.Z",0,"a","hyp_ass",[]],["coq_ind","Coq.Numbers.BinNums.positive",0,"n","hyp_ass",[]],["coq_const","Coq.ZArith.BinInt.Z.le",2,"H","hyp_ass",[0]],["coq_construct","Coq.Numbers.BinNums.Z0",0,"H","hyp_ass",[0,0]],["coq_construct","Coq.Numbers.BinNums.Zneg",1,"H","hyp_ass",[0,1,0]],["coq_var","n",0,"H","hyp_ass",[0,1,0,0]]],"goal":[["Coq.Init.Logic.eq","Coq.Init.Logic.eq",3,[0]],["coq_ind","Coq.Init.Datatypes.comparison",0,[0,0]],["coq_const","Coq.ZArith.BinIntDef.Z.compare",2,[0,1,0]],["coq_construct","Coq.Numbers.BinNums.Z0",0,[0,1,0,0]],["coq_construct","Coq.Numbers.BinNums.Zneg",1,[0,1,0,1,0]],["coq_var","n",0,[0,1,0,1,0,0]],["coq_construct","Coq.Init.Datatypes.Gt",0,[0,2]]],"tac":"auto"}

tac(A,"auto",9) :-
    goal_node(coq_ind,A,B,C), hyp_node(coq_ind,A,D,E,F), goal_node(coq_Init_Logic_eq,A,G,H), is_goal_root(A,G), goal_node(coq_construct,A,I,J), goal_position_left(B,I), goal_node(coq_construct,A,K,J), goal_position_left(K,I).

tac(A,"auto",10) :-
    goal_node(coq_construct,A,B,C), goal_node(coq_Init_Logic_eq,A,D,E), goal_above(A,D,B), goal_node(coq_construct,A,F,C), eq_goal_term(A,F,B).

tac(A,"f_equal",0) :-
    goal_node(coq_Init_Logic_eq,A,B,C), goal_node(coq_const,A,D,E), goal_node(coq_const,A,F,G), similar_goal_terms(A,F,D), goal_above(A,B,D).

tac(A,"split",0) :-
    goal_node(coq_Init_Logic_and,A,B,C), is_goal_root(A,B).

|- (g' _(xc_ x) = xc _(g'_ x))
"goal":[["Coq.Init.Logic.eq","Coq.Init.Logic.eq",3,[0]],["coq_ind","Coq.Numbers.BinNums.Z",0,[0,0]],["coq_const","Coq.ZArith.BinIntDef.Z.mul",2,[0,1,0]],["coq_var","g'",0,[0,1,0,0]],["coq_const","Coq.ZArith.BinIntDef.Z.mul",2,[0,1,0,1,0]],["coq_var","xc",0,[0,1,0,1,0,0]],["coq_var","x",0,[0,1,0,1,0,1]],["coq_const","Coq.ZArith.BinIntDef.Z.mul",2,[0,2,0]],["coq_var","xc",0,[0,2,0,0]],["coq_const","Coq.ZArith.BinIntDef.Z.mul",2,[0,2,0,1,0]],["coq_var","g'",0,[0,2,0,1,0,0]],["coq_var","x",0,[0,2,0,1,0,1]]],"
??
tac(A,"ring",1) :-
    goal_node(coq_ind,A,B,C), goal_node(coq_construct,A,D,E), goal_node(coq_const,A,F,G), goal_above(A,F,D), goal_node(coq_const,A,H,G), goal_above(A,H,F), goal_node(coq_const,A,I,J), similar_goal_terms(A,I,H), goal_node(coq_Init_Logic_eq,A,K,L), goal_above(A,K,H).

## constants in anonymous

use True corresponds to False even if it is uncommon

how to use true false?

* include true and false becasuse very common
* In QArith, true false are useless one inversion, Lists, inversion

how to use andb, orb, negb?

* no andb negb in QArith
* In Lists, andb only works for true && forallb l = true

how to use not?

* must use, very common
