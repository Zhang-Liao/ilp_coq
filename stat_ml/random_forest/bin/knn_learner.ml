(* open Ocaml *)
(* open Base.Set *)

let knn f1 f2 =
  let open Base.Set in
  let inter = float_of_int @@ length @@ inter f1 f2 in
  let union = float_of_int @@ length @@ union f1 f2 in
  inter /. union

module Tactic = struct
  type t = string

  let compare = Stdlib.compare
end

module TacticMap = Map.Make (Tactic)
module IntSet = Base.Set.M(Base.Int)

type db_entry = { obj : string; features : IntSet.t }

let add db (features, obj) = { obj; features } :: db

let knn_dist ps db =
  let dist x = (knn ps x.features, x.obj) in
  List.map dist db

let firstn n l =
  let rec aux acc n l =
    match (n, l) with
    | 0, _ -> List.rev acc
    | n, h :: t -> aux (h :: acc) (pred n) t
    | _ -> List.rev acc
  in
  aux [] n l

module StrMap = Map.Make (String)

let remove_dups_and_sort ranking =
  let ranking_map =
    List.fold_left
      (fun map (score, tac) ->
        StrMap.update tac
          (function
            | None -> Some (score, tac)
            | Some (lscore, ltac) ->
                if score > lscore then Some (score, tac) else Some (lscore, ltac))
          map)
      StrMap.empty ranking
  in
  let new_ranking =
    List.map
      (fun (_hash, (score, tac)) -> (score, tac))
      (StrMap.bindings ranking_map)
  in
  List.sort (fun (x, _) (y, _) -> Float.compare y x) new_ranking

let predict db ps = firstn 20 @@ remove_dups_and_sort @@ knn_dist ps db
