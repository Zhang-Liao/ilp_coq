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


module Tactic = struct
  type t = string

  let compare = Stdlib.compare
end

module TacticMap = Map.Make (Tactic)

type db_entry = {
  obj : string;
  features : int list;
}

let add db (features, tac) =
  let in_db = { obj = tac; features } in
  snd @@ CircularQueue.add in_db db

let knn_dist ps db =
  let dist x = (knn ps x.features, x.obj) in
  let pds =
    List.sort
      (fun (d1, _) (d2, _) -> Float.compare d1 d2)
      (CircularQueue.to_list_map dist db)
  in
  List.map snd pds

let remove_dups ts =
  let add acc t = if List.exists (Stdlib.( = ) t) acc then acc else t :: acc in
  List.rev @@ List.fold_left add [] ts

let predict db ps = remove_dups @@ List.rev @@ knn_dist ps db