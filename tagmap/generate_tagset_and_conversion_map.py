import os
import json

from typing import NamedTuple
from collections import defaultdict

import click
import nltk

from tqdm import tqdm
from strategies import JustPOS

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


def get_longes_common_subchain(lst1, lst2):
    longest_substr = []
    if lst1 and lst2:
        opt1 = get_longes_common_subchain(lst1[1:], lst2)
        opt2 = get_longes_common_subchain(lst1, lst2[1:])
        opt3 = get_longes_common_subchain(lst1[1:], lst2[1:])
        if lst1[0] == lst2[0]:
            opt3.insert(0, lst1[0])

        max_l = max([len(l) for l in [opt1, opt2, opt3]])
        for l in [opt1, opt2, opt3]:
            if len(l) == max_l:
                longest_substr = l
                break

    return longest_substr


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


def prepare_structured_data():
    corpus = nltk.corpus.reader.TaggedCorpusReader(root=CORPUS_PATH, fileids=r".*")
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
    structured_data = defaultdict(list)
    for s in sets:
        flexeme = s[0]
        flexeme_data = dict(tags=s[1], card=s[2])
        structured_data[flexeme] += [flexeme_data]

    return structured_data


@click.command(help='Generate tagset and nkjp2us mapping')
@click.option("--tagset-filepath", type=str, default="./data/tagmap_data/transitional_tagset.json")
@click.option("--conversion-map-filepath", type=str, default="./data/tagmap_data/nkjp2us.json")
@click.option("--min-cardinality", type=int, default=100)
@click.option("--strategy", type=str, default='justpos')
def generate_tagset_and_conversion(
        tagset_filepath,
        conversion_map_filepath,
        min_cardinality,
        strategy
):
    structured_data = prepare_structured_data()

    if strategy == 'justpos':
        strategy_obj = JustPOS()
    else:
        raise ValueError(f"Strategy {strategy} does not exist")

    conversion_function, transitional_tagset = strategy_obj.prepare_conversion(structured_data)

    # a new tagset (to generate tagmap)
    with open(tagset_filepath, 'w') as file:
        file.write(json.dumps(transitional_tagset, indent=4, sort_keys=True))

    # a mapping from original NKJP tagset to our smaller tagset (to convert nkjp)
    with open(conversion_map_filepath, 'w') as file:
        file.write(json.dumps(conversion_function, indent=4, sort_keys=True))


if __name__ == "__main__":
    generate_tagset_and_conversion()
