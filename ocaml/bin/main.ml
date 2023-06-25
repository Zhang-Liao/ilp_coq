open Ocaml
open Utils
open Knn_learner

let train_x = ref ""
let train_y = ref ""
let test_x = ref ""
let test_y = ref ""

let speclist =
  [
    ("-train_x", Arg.Set_string train_x, "Training data, features.");
    ("-train_y", Arg.Set_string train_y, "Training data, labels.");
    ("-test_x", Arg.Set_string test_x, "Testing data, features.");
    ("-test_y", Arg.Set_string test_y, "Predictions for testing data.");
  ]

let usage = "Chronology evaluation."

let () =
  Arg.parse speclist (fun x -> raise (Arg.Bad ("Bad argument : " ^ x))) usage

let safe_index l x =
  let rec aux l n =
    match l with
    | [] -> None
    | h :: tl -> if String.equal h x then Some n else aux tl (n + 1)
  in
  aux l 0

let test rows model =
  let aux (ps, tac) =
    let preds = predict model ps in
    let k = safe_index preds tac in
    let k = if k == None then -1 else Option.get k in
    (* let k = -1 in *)
    Printf.sprintf "%i\n" k
    (* string_of_int k *)
  in
  (* fast_map aux rows *)
  let res, _, _ =
    List.fold_left
      (fun (acc, i, t) r ->
        let t' = Unix.time () in
        (* if i mod 100 = 0 then  *)
        Printf.printf "%i %f\n" i (t' -. t);
        flush Stdlib.stdout;
        (aux r :: acc, i + 1, t'))
      ([], 0, Unix.time ())
      rows
  in
  res

let train exgs = List.fold_left (fun model e -> add model e) [] exgs

let eval () =
  let train_feat = load_features !train_x in
  let train_label = load_labels !train_y in
  let train_dat = List.combine train_feat train_label in
  let test_feat = load_features !test_x in
  let test_label = load_labels !test_y in
  let test_dat = List.combine test_feat test_label in
  let db = train train_dat in
  test test_dat db

let _ =
  print_endline ("eval " ^ !test_x);
  let idx = String.rindex !test_x '.' in
  let out = String.sub !test_x 0 idx ^ ".eval" in
  let oc =
    open_out_gen [ Open_trunc; Open_creat; Open_text; Open_append ] 0o640 out
  in
  let res = eval () in
  List.iter (output_string oc) res