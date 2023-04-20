open Type
open Sexplib.Sexp

(* open Util *)
open Sexpr
(* open Tactic_learner *)

(** Data structure *)
let eq_term = Stdlib.( = )

let eq_rtrem t1 t2 =
  match (t1, t2) with
  | Hole (h1, o1), Hole (h2, o2) when List.length o1 = List.length o2 ->
      Int.equal h1 h2 && List.for_all2 Stdlib.( = ) o1 o2
  | _, _ -> false

let rm_rhyp_ids h = List.map snd h
let get_rhyp_ids h = List.map fst h
let rm_rule_ids (h, g) = (rm_rhyp_ids h, g)
let rmv_subst r = (r.rhyps, r.rgoal)

(* TODO: equal for list *)
let eq_rule r1 r2 =
  let e1 = r1.rhyps == r2.rhyps && r1.rgoal == r2.rgoal in
  e1 && IntMap.equal Stdlib.( = ) r1.rsubst r2.rsubst

let all_rf_kinds =
  [
    (* Type None; *)
    AddNode (Hole (0, []))
    (* NotNode (SProd (None, None));
       NotNode (SLambda (None, None));
       NotNode (SApp (None, None));
       NotNode (SCase (None, None, None)); *);
  ]

module RefineOperator = struct
  type t = refine_op

  (* TODO: better comparing function *)
  let compare = Stdlib.compare
end

module RefineOperatorSet = Set.Make (RefineOperator)

let rftm = function RTerm (t, _) -> t | Hole _ -> assert false
let rfop = function RTerm (_, o) | Hole (_, o) -> o

(** General. *)

let eq_len l1 l2 =
  let open List in
  for_all2 (fun a b -> length a == length b) l1 l2

let list_remove eq l i =
  let rec aux l acc =
    match l with
    | [] -> raise Not_found
    | hd :: tl -> if eq i hd then List.rev_append tl acc else aux tl (hd :: acc)
  in
  List.rev @@ aux l []

let list_removes eq l origin = List.fold_left (list_remove eq) origin l

let equal_hyp eq decl1 decl2 =
  match (decl1, decl2) with
  | LocalAssum (id1, ty1), LocalAssum (id2, ty2) -> id1 = id2 && ty1 = ty2
  | LocalDef (id1, v1, ty1), LocalDef (id2, v2, ty2) ->
      id1 = id2 && v1 = v2 && ty1 = ty2
  | _ -> false

let rm_hyp_from_list hs h = list_remove (equal_hyp Stdlib.( = )) hs h

