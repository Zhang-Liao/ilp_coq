# ILP for Coq

## Encoding

Rel | Evar | Construct | Ind  | Var | Const | Int | Float
| Prod (_, t, b) | Lambda (_, t, b) | Fix (_, (_, tl, bl))
| CoFix (_, (_, tl, bl))
| Case (ci, pb, b, l)
| LetIn (na, b, t, c)
| Proj (p, c)
| Cast (b, k, t)
| App (h, l)
| Sort | Meta

### anonym

ignore: Int (mis include), Float (mis include), Fix, CoFix, Case, LetIn, Proj, Sort, Meta

## origin

ignore: Int (mis include), Float (mis include), Sort, Meta, App
include: the other

Cannot show all the details of encoding because it is complicate, e.g., only one identidier of Constructor ... To explain, first, show the tree structure, then show encoding by position. Some constructors (App,...) are ignored because they have been indicated by their arguments. Appendix pseudocode shows the structure of Coq, which predicates are used, do not need explain the meaning of each argument.
For anonymous,only keep ...
