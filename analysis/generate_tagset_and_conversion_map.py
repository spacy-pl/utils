import os
import nltk

corpus_path=os.path.abspath("./data/NKJP_1.2_nltk/")
corpus=nltk.corpus.reader.TaggedCorpusReader(root=corpus_path, fileids=".*")

tags = [x[1] for x in corpus.tagged_words()]
fqd = nltk.FreqDist(tags)

# @TODO merge tags so that their cardinalities are ≥  100, 1000
sets = fqd.most_common()
sets = [(s[0].split(':'), s[1]) for s in sets]
sets = [(s[0][0], s[0][1:], s[1]) for s in sets]
# sets = {s[0][0]:{'tags':s[0][1:], 'card': s[1]} for s in sets}
# we want a struct:
# main_tag : {
# list(
#     {tags: [other tags], card: cardinality}
# )
# }
structurized_data = {}
for s in sets:
    k = s[0]
    v = {'tags': s[1], 'card': s[2]}
    if k in structurized_data.keys():
        structurized_data[k]+=[v]
    else:
        structurized_data[k] =[v]


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def concat(A):
    res = ""
    for a in A:
        res += ':'
        res += a

    res = res[1:]
    return res


def flatten(A):
    def merge(B):
        tmp = {'tags': B[0]['tags'], 'card': 0}
        for el in B:
            tmp['card'] += el['card']
        return tmp

    sets = {}
    for el in A:
        key = concat(el['tags'])
        if key in sets:
            sets[key] += [el]
        else:
            sets[key] = [el]

    res = []
    for k, v in sets.items():
        res += [merge(v)]

    return res


res_f = {}
from queue import *

result = {}

# for each POS
for k in structurized_data:
    t = structurized_data[k].copy()
    t = sorted(t, key=lambda x: x['card'])

    p = t[0]
    fin = []
    while (p['card'] < 100 and len(t) > 0):
        p = t[0]
        best = (0, 0, None, None, None, None)

        # find the best match for current set p
        for i in range(1, len(t)):
            r = t[i]
            pr_tags = intersection(p['tags'], r['tags'])
            pr_card = p['card'] + r['card']
            intersection_size = len(pr_tags)
            if (intersection_size > best[0]):
                best = (intersection_size, pr_card, {'tags': pr_tags, 'card': pr_card}, i)
            elif (intersection_size == best[0] and pr_card <= best[1]):
                best = (intersection_size, pr_card, {'tags': pr_tags, 'card': pr_card}, i)

        # if we can merge it, do so and update t, so that the next p:=t[0] will be the new smallest set
        if best[3] is not None:
            # this print is useful if we want to know/check what sets have we merged
            # print(f'From {k} deleted {t[best[3]]} and {t[0]} ({best[3]}) \n added {best[2]}')
            res_f[k + ':' + concat(t[best[3]]['tags'])] = k + ':' + concat(best[2]['tags'])
            res_f[k + ':' + concat(t[0]['tags'])] = k + ':' + concat(best[2]['tags'])
            del (t[best[3]])
            del (t[0])

            t.append(best[2])
            t = sorted(t, key=lambda x: x['card'])

        else:
            fin += [t[0]]
            del (t[0])

    t += fin
    if k in result:
        result[k] += t
    else:
        result[k] = t


import json

# a new tagset (to generate tagmap)
with open('./data/pos.json', 'w') as file:
     file.write(json.dumps(result))

# a mapping from original NKJP tagset to our smaller tagset (to convert nkjp)
with open('./data/nkjp2us.json', 'w') as file:
    file.write(json.dumps(res_f))