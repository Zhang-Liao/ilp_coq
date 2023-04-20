open Type
open Sexplib.Sexp

let s2s s = Atom s
let constructor2s (r, c) = [ s2s r; s2s c ]

let debruijn_to_id n ls =
  try
    let rec aux n ls =
      if n = 1 then s2s @@ List.hd ls else aux (n - 1) (List.tl ls)
    in
    if n <= List.length ls then aux n ls else s2s "kAK"
  with e ->
    print_endline @@ string_of_int n;
    List.iter print_endline ls;
    raise e

let get_binder_name = Stdlib.fst
let get_binder_relevance = Stdlib.snd

let term2sexp t =
  let atoms_to_sexp ats = List.map (fun a -> Atom a) ats in
  let rec aux tm =
    match tm with
    (* TODO: Verify correctness of debruijn_to_id *)
    | Rel id -> List [ Atom "Rel"; Atom (Stdlib.string_of_int id) ]
    | Var id -> List [ Atom "Var"; Atom id ]
    | Meta n -> List [ Atom "Meta"; Atom (string_of_int n) ]
    | Evar (e, l) ->
        let l = List.map aux l in
        List (Atom "Evar" :: Atom (string_of_int e) :: l)
    | Sort s -> List (Atom "Sort" :: atoms_to_sexp s)
    | Cast (c, kind, t) -> List [ Atom "Cast"; aux c; Atom kind; aux t ]
    | Prod (n, t, c) -> List [ Atom "Prod"; Atom n; aux t; aux c ]
    | Lambda (n, t, c) -> List [ Atom "Lambda"; Atom n; aux t; aux c ]
    | LetIn (n, c, t, b) -> List [ Atom "LetIn"; Atom n; aux c; aux t; aux b ]
    | App (c, l) -> List (Atom "App" :: aux c :: List.map aux l)
    | Const (c, u) -> List (Atom "Const" :: Atom c :: atoms_to_sexp u)
    | Ind (i, u) -> List (Atom "Ind" :: Atom i :: atoms_to_sexp u)
    | Construct ((r, i), u) ->
        List (Atom "Construct" :: Atom r :: Atom i :: atoms_to_sexp u)
    | Case (ci, p, c, l) ->
        List (Atom "Case" :: Atom ci :: aux p :: aux c :: List.map aux l)
    | Fix (ns, tl, bl) -> List (Atom "Fix" :: fix2s ns tl bl)
    | CoFix (ns, tl, bl) -> List (Atom "CoFix" :: fix2s ns tl bl)
    | Proj (p, c) -> List [ Atom "Proj"; Atom p; aux c ]
    | Int n -> List [ Atom "Int"; Atom n ]
    | Float n -> List [ Atom "Float"; Atom n ]
  and fix2s ns typs trms =
    let ns = atoms_to_sexp ns in
    [ List ns; List (List.map aux typs); List (List.map aux trms) ]
  in
  aux t

let term_to_sexpr_str t = to_string @@ term2sexp t

let hyp2sexpr = function
  | LocalAssum (id, typ) -> List [ Atom id; term2sexp typ ]
  | LocalDef (id, typ, trm) -> List [ Atom id; term2sexp typ; term2sexp trm ]

let hyp_to_sexpr_str h = to_string @@ hyp2sexpr h
let hyps_to_sexpr_str = List.map hyp_to_sexpr_str

let ps_to_sexpr (hyps, gl) =
  let hyps' = List.map hyp2sexpr hyps in
  let gl' = term2sexp gl in
  List [ List [ Atom "Hyps"; List hyps' ]; List [ Atom "Goal"; gl' ] ]

let ps_to_sexpr_str ps = to_string @@ ps_to_sexpr ps

