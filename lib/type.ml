module FeatSet = Set.Make(String)
module HoleFeat = Map.Make(Int)

type 'term term =
(* leafs *)
| Rel       of int
| Evar      of int * 'term  list
| Construct of (string * string) * string list
| Ind       of string * string list
| Var       of string
| Const     of string * string list
| Int       of string
| Float     of string
| Sort      of string list
| Meta      of int
(* non-leafs *)
| Cast      of 'term  * string * 'term
| Prod      of string * 'term  * 'term
| Lambda    of string * 'term  * 'term
| LetIn     of string * 'term  * 'term  * 'term
| App       of 'term * 'term list
| Case      of string * 'term * 'term * 'term list
| Fix       of string list * 'term list * 'term list
| CoFix     of string list * 'term list * 'term list
| Proj      of string * 'term

type constr = constr term

type 'term hyp =
(* id * type *)
| LocalAssum of string * 'term
(* id * term * type *)
| LocalDef of string * 'term * 'term

type proof_state = constr hyp list * constr

type term_struct =
  | SProd of constr option * constr option
  | SLambda of constr option * constr option
  | SApp of constr option * constr array option
  | SCase of constr option * constr option * constr array option

type refine_op =
  (* None means we fail to calaulate the type  *)
  | Type of constr option
  (* | HNF *)
  | AddNode of rterm
  | NotNode of term_struct

and rterm =
  | RTerm of (rterm term * refine_op list)
  | Hole of (int * refine_op list)

module IntMap = Map.Make (Int)

type rule_with_subst = {
    (* The id of the hypotheses in the current example to learn *)
    rhyps : (int * rterm hyp) list;
    rgoal : rterm;
    rsubst : constr IntMap.t;
  }