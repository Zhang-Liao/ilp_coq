open Ilplib
open Ilp_lib
open Type
(* open Sexpr *)

let sat_not not t =
  match (not, t) with
  | SProd _, Prod _ -> false
  | SApp _, App _ -> false
  | SCase _, Case _ -> false
  | SLambda _, Lambda _ -> false
  | _ -> true

let sat_rfops t t2 =
  let sat op =
    match op with
    | Type ty1 -> false
    | NotNode n -> sat_not n t
    | AddNode _ ->
        prerr_endline
          "sat_rfops should not check AddNode. AddNode can be checked by \
           pattern match automatically.";
        assert false
  in
  List.for_all sat (rfop t2)

let unsat = (false, IntMap.empty)

let rec sat_term tm1 tm2 sbs =
  let open List in
  let match_hole t1 i sbs =
    match IntMap.find_opt i sbs with
    | None -> (true, IntMap.add i t1 sbs)
    | Some t2 -> if eq_term t1 t2 then (true, sbs) else (false, sbs)
  in
  let rec match_term tm1 tm2 sbs =
    match (tm1, tm2) with
    | Rel r1, Rel r2 when r1 == r2 -> (true, sbs)
    | Construct (c1, i1), Construct (c2, i2) when c1 = c2 && i1 = i2 ->
        (true, sbs)
    | Ind (ind1, u1), Ind (ind2, u2) when ind1 = ind2 && u1 = u2 -> (true, sbs)
    | Const (c1, i1), Const (c2, i2) when c1 = c2 && i1 = i2 -> (true, sbs)
    | Var v1, Var v2 when v1 = v2 -> (true, sbs)
    | Int i1, Int i2 when i1 = i2 -> (true, sbs)
    | Float f1, Float f2 when f1 = f2 -> (true, sbs)
    | Sort s1, Sort s2 when s1 = s2 -> (true, sbs)
    | Meta m1, Meta m2 when m1 = m2 -> (true, sbs)
    | Evar (e1, l1), Evar (e2, l2) when e1 = e2 && length l1 == length l2 ->
        lsat l1 l2 sbs
    | Case (_, pb1, b1, l1), Case (_, pb2, b2, l2) when length l1 == length l2
      ->
        lsat (pb1 :: b1 :: l1) (pb2 :: b2 :: l2) sbs
    | Fix (ns1, tl1, bl1), Fix (ns2, tl2, bl2)
      when eq_len [ tl1; bl1 ] [ tl2; bl2 ] ->
        sat_fix (ns1, tl1, bl1) (ns2, tl2, bl2) sbs
    | CoFix (ns1, tl1, bl1), CoFix (ns2, tl2, bl2)
      when eq_len [ tl1; bl1 ] [ tl2; bl2 ] ->
        sat_fix (ns1, tl1, bl1) (ns2, tl2, bl2) sbs
    | Prod (na1, t1, b1), Prod (na2, t2, b2) ->
        let sat, sbs = sat_term t1 t2 sbs in
        if sat then sat_term b1 b2 sbs else unsat
    | Lambda (na1, t1, b1), Lambda (na2, t2, b2) ->
        let sat, sbs = sat_term t1 t2 sbs in
        if sat then sat_term b1 b2 sbs else unsat
    | LetIn (na1, b1, t1, c1), LetIn (na2, b2, t2, c2) ->
        let sat, sbs = sat_term b1 b2 sbs in
        if sat then
          let sat, sbs = sat_term t1 t2 sbs in
          if sat then sat_term c1 c2 sbs else unsat
        else unsat
    | Proj (p1, c1), Proj (p2, c2) when p1 = p2 -> sat_term c1 c2 sbs
    | App (h1, l1), App (h2, l2) when length l1 == length l2 ->
        lsat (h1 :: l1) (h2 :: l2) sbs
    | Cast (b1, k1, t1), Cast (b2, k2, t2) when k1 == k2 ->
        lsat [ b1; t1 ] [ b2; t2 ] sbs
    | _ -> unsat
  and lsat l1 l2 sbs =
    let l = List.combine l1 l2 in
    List.fold_left
      (fun (sat, sbs) (a, b) -> if sat then sat_term a b sbs else unsat)
      (true, sbs) l
  and sat_fix (ns1, tl1, bl1) (ns2, tl2, bl2) sbs =
    let sat, sbs = lsat tl1 tl2 sbs in
    if sat then lsat bl1 bl2 sbs else unsat
  in
  if sat_rfops tm1 tm2 then
    match tm2 with
    | Hole (i, _) -> match_hole tm1 i sbs
    | RTerm (t2, _) -> match_term tm1 t2 sbs
  else unsat

