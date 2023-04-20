open Ilplib
open Ilp_lib
open Type
open Ilp_refine

module Tactic = struct
  type t = string

  let compare = Stdlib.compare
end

module TacticMap = Map.Make (Tactic)

type db_entry = { state : proof_state; obj : string }
type prediction = { tactic : string; keep : bool }

let find_exgs tac db pn nn =
  let add_pos i st pos = if i >= pn then (i, pos) else (i + 1, st :: pos) in
  let add_neg i st neg = if i >= nn then (i, neg) else (i + 1, st :: neg) in
  let rec aux ents pi ni (pos, neg) =
    match ents with
    | _ when pi >= pn && ni >= nn -> (pos, neg)
    | ent :: tl ->
        let st = ent.state in
        if tac = ent.obj then
          let pi, pos = add_pos pi st pos in
          aux tl pi ni (pos, neg)
        else
          let ni, neg = add_neg ni st neg in
          aux tl pi ni (pos, neg)
    | [] -> (pos, neg)
  in
  let db = CircularQueue.to_list_map (fun x -> x) db in
  (* print_endline "=======Database state===========";
     List.iter
       (fun e ->
         print_endline @@ sexpr_to_string @@ LH.proof_state_to_sexpr e.state)
       db; *)
  aux db 0 0 ([], [])

let new_rule pos neg tac ps tac_rules feat =
  let r = rm_rule_ids @@ rmv_subst @@ foil ps pos neg in
  (* TODO: replace 0 with the indexes of the examples that satisfied by the rule in the database. *)
  (* print_endline "Current";
     pr_state @@ proof_state_repr ps;
     print_endline "Positive";
     List.iter (fun (p, _, _) -> pr_state p) pos;
     print_endline "Negative";
     List.iter (fun (n, _, _) -> pr_state n) neg;
     print_endline ("Label " ^ pr_tac @@ tactic_repr tac); *)
  (* print_endline ("Rule" ^ sexpr_to_string @@ sexp_of_rstate r); *)
  (* print_newline (); *)
  TacticMap.update tac
    (function
      | None -> Some ([ r ], [ 0 ]) | Some (rs, idx) -> Some (r :: rs, 0 :: idx))
    tac_rules

let add (db, tac_rules) tac state feat =
  (* (db, tac_rules) *)
  let in_db = { state; obj = tac } in
  let pos, neg = find_exgs tac db 4 8 in
  let rules = TacticMap.find_opt tac tac_rules in
  let sat_curr r = sat_state state r in
  let reject_all r =
    let left = List.filter (fun s -> sat_state s r) neg in
    if left == [] then Some r else None
  in
  let db' = snd @@ CircularQueue.add in_db db in
  let tac_rules' =
    if rules == None then new_rule pos neg tac state tac_rules feat
    else
      let rules, _ = Option.get rules in
      (* let rules = List.map rm_rule_ids rules in *)
      let rules = List.filter sat_curr rules in
      let rule_negs = List.filter_map reject_all rules in
      if rule_negs == [] then tac_rules
      else new_rule pos neg tac state tac_rules feat
  in
  (db', tac_rules')

let file_dist _ db = CircularQueue.to_list_map (fun x -> x.obj) db

let remove_dups ts =
  let add acc t = if List.exists (Stdlib.( = ) t) acc then acc else t :: acc in
  List.rev @@ List.fold_left add [] ts

let filter tac_rules st preds =
  let sat tac =
    let rules = TacticMap.find_opt tac tac_rules in
    if rules == None then false
    else
      let rules, _ = Option.get rules in
      List.exists (sat_state st) rules
  in
  let filter_l preds =
    List.map (fun p -> (p, sat p)) preds
    (* List.filter_map (fun t -> if sat t then Some (t, true) else None) *)
  in
  filter_l preds

let predict (db, tac_rules) ps =
  let pred ps =
    let pds = remove_dups @@ List.rev @@ file_dist ps db in
    let out = filter tac_rules ps pds in
    List.map (fun (t, keep) -> { tactic = t; keep }) out
  in
  pred ps