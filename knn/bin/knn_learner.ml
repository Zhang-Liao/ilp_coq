module FeatureOrd = struct
  type t = int

  let compare = Int.compare
end

module Frequencies = Map.Make (FeatureOrd)

type db_entry = { features : int list; obj : string }
type database = { entries : db_entry list; frequencies : int Frequencies.t }

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

let option_default a = function Some y -> y | _ -> a

let tfidf size freqs ls1 ls2 =
  let inter = intersect compare ls1 ls2 in
  List.fold_left ( +. ) 0.
    (List.map
       (fun f ->
         Float.log
           (Float.of_int (1 + size)
           /. Float.of_int (1 + option_default 0 (Frequencies.find_opt f freqs))
           ))
       inter)

let add { entries; frequencies } (features, obj) =
  let frequencies =
    List.fold_left
      (fun freq f ->
        Frequencies.update f (fun y -> Some (option_default 0 y + 1)) freq)
      frequencies features
  in
  let entries = { features; obj } :: entries in
  { entries; frequencies }

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

let predict { entries; frequencies } feats =
  let length = List.length entries in
  let tdidfs =
    List.map
      (fun ent ->
        let x = tfidf length frequencies feats ent.features in
        (x, ent.obj))
      entries
  in
  firstn 50 @@ remove_dups_and_sort tdidfs
