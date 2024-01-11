let fast_map f l = List.rev @@ List.rev_map f l

let line_to_feats l =
  let split = String.split_on_char ' ' in
  List.map int_of_string (split @@ String.trim l)

let read_lines_aux func file : string list =
  let ic = open_in file in
  let try_read () = try Some (input_line ic) with End_of_file -> None in
  let rec loop acc =
    match try_read () with
    | Some s -> loop @@ func s acc
    | None ->
        close_in ic;
        List.rev acc
  in
  loop []

let read_lines file = read_lines_aux List.cons file

let read_lines_no_lemma file : string list =
  let aux s acc =
    let split_s = String.split_on_char '\t' s in
    if String.equal (List.hd split_s) "#lemma" then acc else s :: acc
  in
  read_lines_aux aux file

let load_features file =
  let lines = read_lines_no_lemma file in
  fast_map line_to_feats lines

let load_labels file = read_lines_no_lemma file
