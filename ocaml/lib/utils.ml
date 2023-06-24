let fast_map f l = List.rev@@List.rev_map f l

let read_lines file : string list =
  let ic = open_in file in
  let try_read () =
    try Some (input_line ic) with End_of_file -> None in
  let rec loop acc = match try_read () with
    | Some s -> loop (s :: acc)
    | None -> close_in ic; List.rev acc in
  loop []

let load_features file =
  let lines = read_lines file in
  let split = Str.split_delim (Str.regexp " ") in
  let line_to_feats l =
    List.map int_of_string (split@@String.trim l) in
  fast_map line_to_feats lines

let load_labels file = read_lines file