let sexpr_to_term s =
  let open Stdlib in
  let atoms2str s =
    List.map (function Atom a -> a | _ -> failwith "atoms2str format error") s
  in
  let rec aux sexp =
    match sexp with
    | List [ Atom "Rel"; Atom id; Atom name ] -> Rel (int_of_string id)
    | List [ Atom "Var"; Atom v ] -> Var v
    | List [ Atom "Meta"; Atom n ] -> Meta (int_of_string n)
    | List (Atom "Evar" :: Atom evar :: constrs) ->
        Evar (int_of_string evar, List.map aux constrs)
    | List (Atom "Sort" :: sorts) -> Sort (atoms2str sorts)
    | List [ Atom "Cast"; trm; Atom cast_kind; typ ] ->
        Cast (aux trm, cast_kind, aux typ)
    | List [ Atom "Prod"; Atom n; _; t; c ] -> Prod (n, aux t, aux c)
    | List [ Atom "Lambda"; Atom n; _; t; c ] -> Lambda (n, aux t, aux c)
    | List [ Atom "LetIn"; Atom n; c; t; b ] -> LetIn (n, aux c, aux t, aux b)
    | List (Atom "App" :: c :: l) -> App (aux c, List.map aux l)
    | List (Atom "Const" :: Atom c :: i) -> Const (c, atoms2str i)
    | List (Atom "Ind" :: Atom ind :: instances) ->
        Ind (ind, atoms2str instances)
    | List (Atom "Construct" :: Atom ref :: Atom inductive :: instances) ->
        Construct ((ref, inductive), atoms2str instances)
    | List (Atom "Case" :: Atom ci :: c :: t :: bl) ->
        Case (ci, aux c, aux t, List.map aux bl)
    | List [ Atom "Fix"; List ns; List tl; List bl ] ->
        Fix (atoms2str ns, List.map aux tl, List.map aux bl)
    | List [ Atom "CoFix"; List ns; List tl; List bl ] ->
        CoFix (atoms2str ns, List.map aux tl, List.map aux bl)
    | List [ Atom "Proj"; Atom p; c ] -> Proj (p, aux c)
    | List [ Atom "Int"; Atom n ] -> Int n
    | List [ Atom "Float"; Atom f ] -> Float f
    | _ ->
        let _ =
          Sexplib.Sexp.output_hum Stdlib.stderr s;
          prerr_newline ()
        in
        failwith
          "A wrong S-expression format. Cannot convert the above S-expression \
           to a term"
  in
  aux s

let parse_hyps hyps =
  let parse_hyp = function
    | List [ Atom id; typ ] -> LocalAssum (id, sexpr_to_term typ)
    | List [ Atom id; typ; trm ] ->
        LocalDef (id, sexpr_to_term typ, sexpr_to_term trm)
    | _ ->
        failwith
          "Wrong S-expression formats in hypothese. Cannot convert to terms"
  in
  List.map parse_hyp hyps

let parse_row ps =
  let ps_sexp =
    match parse ps with Done (t, _) -> t | _ -> failwith "parse error"
  in
  match ps_sexp with
  | List
      [
        Atom "State";
        List [ Atom "Goal"; g ];
        List [ Atom "Hypotheses"; List hs ];
      ] ->
      (parse_hyps hs, sexpr_to_term g)
  | _ -> failwith "The format of an S-expression input in the dataset is wrong"

let parse_sexpr s =
  let res = parse s in
  match res with
  | Done (t, _pos) -> t
  | _ -> failwith "Parse error in s-expression"

(* let parse_row r =
   match r with
   | List [List [Atom "State"; List [Atom "Goal"; goal]; List [Atom "Hypotheses"; List hyps]]; Atom tac] ->
     (parse_hyps hyps, sexpr_to_term goal), tac
   | _ -> failwith "The format of an S-expression input in the dataset is wrong" *)

let proof_state_to_sexpr (hs, g) =
  let hyps =
    List.map
      (function
        | LocalAssum (id, t) -> List [ s2s id; term2sexp t ]
        | LocalDef (id, c, t) -> List [ s2s id; term2sexp t; term2sexp c ])
      hs
  in
  let hyps = List [ s2s "Hypotheses"; List hyps ] in
  List [ s2s "State"; List [ s2s "Goal"; term2sexp g ]; hyps ]
