(* Goal forall P Q (x: Prop), P x -> (P x -> Q x) -> Q x.
Proof.
intro. intro. intro. intro H1. intro H2. apply H2 in H1.
*)

(* Goal forall P Q (x: Prop), P x -> (P x -> Q x) -> Q x.
Proof.
intro. intro. intro. intro H1. intro H2.
auto.
 apply H2 in H1.
*)

Goal forall x y, x + y = y + x.
intros. 