let sat_hyp h1 h2 sbs =
  match (h1, h2) with
  | LocalAssum (id1, t1), LocalAssum (id2, t2) -> sat_term t1 t2 sbs
  | LocalDef (id1, b1, t1), LocalDef (id2, b2, t2) ->
      let sat, sbs = sat_term b1 b2 sbs in
      if sat then sat_term t1 t2 sbs else unsat
  | LocalAssum _, LocalDef _ | LocalDef _, LocalAssum _ -> unsat

let first_sat_hyp r hs sbs =
  let rec aux hs acc =
    match hs with
    | [] -> (None, [])
    | h :: tl ->
        let sat, sbs = sat_hyp h r sbs in
        if sat then (Some (h, sbs), acc @ tl) else aux tl (h :: acc)
  in
  aux hs []

let filter_hyp sbs rule h =
  let sat, sbs = sat_hyp h rule sbs in
  if sat then Some (h, sbs) else None

(* let sat_state (hs1, g1) (hs2, g2)  =
   let rec aux hs1 hs2 sbs =
     match hs2 with
     | [] ->
       let sat, sbs = sat_term g1 g2  sbs in
       if sat then print_endline "sat" else print_endline "unsat";
       pr_state ([], g1);
       pr_rule ([], g2);
       pr_subst sbs;
       sat, sbs
     | h2 :: tl ->
         let sat_h, left_hs1 = first_sat_hyp h2 hs1  sbs in
         if sat_h == None then (
           (* print_endline "Left hyps"; *)
         false, IntMap.empty)
         else
           let sbs1 = snd @@ Option.get sat_h in
           let sat, sbs2 = aux left_hs1 tl sbs1 in
           if sat then (sat, sbs2) else (
           print_endline "back track Left hyps";
           pr_state (left_hs1, g1);
           pr_rule (hs2, g2);
           pr_subst sbs;
           aux left_hs1 hs2 sbs)
   in
   fst @@ aux hs1 hs2 IntMap.empty *)
let sat_state (hs1, g1) (hs2, g2) =
  let rec aux hs1 hs2 sbs =
    match hs2 with
    | [] -> sat_term g1 g2 sbs
    | h2 :: tl ->
        let sat_hs1 = List.filter_map (filter_hyp sbs h2) hs1 in
        List.fold_left
          (fun (sat, sbs) (h1, sbs1) ->
            if sat then (true, sbs)
            else
              let sat1, sbs1 = aux (rm_hyp_from_list hs1 h1) tl sbs1 in
              if sat1 then (true, sbs1) else (false, sbs))
          (false, sbs) sat_hs1
  in
  fst @@ aux hs1 hs2 IntMap.empty

let match_state (hs1, g1) (hs2, g2) =
  let mat = List.map (fun (i, h) -> (i, List.nth hs1 i, h)) hs2 in
  let _, sbs = sat_term g1 g2 IntMap.empty in
  List.fold_left (fun acc (_, h, r) -> snd @@ sat_hyp h r acc) sbs mat

