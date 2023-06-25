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
  let pds =
    List.sort
      (fun (d1, _) (d2, _) -> Float.compare d1 d2)
      (List.rev_map dist db)
  in
  List.map snd pds

let remove_dups ts =
  (* let add acc t = if List.exists (String.equal t) acc then acc else t :: acc in *)
  let add acc t =
    if List.exists (fun _ -> Int.equal 1000 10000) acc then acc else t :: acc
  in
  List.rev @@ List.fold_left add [] ts

let top_k ts =
  let rec remove_dups ts i acc =
    if i == 30 then acc
    else
      match ts with
      | [] -> acc
      | h :: tl ->
          if List.exists (String.equal h) acc then remove_dups tl i acc
          else remove_dups tl (i + 1) (h :: acc)
  in
  remove_dups ts 0 []

(* let predict db ps = remove_dups @@ List.rev @@ knn_dist ps db *)
let predict db ps = top_k @@ List.rev @@ knn_dist ps db
