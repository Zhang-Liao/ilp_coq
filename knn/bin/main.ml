open Stat_ml
open Utils
open Knn_learner

let train_x = ref ""
let train_y = ref ""
let test_x = ref ""

let speclist =
  [
    ("-train_x", Arg.Set_string train_x, "Training data, features.");
    ("-train_y", Arg.Set_string train_y, "Training data, labels.");
    ("-test_x", Arg.Set_string test_x, "Testing data, features.");
  ]

let usage = "Chronology evaluation."

let () =
  Arg.parse speclist (fun x -> raise (Arg.Bad ("Bad argument : " ^ x))) usage

let test rows db =
  let pr_preds preds =
    let preds = List.map snd preds in
    Printf.sprintf "%s\n" (String.concat "\t" preds)
  in
  let split_l = String.split_on_char '\t' in
  let test_one (acc, i, t) r =
    if String.equal (List.hd @@ split_l r) "#lemma" then
      ((r ^ "\n") :: acc, i, t)
    else
      let feat = line_to_feats r in
      let t' =
        if i mod 100 != 0 then t
        else
          let now = Unix.time () in
          Printf.printf "%i %f\n" i (now -. t);
          flush Stdlib.stdout;
          now
      in
      ((pr_preds @@ predict db feat) :: acc, i + 1, t')
  in
  let res, _, _ = List.fold_left test_one ([], 0, Unix.time ()) rows in
  List.rev res

let train exgs =
  let empty = { entries = []; frequencies = Frequencies.empty } in
  List.fold_left (fun model e -> add model e) empty exgs

let eval () =
  let train_feat = load_features !train_x in
  let train_label = load_labels !train_y in
  let train_dat = List.combine train_feat train_label in
  let db = train train_dat in
  test (read_lines !test_x) db

let _ =
  print_endline ("eval " ^ !test_x);
  let idx = String.rindex !test_x '.' in
  let out = String.sub !test_x 0 idx ^ ".eval" in
  let oc =
    open_out_gen [ Open_trunc; Open_creat; Open_text; Open_append ] 0o640 out
  in
  let res = eval () in
  List.iter (output_string oc) res
