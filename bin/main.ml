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
    let top1 = if List.length preds > 0 then List.hd preds else "None" in
    let k = safe_index preds top1 in
    let k = if k == None then -1 else Option.get k in
    print_endline top1;
    print_endline@@string_of_int k
  in
  List.map aux rows

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
  List.fold_left
    (fun (model, dat) (ps, tac) ->
      if ps = "#lemma" then
        let _ = test dat model in
        (model, [])
      else
        let ps = parse_row ps in
        (* print_endline tac; *)
        let model = add model tac ps model in
        (model, (ps, tac) :: dat))
    (model, []) rows

let _ = eval !eval_file
