import scipy.stats as stats

tacs = [
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
    "order",
    "ring",
    "left",
]
K = 10
tacs = tacs[:K]
init = dict(zip(tacs, [0]*10))
print(init)
prop = ['', '']


