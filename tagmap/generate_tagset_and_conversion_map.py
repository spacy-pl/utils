import os
import nltk
import json
import argparse

from typing import NamedTuple
from collections import defaultdict

CORPUS_PATH = os.path.abspath("./data/NKJP_1.2_nltk/")


class Flexeme(NamedTuple):
    subclasses: list

    def convert(self):
        return [s.convert() for s in self.subclasses]


class FlexemeSubclass(NamedTuple):
    tags: list
    card: int

    def convert(self):
        return {"tags": self.tags, "card": self.card}


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


def prepare_structurized_data():
    corpus = nltk.corpus.reader.TaggedCorpusReader(root=CORPUS_PATH, fileids=r"^[^\.]*")
    tags = [x[1] for x in corpus.tagged_words()]
    fqd = nltk.FreqDist(tags)

    sets = fqd.most_common()
    sets = [(s[0].split(':'), s[1]) for s in sets]
    sets = [(s[0][0], s[0][1:], s[1]) for s in sets]
    # now sets is list((main tag, [other tags], cardinality))

    # we want a struct:
    # main_tag : {
    # list(
    #     {tags: [other tags], card: cardinality}
    # )
    # }
    structurized_data = defaultdict(list)
    for s in sets:
        flexeme = s[0]
        flexeme_data = FlexemeSubclass(tags=s[1], card=s[2])
        structurized_data[flexeme] += [flexeme_data]

    return structurized_data


def main(args):
    structurized_data = prepare_structurized_data()

    conversion_function = {}
    result = {}

    for flexeme in structurized_data:
        flexeme_data = structurized_data[flexeme].copy()
        flexeme_data = sorted(flexeme_data, key=lambda x: x.card)

        smallest_subclass = flexeme_data[0]
        fin = []
        while smallest_subclass.card < args.min_cardinality and len(flexeme_data) > 0:
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

                # bug fix: if k1 -> k2 and k2->k3, then k1->k3
                keys_to_update = set()
                for k, v in conversion_function.items():
                    if v == key_1 or v == key_2:
                        keys_to_update.add(k)

                for k in keys_to_update:
                    conversion_function[k] = value

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

    for flexeme in result:
        result[flexeme] = [subclass.convert() for subclass in result[flexeme]]

    # a new tagset (to generate tagmap)
    with open(args.tagset_filepath, 'w') as file:
        file.write(json.dumps(result, indent=4, sort_keys=True))

    # a mapping from original NKJP tagset to our smaller tagset (to convert nkjp)
    with open(args.conversion_map_filepath, 'w') as file:
        file.write(json.dumps(conversion_function, indent=4, sort_keys=True))


if __name__ == "__main__":
    TAGSET_FILEPATH = './data/tagmap_data/transitional_tagset.json'
    CONVERSION_MAP_FILEPATH = './data/tagmap_data/nkjp2us.json'

    parser = argparse.ArgumentParser()
    parser.add_argument('--tagset_filepath', type=str, default=TAGSET_FILEPATH)
    parser.add_argument('--conversion_map_filepath', type=str, default=CONVERSION_MAP_FILEPATH)
    parser.add_argument('-c', '--min_cardinality', type=int, default=100)
    args = parser.parse_args()

    main(args)
