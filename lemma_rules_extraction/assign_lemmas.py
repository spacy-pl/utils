import json
from collections import defaultdict

with open("../data/polish.dic", "rb") as f:
        lines = f.readlines()

lines = [l.decode('iso-8859-2').strip() for l in lines]
lines = [(l.split('/')) if '/' in l else (l, " ") for l in lines]

words_dict = defaultdict(list)
for word, flags in lines:
    if flags == "":
        words_dict[""].append(word)
    else:
        for f in flags:
            words_dict[f].append(word)

for f, w in words_dict.items():
    print(f, len(w))

with open("words.json", "w") as f:
    json.dump(words_dict, f)
