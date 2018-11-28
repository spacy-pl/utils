import re
import json
from collections import defaultdict, namedtuple
# aktualne dane pochodzą z sjp-ispell-pl-20181128-src
Rawrule = namedtuple("Rawrule", ["suf", "lemma_end", "word_end", "comment"])

def extract_comment(line):
    if line[0] == '#':
        comment = line[1:]
        line = ''
    else:
        splitted = line.split("#")
        line = splitted[0]
        if len(splitted) > 1:
            comment = splitted[1]
        else:
            comment = ''
    return line, comment

with open("../data/polish.aff", "rb") as f:
        lines = f.readlines()

lines = [l.decode('iso-8859-2').strip() for l in lines]
lines = lines[34:] # pominięcie pierwszych linii
lines = [l.replace('\t', '') for l in lines]
lines = [l for l in lines if l.replace(' ', '') != '']
lines = [(l.replace(' ', ''), c.strip()) for l, c in [extract_comment(line) for line in lines]]
lines = [l for l in lines if l[0] != '' or l[1] != '']

rule_groups = defaultdict(list)
comments = defaultdict(list)
flag = ''
print(len(lines))
for i, l in enumerate(lines):
    line = l[0]
    if line.startswith('flag*'):
        flag = line[5]
    elif line == '' and l[1] != '':
        comments[flag].append(l[1])
    elif line != '':
        suf, ends = (line).split('>')
        if ',' in ends:
            lemma_end, word_end = (" " + ends + " ").split(',')
            lemma_end = lemma_end.strip()[1:]
            word_end = word_end.strip()
            word_suf = suf[:-len(lemma_end)] + word_end
        else:
            lemma_end = ''
            word_end = ends
            word_suf = suf + word_end
        rule_groups[flag].append({'word_suf': word_suf, "lemma_suf": suf})
        # print('\t'.join([line, word_suf, suf]))
    else:
        print("UUUPS PROBLEM", i, l)
with open("rules.json", 'w') as f:
    json.dump(rule_groups, f)

# with open("opisy_flag.txt", "w") as f:
#     for flag, c  in comments.items():
#         f.write("\n===== " + flag + " =====\n")
#         f.write('\n'.join(c) + '\n')
