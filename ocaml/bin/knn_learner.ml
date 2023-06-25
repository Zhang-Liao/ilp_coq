open Ocaml

let intersect cmp l1 l2 =
  let rec intersect l1 l2 =
    match l1 with
    | [] -> []
    | h1 :: t1 -> (
        match l2 with
        | [] -> []
        | h2 :: _ when cmp h1 h2 < 0 -> intersect t1 l2
        | h2 :: t2 when cmp h1 h2 > 0 -> intersect l1 t2
        | _ :: t2 -> (
            match intersect t1 t2 with
            | [] -> [ h1 ]
            | h3 :: _ as l when h3 = h1 -> l
            | _ :: _ as l -> h1 :: l))
  in
  intersect l1 l2

let union l1 l2 =
  List.fold_left (fun acc x -> if List.mem x acc then acc else x :: acc) l1 l2

let knn f1 f2 =
  let i = float_of_int @@ List.length @@ intersect compare f1 f2 in
  i
(* let u = float_of_int @@ List.length@@union f1 f2 in
   i /. u *)

module Tactic = struct
  type t = string

  let compare = Stdlib.compare
end

module TacticMap = Map.Make (Tactic)

type db_entry = { obj : string; features : int list }

let add db (features, obj) = { obj; features } :: db

let knn_dist ps db =
  let dist x = (knn ps x.features, x.obj) in
  Utils.fast_map dist db

(* let remove_dups ts =
   let add acc t =
     if List.exists (fun _ -> Int.equal 1000 10000) acc then acc else t :: acc
   in
   List.rev @@ List.fold_left add [] ts *)

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

(* let predict db ps = remove_dups @@ List.rev @@ knn_dist ps db *)
(* let predict db ps = top_k @@ List.rev @@ knn_dist ps db *)
let predict db ps = firstn 20 @@ remove_dups_and_sort @@ List.rev @@ knn_dist ps db
