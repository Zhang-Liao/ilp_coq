open Ilplib
open Ilp_lib
open Ilp_learner
open Sexpr

let eval_file = ref ""
let speclist = [ ("-file", Arg.Set_string eval_file, "file to evaluate") ]
let usage = "Chronology evaluation."

let () =
  Arg.parse speclist (fun x -> raise (Arg.Bad ("Bad argument : " ^ x))) usage

let test rows model =
  let aux (ps, tac) =
    let preds = predict model ps in
    let preds =
      List.filter_map (fun p -> if p.keep then Some p.tactic else None) preds
    in
    (* let top1 = if List.length preds > 0 then List.hd preds else "None" in *)
    (* print_endline top1; *)
    let k = safe_index preds tac in
    if k == None then -1 else Option.get k
    (* string_of_int k *)
  in
  List.map aux rows

let train model rows lema = List.fold_left (fun m (p, t) -> add m t p lema) model rows

let read_lines file =
  let ic = open_in file in
  let try_read () = try Some (input_line ic) with End_of_file -> None in
  let rec loop acc =
    match try_read () with
    | Some s ->
        let s = String.split_on_char '\t' s in
        (* if String.equal (List.hd split_s) "#lemma" then loop acc *)
        loop ((List.hd s, List.nth s 1) :: acc)
    | None ->
        close_in ic;
        List.rev acc
  in
  loop []

let eval file =
  let model = (CircularQueue.empty 1000, TacticMap.empty) in
  let rows = read_lines file in
  let eval_row (model, dat, res, lema) (ps, tac) =
    if ps = "#lemma" then
      let _ =
        if lema != None then print_endline ("eval lemma " ^ Option.get lema)
      in
      let dat = List.rev dat in
      (* let _ = test dat model in *)
      let res = res @ test dat model in
      let model = train model dat lema in
      (model, [], res, Some tac)
    else
      let ps = parse_row ps in
      (* print_endline tac; *)
      (* let model = add model tac ps in *)
      (model, (ps, tac) :: dat, res, lema)
  in
  List.fold_left eval_row (model, [], [], None) rows

let _ =
  print_endline ("eval " ^ !eval_file);
  let out = !eval_file ^ ".eval" in
  let oc =
    open_out_gen [ Open_trunc; Open_creat; Open_text; Open_append ] 0o640 out
  in
  let _, _, res, _ = eval !eval_file in
  List.iter (fun k -> output_string oc (string_of_int k ^ "\n")) res
