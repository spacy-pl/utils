import os
import nltk
import json
from typing import NamedTuple

CORPUS_PATH = os.path.abspath("./data/NKJP_1.2_nltk/")


class Flexeme(NamedTuple):
    subclasses: list


class FlexemeSubclass(NamedTuple):
    tags: list
    card: int


class Candidate(NamedTuple):
    intersection_size: int
    union_card: int
    flexeme_subclass: FlexemeSubclass
    index: int


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


def get_function_keys(k, t, best):
    k1 = k + ':' + concat(t[best.index].tags)
    k2 = k + ':' + concat(t[0].tags)
    return k1, k2


def get_function_value(k, best):
    return k + ':' + concat(best.flexeme_subclass.tags)


corpus = nltk.corpus.reader.TaggedCorpusReader(root=CORPUS_PATH, fileids=r"^[^\.]*")
tags = [x[1] for x in corpus.tagged_words()]
fqd = nltk.FreqDist(tags)

sets = fqd.most_common()
sets = [(s[0].split(':'), s[1]) for s in sets]
sets = [(s[0][0], s[0][1:], s[1]) for s in sets]
# we want a struct:
# main_tag : {
# list(
#     {tags: [other tags], card: cardinality}
# )
# }
structurized_data = {}
for s in sets:
    flexeme = s[0]
    flexeme_data = FlexemeSubclass(tags=s[1], card=s[2])
    if flexeme in structurized_data.keys():
        structurized_data[flexeme] += [flexeme_data]
    else:
        structurized_data[flexeme] = [flexeme_data]


conversion_function = {}

result = {}

for flexeme in structurized_data:
    flexeme_data = structurized_data[flexeme].copy()
    flexeme_data = sorted(flexeme_data, key=lambda x: x.card)

    smallest_subclass = flexeme_data[0]
    fin = []
    while smallest_subclass.card < 100 and len(flexeme_data) > 0:
        smallest_subclass = flexeme_data[0]
        best = Candidate(intersection_size=0, union_card=0, flexeme_subclass=None, index=None)

        # find the best match for current smallest subclass
        for i, match_candidate in enumerate(flexeme_data[1:]):
            merge_tags = intersection(smallest_subclass.tags, match_candidate.tags)
            merge_card = smallest_subclass.card + match_candidate.card
            intersection_size = len(merge_tags)
            if intersection_size > best.intersection_size:
                best = Candidate(intersection_size, merge_card, FlexemeSubclass(merge_tags, merge_card), i)
            elif intersection_size == best.intersection_size and merge_card <= best.union_card:
                best = Candidate(intersection_size, merge_card, FlexemeSubclass(merge_tags, merge_card), i)

        if best.index is not None:
            # merge two matched subclasses, delete them and insert the result
            key_1, key_2 = get_function_keys(flexeme, flexeme_data, best)
            value = get_function_value(flexeme, best)
            conversion_function[key_1] = value
            conversion_function[key_2] = value

            del (flexeme_data[best.index])
            del (flexeme_data[0])

            flexeme_data.append(best.flexeme_subclass)
            # now flexeme_data[0] is the smallest subclass again
            flexeme_data = sorted(flexeme_data, key=lambda x: x.card)

        else:
            fin += [flexeme_data[0]]
            del (flexeme_data[0])

    flexeme_data += fin
    if flexeme in result:
        result[flexeme] += flexeme_data
    else:
        result[flexeme] = flexeme_data

# a new tagset (to generate tagmap)
with open('./data/pos.json', 'w') as file:
    file.write(json.dumps(result))

# a mapping from original NKJP tagset to our smaller tagset (to convert nkjp)
with open('./data/nkjp2us.json', 'w') as file:
    file.write(json.dumps(conversion_function))
