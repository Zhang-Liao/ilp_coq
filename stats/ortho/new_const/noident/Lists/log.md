# Log

kind     anonym_rel_Lists
f1               0.423792
param                p2n8
prec                   20
Name: 17, dtype: object
kind     anonym_prop_Lists
f1                0.380116
param                 p2n1
prec                    20
Name: 152, dtype: object


## anonym rel bag rules

### init

simpl
"1": {"TP": 0, "FP": 29, "FN": 40, "TN": 527, "precision": 0.0}, 
tac(A,"simpl",1) :-
    goal_node(coq_Init_Logic_eq,A,B,C),is_goal_root(A,B),goal_node(coq_var,A,D,E),goal_node(coq_var,A,F,E),dif(F,D),goal_node(coq_var,A,G,H),goal_position_left(G,D),goal_node(coq_construct,A,I,J),goal_above(A,I,D),!.


"4": {"TP": 2, "FP": 513, "FN": 38, "TN": 43, "precision": 0.0038835}
tac(A,"simpl",4) :-
    goal_node(coq_const,A,B,C),goal_node(coq_const,A,D,E),goal_above(A,D,B),goal_node(coq_construct,A,F,G),goal_above(A,B,F),!.

### vectors

auto
"24": {"TP": 11, "FP": 102, "FN": 29, "TN": 134, "precision": 0.0973451},
tac(A,"auto",24) :-
    hyp_node(coq_Init_Logic_eq,A,B,C,D),goal_node(coq_Init_Logic_eq,A,E,D),!.

simpl
"1": {"TP": 8, "FP": 32, "FN": 17, "TN": 63, "precision": 0.2}
simpl
"3": {"TP": 0, "FP": 10, "FN": 25, "TN": 85, "precision": 0.0},
tac(A,"simpl",3) :-
    goal_node(coq_const,A,B,C),goal_node(coq_const,A,D,C),goal_above(A,D,B),!. 
simpl
"4": {"TP": 5, "FP": 50, "FN": 20, "TN": 45, "precision": 0.0909091}

## sorting

simpl
"3": {"TP": 5, "FP": 34, "FN": 49, "TN": 86, "precision": 0.1282051},