import json

theory_tac = json.load(open("stats/theory_tac.json", "r"))
out = "stats/balanced_tac.json"
balanced = {}
common = [
    "auto",
    "intros",
    "simpl",
    "reflexivity",
    "assumption",
    "trivial",
    "intro",
    "split",
    "intuition",
    "discriminate",
]

for theory, tacs in theory_tac.items():
    popular_tacs = set(tacs.keys())
    shared = list(popular_tacs.intersection(common))
    balanced[theory] = {}
    for t in shared:
        balanced[theory][t] = tacs[t]
    # print(theory)
    # print(tacs.intersection(common))


balanced = sorted(balanced.items(), key=lambda x: len(x[1]), reverse=True)
balanced = dict(balanced)
json.dump(balanced, open(out, "w"))
