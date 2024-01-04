import json
import random

reader = open("stats/theory_origin_tac.json", "r")
f = json.load(reader)

used = ['QArith', 'Sorting', 'setoid_ring' , 'Init', 'NArith', 'Vectors' ,
        'Logic', 'ZArith', 'Classes', 'FSets', 'rtauto']
theories = list(f.keys())
random.shuffle(theories)
theories = [x for x in theories if x not in used]
print(theories[:5])

# ['Init', 'setoid_ring', 'Vectors', 'omega', 'Classes', 'NArith', 'Floats', 'Relations', 'Strings', 'Arith']