(* TODO: return multiple hole ids which relate to the same term.  *)
let extend t sbs ops =
  let ext sbs t =
    let sbs2 = IntMap.filter (fun _ t1 -> eq_term t t1) sbs in
    if IntMap.is_empty sbs2 then
      let i =
        if IntMap.is_empty sbs then 0 else (fst @@ IntMap.max_binding sbs) + 1
      in
      (IntMap.add i t sbs, Hole (i, []))
    else
      let i, _ = IntMap.choose sbs2 in
      (sbs, Hole (i, []))
  in
  let sbs, t = fold_map ext sbs t in
  let ops =
    List.filter (function AddNode _ -> false | Type _ | NotNode _ -> true) ops
  in
  (sbs, RTerm (t, ops))

let refine t idx ops sbs =
  let refin = function
    | AddNode _ ->
        let sbs, t' = extend t sbs ops in
        (sbs, AddNode t')
    | Type _ -> assert false
    | NotNode (SApp _) -> (sbs, NotNode (SApp (None, None)))
    | NotNode (SCase _) -> (sbs, NotNode (SCase (None, None, None)))
    | NotNode (SLambda _) -> (sbs, NotNode (SLambda (None, None)))
    | NotNode (SProd _) -> (sbs, NotNode (SProd (None, None)))
  in
  let undo op1 =
    let is_do op2 =
      match (op1, op2) with
      | Type _, Type _
      | AddNode _, AddNode _
      | NotNode (SProd _), NotNode (SProd _)
      | NotNode (SLambda _), NotNode (SLambda _)
      | NotNode (SApp _), NotNode (SApp _)
      | NotNode (SCase _), NotNode (SCase _) ->
          true
      | _ -> false
    in
    not @@ List.exists is_do ops
  in
  List.fold_left
    (fun acc op -> if undo op then (idx, refin op) :: acc else acc)
    [] all_rf_kinds

(* TODO: redundance elimination *)
(* TODO: optimize so that only needs to add constraint to a variable *)
(* TODO: try to implement by mapping and compare in pratical. *)
let rec refine_trm tm1 tm2 idx acc sbs =
  let open List in
  let rec deep tm1 tm2 idx acc =
    match (tm1, tm2) with
    | Rel _, Rel _
    | Construct _, Construct _
    | Ind _, Ind _
    | Const _, Const _
    | Var _, Var _
    | Int _, Int _
    | Float _, Float _
    | Sort _, Sort _
    | Meta _, Meta _
    | Evar _, Evar _ ->
        acc
    | Case (ci, pb1, b1, l1), Case (_, pb2, b2, l2) ->
        laux (pb1 :: b1 :: l1) (pb2 :: b2 :: l2) idx (0, acc)
    | Fix (ns1, tl1, bl1), Fix (ns2, tl2, bl2) ->
        aux_fix (ns1, tl1, bl1) (ns2, tl2, bl2) idx acc
    | CoFix (ns1, tl1, bl1), CoFix (ns2, tl2, bl2) ->
        aux_fix (ns1, tl1, bl1) (ns2, tl2, bl2) idx acc
    | Prod (na1, t1, b1), Prod (na2, t2, b2) ->
        let acc = refine_trm t1 t2 (0 :: idx) acc sbs in
        refine_trm b1 b2 (1 :: idx) acc sbs
    | Lambda (na1, t1, b1), Lambda (na2, t2, b2) ->
        let acc = refine_trm t1 t2 (0 :: idx) acc sbs in
        refine_trm b1 b2 (1 :: idx) acc sbs
    | LetIn (na1, b1, t1, c1), LetIn (na2, b2, t2, c2) ->
        let acc = refine_trm b1 b2 (0 :: idx) acc sbs in
        let acc = refine_trm t1 t2 (1 :: idx) acc sbs in
        refine_trm c1 c2 (2 :: idx) acc sbs
    | Proj (p1, c1), Proj (p2, c2) -> refine_trm c1 c2 (0 :: idx) acc sbs
    | App (h1, l1), App (h2, l2) -> laux (h1 :: l1) (h2 :: l2) idx (0, acc)
    | Cast (b1, k1, t1), Cast (b2, k2, t2) ->
        laux [ b1; t1 ] [ b2; t2 ] idx (0, acc)
    | _ -> assert false
  and laux l1 l2 idx acc =
    let l = List.combine l1 l2 in
    let _, acc =
      List.fold_left
        (fun (i, ops) (a, b) -> (i + 1, refine_trm a b (i :: idx) ops sbs))
        acc l
    in
    acc
  and aux_fix (ns1, tl1, bl1) (ns2, tl2, bl2) idx acc =
    let acc = laux tl1 tl2 idx (0, acc) in
    laux bl1 bl2 idx (length tl1, acc)
  in
  match tm2 with
  | RTerm (t2, _) -> deep tm1 t2 idx acc
  | Hole (i, ops) -> List.rev_append acc (refine tm1 idx ops sbs)

let init_h sbs =
  let open IntMap in
  let max = if is_empty sbs then 0 else fst @@ max_binding sbs in
  function
  | LocalAssum (id, t) -> LocalAssum (id, Hole (max + 1, []))
  | LocalDef (id, b, t) -> LocalDef (id, Hole (max + 1, []), Hole (max + 2, []))

let init_hyps sbs hs = List.map (init_h sbs) hs
let refined_h i ids = List.mem i ids
let ith_rhyp i hs = List.find (fun (j, h) -> i == j) hs

let refine_hyps hs1 hs2 acc sbs =
  let refine acc (h1, (i, h2)) =
    match (h1, h2) with
    | LocalAssum (id1, t1), LocalAssum (id2, t2) ->
        refine_trm t1 t2 [ i; 0 ] acc sbs
    | LocalDef (id, b1, t1), LocalDef (id2, b2, t2) ->
        refine_trm b1 b2 [ 0; i; 0 ] acc sbs
        @ refine_trm t1 t2 [ 1; i; 0 ] acc sbs
    | LocalAssum _, LocalDef _ | LocalDef _, LocalAssum _ -> assert false
  in
  let ids = get_rhyp_ids hs2 in
  let hs_rules =
    let aux i h =
      if refined_h i ids then ith_rhyp i hs2 else (i, init_h sbs h)
    in
    List.mapi (fun i h -> (h, aux i h)) hs1
  in
  List.fold_left refine acc hs_rules

let refine_state hs g rule =
  (* let hs = List.combine hs rule.rhyps in *)
  let acc = refine_hyps hs rule.rhyps [] rule.rsubst in
  let acc = refine_trm g rule.rgoal [ 1 ] acc rule.rsubst in
  (* let print (idx, (_, op)) =
       print_endline
       @@ Printf.sprintf "%s %s" (idx_str idx) (sexpr_to_string @@ op2sexp [] op)
     in
     print_endline "refinment operators";
     List.iter print acc; *)
  (* print_newline (); *)
  List.map (fun (idx, (sbs, o)) -> (List.rev idx, sbs, o)) acc

let insert_node op h ops =
  match op with AddNode n -> n | Type _ | NotNode _ -> Hole (h, op :: ops)

let rec insert_op idx tm op =
  let rec deep idx tm =
    let id = List.hd idx in
    let tl_idx = List.tl idx in
    match tm with
    | Rel _ | Construct _ | Ind _ | Const _ | Var _ | Int _ | Float _ | Sort _
    | Meta _ | Evar _ ->
        tm
    | Case (ci, pb, b, l) ->
        if id == 0 then Case (ci, insert_op tl_idx pb op, b, l)
        else if id == 1 then Case (ci, pb, insert_op tl_idx b op, l)
        else Case (ci, pb, b, ins_l l (id - 2) tl_idx op)
    | Prod (na, t, b) ->
        assert (id == 0 || id == 1);
        if id == 0 then Prod (na, insert_op tl_idx t op, b)
        else Prod (na, t, insert_op tl_idx b op)
    | Lambda (na, t, b) ->
        assert (id == 0 || id == 1);
        if id == 0 then Lambda (na, insert_op tl_idx t op, b)
        else Lambda (na, t, insert_op tl_idx b op)
    | LetIn (na, b, t, c) ->
        assert (id == 0 || id == 1 || id == 2);
        if id == 0 then LetIn (na, insert_op tl_idx b op, t, c)
        else if id == 1 then LetIn (na, b, insert_op tl_idx t op, c)
        else LetIn (na, b, t, insert_op tl_idx c op)
    | Proj (p, c) ->
        assert (id == 0);
        Proj (p, insert_op tl_idx c op)
    | Cast (b, k, t) ->
        assert (id == 0 || id == 1);
        if id == 0 then Cast (insert_op tl_idx b op, k, t)
        else Cast (b, k, insert_op tl_idx t op)
    | App (h, l) ->
        if id == 0 then App (insert_op tl_idx h op, l)
        else App (h, ins_l l (id - 1) tl_idx op)
    | Fix (ns, tl, bl) ->
        let len = List.length tl in
        if id < len then Fix (ns, ins_l tl 0 tl_idx op, bl)
        else Fix (ns, tl, ins_l bl (id - len) tl_idx op)
    | CoFix (ns, tl, bl) ->
        let len = List.length tl in
        if id < len then CoFix (ns, ins_l tl 0 tl_idx op, bl)
        else CoFix (ns, tl, ins_l bl (id - len) tl_idx op)
  and ins_l l id idx op =
    List.mapi (fun i t -> if i == id then insert_op idx t op else t) l
  in
  match tm with
  | Hole (h, ops) ->
      assert (idx == []);
      insert_node op h ops
  | RTerm (t, ops) -> RTerm (deep idx t, ops)

(* TODO: fine gained refinement operator. Not directly extending a term in the hypotheses with structures like App. First replace the entire term with a hole. *)
let rm_empty_hyps (hs, g) =
  let not_empty = function
    | Hole (_, []) -> false
    | RTerm _ | Hole (_, _) -> true
  in
  let not_empty_h (_, h) =
    match h with
    | LocalAssum (_, t) -> not_empty t
    | LocalDef (_, b, t) -> not_empty b && not_empty t
  in
  (List.filter not_empty_h hs, g)

let insert_hyps hs1 hs2 op idx sbs =
  let tl_idx = List.tl idx in
  let id = List.hd idx in
  let hs =
    if List.mem id (get_rhyp_ids hs2) then hs2
    else (id, init_h sbs (List.nth hs1 id)) :: hs2
  in
  let insert = function
    | LocalAssum (id, t) -> LocalAssum (id, insert_op tl_idx t op)
    | LocalDef (id, b, t) ->
        let idx = List.hd tl_idx in
        let tl' = List.tl tl_idx in
        assert (idx == 0 || idx == 1);
        if idx == 0 then LocalDef (id, insert_op tl' b op, t)
        else LocalDef (id, b, insert_op tl' t op)
  in
  List.map (fun (i, h) -> (i, if i == id then insert h else h)) hs

let insert_state hs1 hs2 g op idx sbs =
  match idx with
  | 0 :: tl -> rm_empty_hyps (insert_hyps hs1 hs2 op tl sbs, g)
  | 1 :: tl -> (hs2, insert_op tl g op)
  | _ -> assert false

let cover r sts =
  let check (s, acc) (st, i) =
    if sat_state st r then (s +. 1., (st, i) :: acc) else (s, acc)
  in
  List.fold_left check (0., []) sts

let log10_2 = log10 2.
let log2 x = log10 x /. log10_2

(** Foil gain and QuickFOIL gain use the symbol from the paper QuickFOIL. *)
let foil_gain r1 r2 pos1 neg1 =
  let t_plus1, _ = cover r1 pos1 in
  let t_minus1, _ = cover r1 neg1 in
  let t_plus2, pos2 = cover r2 pos1 in
  let t_minus2, neg2 = cover r2 neg1 in
  let entropy2 = t_plus2 /. (t_plus2 +. t_minus2) in
  let entropy1 = t_plus1 /. (t_plus1 +. t_minus1) in
  (* print_endline ("--------Rule1-------\n" ^ sexpr_to_string @@ sexp_of_rstate r1);
     print_endline "Positive";
     List.iter
       (fun (p, _, _) ->
         print_endline @@ sexpr_to_string @@ proof_state_to_sexpr p)
       pos1;
     print_endline "Still Negative";
     List.iter
       (fun (n, _, _) ->
         print_endline @@ sexpr_to_string @@ proof_state_to_sexpr n)
       neg1;
     print_endline ("----Rule2-----\n" ^ sexpr_to_string @@ sexp_of_rstate r2);
     print_endline "Positive";
     List.iter
       (fun (p, _, _) ->
         print_endline @@ sexpr_to_string @@ proof_state_to_sexpr p)
       pos2;
     print_endline "Still Negative";
     List.iter
       (fun (n, _, _) ->
         print_endline @@ sexpr_to_string @@ proof_state_to_sexpr n)
       neg2;
     print_newline (); *)
  (t_plus2 *. (log2 entropy2 -. log2 entropy1), pos2, neg2)

let gen_rules hyps rule ops =
  let remove_dups rs =
    let add acc r =
      if List.exists (fun x -> r = x) acc then acc else r :: acc
    in
    List.fold_left add [] rs
  in
  let gen (idx, sbs, o) =
    let hs, g = insert_state hyps rule.rhyps rule.rgoal o idx sbs in
    { rhyps = hs; rgoal = g; rsubst = sbs }
  in
  remove_dups @@ List.map gen ops

let rec learn_one_rule rule1 st0 pos1 neg1 =
  let hs0, g0 = st0 in
  let hs1, g1 = (rule1.rhyps, rule1.rgoal) in
  let learn rule =
    let sbs = match_state st0 (hs1, g1) in
    let ops = refine_state hs0 g0 { rule with rsubst = sbs } in
    let score rule2 =
      let hs1 = rm_rhyp_ids hs1 in
      let hs2 = rm_rhyp_ids rule2.rhyps in
      let s, pos2, neg2 = foil_gain (hs1, g1) (hs2, rule2.rgoal) pos1 neg1 in
      (s, (rule2, pos2, neg2))
    in
    if ops == [] then [ (0., (rule, pos1, neg1)) ]
    else List.map score (gen_rules hs0 rule ops)
  in
  let sort rs = List.sort (fun (s1, _) (s2, _) -> -Float.compare s1 s2) rs in
  if neg1 == [] then (rule1, pos1)
  else
    (* TODO: return all candidates with the highest gain *)
    let _, (rule2, pos2, neg2) = List.hd @@ sort @@ learn rule1 in
    (* TODO: equal *)
    if eq_rule rule1 rule2 then (rule1, pos1)
    else
      (* let _ =
             Sexpr.sexpr_to_string
             @@ sexp_of_rstate (rm_rhyp_ids rule2.rhyps, rule2.rgoal)
         in *)
      (* print_endline
         ("Best scored Rule\n" ^ Sexpr.sexpr_to_string
         @@ sexp_of_rstate (rm_rhyp_ids rule2.rhyps, rule2.rgoal)); *)
      learn_one_rule rule2 st0 pos2 neg2

(* Only instantiating the substitutions after match_state *)
let init_rule = { rhyps = []; rgoal = Hole (0, []); rsubst = IntMap.empty }
let exg_nth exg = List.mapi (fun i st -> (st, i)) exg

let foil st0 pos neg =
  (* Adding dummy bits for negative examples. Positiion information is merely needed for positive examples. *)
  let neg = exg_nth neg in
  let rec aux pos1 =
    let rule, sat = learn_one_rule init_rule st0 pos1 neg in
    (* TODO: checking termination during refinement.  *)
    (* print_endline "before the satisfactory checking of the current"; *)
    let sat_curr = sat_state st0 (rm_rhyp_ids rule.rhyps, rule.rgoal) in
    if sat_curr then rule
    else
      let pos2 =
        List.fold_left (fun acc (_, i) -> remove_nth acc i) pos1 sat
      in
      let pos2 = List.mapi (fun i (st, _) -> (st, i)) pos2 in
      aux @@ pos2
  in
  aux @@ exg_nth pos
