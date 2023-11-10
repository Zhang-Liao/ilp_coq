import json
import random

reader = open("stats/theory_tac.json", "r")
f = json.load(reader)

theories = list(f.keys())
random.shuffle(theories)
print(theories[:10])

# ['Init', 'setoid_ring', 'Vectors', 'omega', 'Classes', 'NArith', 'Floats', 'Relations', 'Strings', 'Arith']
