let fast_map f l = List.rev@@List.rev_map f l

let read_lines_no_lemma file : string list =
  let ic = open_in file in
  let try_read () =
    try Some (input_line ic) with End_of_file -> None in
  let rec loop acc = match try_read () with
    | Some s ->
      let split_s = String.split_on_char '\t' s in
      if String.equal (List.hd split_s) "#lemma" then loop acc
      else loop (s :: acc)
    | None -> close_in ic; List.rev acc in
  loop []

let load_features file =
  let lines = read_lines_no_lemma file in
  let split = Str.split_delim (Str.regexp " ") in
  let line_to_feats l =
    let f = List.map int_of_string (split@@String.trim l) in
    Base.Set.of_list (module Base.Int) f
  in
  fast_map line_to_feats lines

let load_labels file = read_lines_no_lemma file