let remove_nth l i =
  let rec aux l i' acc =
    match l with
    | [] -> raise Not_found
    | hd :: tl ->
        if Int.equal i i' then List.rev_append tl acc
        else aux tl (i' + 1) (hd :: acc)
  in
  List.rev @@ aux l 0 []

(** Circular queue. *)

module CircularQueue : sig
  type 'a t

  val empty : int -> 'a t
  val add : 'a -> 'a t -> 'a option * 'a t
  val to_list_map : ('a -> 'b) -> 'a t -> 'b list
  val size : 'a t -> int
  val max : 'a t -> int
end = struct
  type 'a t = { max : int; size : int; incoming : 'a list; outgoing : 'a list }

  let empty max = { size = 0; max; incoming = []; outgoing = [] }
  let head_tail ls = (List.hd ls, List.tl ls)

  let add x { max; size; incoming; outgoing } =
    if size < max then (
      assert (outgoing = []);
      (None, { max; size = size + 1; incoming = x :: incoming; outgoing }))
    else (
      assert (size = max);
      match outgoing with
      | [] ->
          let out, outgoing = head_tail @@ List.rev (x :: incoming) in
          (Some out, { max; size; incoming = []; outgoing })
      | out :: outgoing ->
          (Some out, { max; size; incoming = x :: incoming; outgoing }))

  let to_list_map f { incoming; outgoing; _ } =
    let tail = List.fold_right (fun x -> List.cons (f x)) outgoing [] in
    List.fold_left (fun ls x -> List.cons (f x) ls) tail incoming

  let size { size; _ } = size
  let max { max; _ } = max
end

(* --------------------------------------------------------- *)
(* Map and Fold *)
let map_term f = function
  | Rel r -> Rel r
  | Evar (e, l) -> Evar (e, List.map f l)
  | Construct (c, u) -> Construct (c, u)
  | Ind (ind, u) -> Ind (ind, u)
  | Var v -> Var v
  | Const (c, u) -> Const (c, u)
  | Int i -> Int i
  | Float fl -> Float fl
  | Sort s -> Sort s
  | Meta m -> Meta m
  | Cast (c, k, t) -> Cast (f c, k, f t)
  | Prod (na, t, c) -> Prod (na, f t, f c)
  | App (c, l) -> App (f c, List.map f l)
  | Proj (p, c) -> Proj (p, f c)
  | Fix (lna, tl, bl) -> Fix (lna, List.map f tl, List.map f bl)
  | CoFix (lna, tl, bl) -> CoFix (lna, List.map f tl, List.map f bl)
  | Lambda (n, t, c) -> Lambda (n, f t, f c)
  | LetIn (n, b, t, c) -> LetIn (n, f b, f t, f c)
  | Case (ci, p, c, bl) -> Case (ci, f p, f c, List.map f bl)

let fold_map f acc c =
  match c with
  | Rel r -> (acc, Rel r)
  | Meta i -> (acc, Meta i)
  | Var v -> (acc, Var v)
  | Sort s -> (acc, Sort s)
  | Const (c, i) -> (acc, Const (c, i))
  | Ind (ind, u) -> (acc, Ind (ind, u))
  | Construct (c, u) -> (acc, Construct (c, u))
  | Int i -> (acc, Int i)
  | Float f -> (acc, Float f)
  | Cast (b, k, t) ->
      let acc, b' = f acc b in
      let acc, t' = f acc t in
      (acc, Cast (b', k, t'))
  | Prod (na, t, b) ->
      let acc, b' = f acc b in
      let acc, t' = f acc t in
      (acc, Prod (na, t', b'))
  | Lambda (na, t, b) ->
      let acc, b' = f acc b in
      let acc, t' = f acc t in
      (acc, Lambda (na, t', b'))
  | LetIn (na, b, t, k) ->
      let acc, b' = f acc b in
      let acc, t' = f acc t in
      let acc, k' = f acc k in
      (acc, LetIn (na, b', t', k'))
  | App (b, l) ->
      let acc, b' = f acc b in
      let acc, l' = List.fold_left_map f acc l in
      (acc, App (b', l'))
  | Proj (p, t) ->
      let acc, t' = f acc t in
      (acc, Proj (p, t'))
  | Evar (e, l) ->
      let acc, l' = List.fold_left_map f acc l in
      (acc, Evar (e, l'))
  | Case (ci, p, b, bl) ->
      let acc, b' = f acc b in
      let acc, p' = f acc p in
      let acc, bl' = List.fold_left_map f acc bl in
      (acc, Case (ci, p', b', bl'))
  | Fix (lna, tl, bl) ->
      let acc, tl' = List.fold_left_map f acc tl in
      let acc, bl' = List.fold_left_map f acc bl in
      (acc, Fix (lna, tl', bl'))
  | CoFix (lna, tl, bl) ->
      let acc, tl' = List.fold_left_map f acc tl in
      let acc, bl' = List.fold_left_map f acc bl in
      (acc, CoFix (lna, tl', bl'))

(* --------------------------------------------------------- *)
(* Equality *)
(* let eq_hyp = Context.Named.Declaration.equal equal *)

let eq_hyp_no_id eq h1 h2 =
  match (h1, h2) with
  | LocalAssum (_, ty1), LocalAssum (_, ty2) -> eq ty1 ty2
  | LocalDef (_, v1, ty1), LocalDef (_, v2, ty2) -> eq v1 v2 && eq ty1 ty2
  | LocalAssum _, LocalDef _ | LocalDef _, LocalAssum _ -> false

let eq_hyps_no_id hs1 hs2 eq =
  let eq_hyp = eq_hyp_no_id eq in
  let rec aux hs1 hs2 =
    match hs1 with
    | [] -> if hs2 == [] then true else false
    | h1 :: tl ->
        let h2 = List.find_opt (eq_hyp_no_id eq h1) hs2 in
        if h2 == None then false
        else aux tl (list_remove eq_hyp hs2 (Option.get h2))
  in
  aux hs1 hs2

let eq_state (hs1, g1) (hs2, g2) eq = eq_hyps_no_id hs1 hs2 eq && eq g1 g2

(* TODO: not only comare rel and named contexts? *)

(* TODO: alpha-conversion
   kind_nocast ???
   CArray.equal_norefl ?? equal ??
*)

(** Treat different universes as the same.  *)
let eq_rterm eq t1 t2 =
  let eq_term t1 t2 =
    match (t1, t2) with
    | Cast (c1, k1, t1), Cast (c2, k2, t2) -> eq c1 c2 && eq t1 t2
    | Rel n1, Rel n2 -> Int.equal n1 n2
    | Meta m1, Meta m2 -> Int.equal m1 m2
    | Var id1, Var id2 -> id1 = id2
    | Int i1, Int i2 -> i1 = i2
    | Float f1, Float f2 -> f1 = f2
    | Sort s1, Sort s2 -> s1 = s2
    | Prod (_, t1, c1), Prod (_, t2, c2) -> eq t1 t2 && eq c1 c2
    | Lambda (_, t1, c1), Lambda (_, t2, c2) -> eq t1 t2 && eq c1 c2
    | LetIn (_, b1, t1, c1), LetIn (_, b2, t2, c2) ->
        eq b1 b2 && eq t1 t2 && eq c1 c2
    | App (c1, l1), App (c2, l2) ->
        let len = List.length l1 in
        Int.equal len (List.length l2) && eq c1 c2 && List.for_all2 eq l1 l2
    | Proj (p1, c1), Proj (p2, c2) -> p1 = p2 && eq c1 c2
    | Evar (e1, l1), Evar (e2, l2) -> e1 = e2 && List.for_all2 eq l1 l2
    | Const (c1, u1), Const (c2, u2) -> c1 = c2
    | Ind (c1, u1), Ind (c2, u2) -> c1 = c2
    | Construct (c1, u1), Construct (c2, u2) -> c1 = c2
    | Case (_, p1, c1, bl1), Case (_, p2, c2, bl2) ->
        eq p1 p2 && eq c1 c2 && List.for_all2 eq bl1 bl2
    | Fix (_, tl1, bl1), Fix (_, tl2, bl2) ->
        List.for_all2 eq tl1 tl2 && List.for_all2 eq bl1 bl2
    | CoFix (_, tl1, bl1), CoFix (_, tl2, bl2) ->
        List.for_all2 eq tl1 tl2 && List.for_all2 eq bl1 bl2
    | _ -> false
  in
  let open RefineOperatorSet in
  match (t1, t2) with
  | RTerm (t1, o1), RTerm (t2, o2) ->
      equal (of_list o1) (of_list o2) && eq_term t1 t2
  | Hole (_, o1), Hole (_, o2) -> equal (of_list o1) (of_list o2)
  | RTerm _, Hole _ | Hole _, RTerm _ -> false

let rec equal_rterm t1 t2 = eq_rterm equal_rterm t1 t2

let eq_rstate (hs1, g1) (hs2, g2) =
  eq_hyps_no_id hs1 hs2 equal_rterm && equal_rterm g1 g2

(* --------------------------------------------------------- *)

(** Sexpr. *)

let not2str = function
  | SProd _ -> "NotProd"
  | SLambda _ -> "NotLambda"
  | SApp _ -> "NotApp"
  | SCase _ -> "NotCase"

let constr_opt_to_str ns = function None -> s2s "None" | Some t -> term2sexp t

let op2sexp ns = function
  | Type t -> List [ s2s "Type"; constr_opt_to_str ns t ]
  (* | HNF *)
  | NotNode n -> s2s @@ not2str n
  | AddNode _ -> List [ s2s "AddNode" ]

let ops2sexp ns os = List (s2s "Refine" :: List.map (op2sexp ns) os)

let rec rterm2s ls =
  let rec aux ls tm =
    match tm with
    | Rel n -> List [ s2s "Rel"; s2s (string_of_int n); debruijn_to_id n ls ]
    | Var id -> List [ s2s "Var"; s2s id ]
    | Meta n -> List [ s2s "Meta"; s2s (string_of_int n) ]
    | Evar (e, l) ->
        let l = List.map (rterm2s ls) l in
        List (s2s "Evar" :: s2s (string_of_int e) :: l)
    | Sort s -> List (s2s "Sort" :: List.map s2s s)
    | Cast (t', k, typ) ->
        List [ s2s "Cast"; rterm2s ls t'; s2s k; rterm2s ls typ ]
    | Prod (n, t, c) ->
        let c = rterm2s (n :: ls) c in
        List [ s2s "Prod _"; rterm2s ls t; c ]
    | Lambda (n, t, c) ->
        let c = rterm2s (n :: ls) c in
        List [ s2s "Lambda _"; rterm2s ls t; c ]
    | LetIn (n, c, t, b) ->
        let b = rterm2s (n :: ls) b in
        List [ s2s "LetIn _"; rterm2s ls c; rterm2s ls t; b ]
    | App (h, l) ->
        let l = List.map (rterm2s ls) l in
        List (s2s "App" :: rterm2s ls h :: l)
    | Const (c, u) -> List (s2s "Const" :: s2s c :: List.map s2s u)
    | Ind (i, u) -> List (s2s "Ind" :: s2s i :: List.map s2s u)
    | Construct (c, u) ->
        List ((s2s "Construct" :: constructor2s c) @ List.map s2s u)
    | Case (ci, c, t, bl) ->
        let bl = List.map (rterm2s ls) bl in
        List (s2s "Case" :: s2s ci :: rterm2s ls c :: rterm2s ls t :: bl)
    | Fix (ns, tl, bl) -> List (s2s "Fix" :: prec_declaration2s ls (ns, tl, bl))
    | CoFix (ns, tl, bl) ->
        List (s2s "CoFix" :: prec_declaration2s ls (ns, tl, bl))
    | Proj (p, t) ->
        (* let p = constant2s (Names.Projection.constant p) in *)
        List [ s2s "Proj"; s2s p; rterm2s ls t ]
    | Int n -> List [ s2s "Int"; s2s n ]
    | Float n -> List [ s2s "Float"; s2s n ]
  and prec_declaration2s ls (ns, tl, bl) =
    let tl = List (List.map (rterm2s ls) tl) in
    let bl = List (List.map (rterm2s (ns @ ls)) bl) in
    [ List (List.map s2s ns); tl; bl ]
  in
  function
  | Hole (h, os) ->
      if os == [] then List [ s2s "Hole"; s2s @@ string_of_int h ]
      else List [ s2s "Hole"; s2s @@ string_of_int h; ops2sexp ls os ]
  | RTerm (t, os) ->
      if os == [] then aux ls t else List [ aux ls t; ops2sexp ls os ]

let hyp_to_sexpr to_sexpr = function
  | LocalAssum (id, t) -> List [ s2s "_"; to_sexpr t ]
  | LocalDef (id, c, t) -> List (s2s "_" :: to_sexpr c :: [ to_sexpr t ])

let hyps_sexpr hyps to_sexpr =
  List (s2s "Hyps" :: List.map (hyp_to_sexpr to_sexpr) hyps)

let sexp_of_rhyps h = hyps_sexpr h (rterm2s [])

let sexp_of_rstate (hs, g) =
  List [ sexp_of_rhyps hs; List [ s2s "Goal"; rterm2s [] g ] ]

(* --------------------------------------------------------- *)

(** Print *)
let pr_subst sbs =
  IntMap.iter
    (fun i s ->
      print_endline (string_of_int i ^ " " ^ to_string_hum @@ term2sexp s))
    sbs

let pr_rule r = print_endline @@ to_string_hum @@ sexp_of_rstate r

let pr_rule_subst rule =
  print_endline "-------------Rule-------";
  pr_rule (rm_rhyp_ids rule.rhyps, rule.rgoal);
  print_endline "-------------Subst------";
  pr_subst rule.rsubst

let pr_state s = print_endline @@ to_string_hum @@ proof_state_to_sexpr s
let idx_str i = String.concat " " (List.map string_of_int (List.rev i))

let pr_refine_op (idx, (_, op)) =
  Printf.sprintf "%s %s" (idx_str idx) (to_string_hum @@ op2sexp [] op)

(* ------------------------ *)
(* Context *)
let push_rel1 n t ev = LocalAssum (n, t) :: ev
let push_rel2 n c t ev = LocalDef (n, c, t) :: ev

(* -------------------------- *)
(* let safe_index0 f x l = try Some (CList.index0 f x l) with Not_found -> None *)

let safe_index l x =
  let rec aux l n =
    match l with
    | [] -> None
    | h :: tl -> if h = x then Some n else aux tl (n + 1)
  in
  aux l 0
