import os
import json

from typing import NamedTuple
from collections import defaultdict

import click
import nltk

from tqdm import tqdm

CORPUS_PATH = os.path.abspath("./data/NKJP_1.2_nltk/")


class Flexeme(NamedTuple):
    subclasses: list

    def convert(self):
        return [s.convert() for s in self.subclasses]


class FlexemeSubclass(NamedTuple):
    tags: list
    card: int

    def convert(self):
        return {"tags": ":".join(self.tags), "card": self.card}


class Candidate(NamedTuple):
    intersection_size: int
    union_card: int
    flexeme_subclass: FlexemeSubclass
    index: int


def get_longest_common_subchain(lst1, lst2):
    longest_substr = []
    if lst1 and lst2:
        opt1 = get_longest_common_subchain(lst1[1:], lst2)
        opt2 = get_longest_common_subchain(lst1, lst2[1:])
        opt3 = get_longest_common_subchain(lst1[1:], lst2[1:])
        if lst1[0] == lst2[0]:
            opt3.insert(0, lst1[0])

        max_l = max([len(l) for l in [opt1, opt2, opt3]])
        for l in [opt1, opt2, opt3]:
            if len(l) == max_l:
                longest_substr = l
                break

    return longest_substr


def concat(A):
    return ":".join(A)


def get_function_keys(k, t, best):
    k1 = k + ':' + concat(t[best.index].tags) if t[best.index].tags else k
    k2 = k + ':' + concat(t[0].tags) if t[0].tags else k
    return k1, k2


def get_function_value(k, best):
    if k == 'ADJC':
        print(best.flexeme_subclass.tags)
    return k + ':' + concat(best.flexeme_subclass.tags) if best.flexeme_subclass.tags else k


def prepare_structurized_data():
    corpus = nltk.corpus.reader.TaggedCorpusReader(root=CORPUS_PATH, fileids=r".*")
    tags = [x[1] for x in corpus.tagged_words()]
    fqd = nltk.FreqDist(tags)

    sets = fqd.most_common()
    sets = [(s[0].split(':'), s[1]) for s in sets]
    sets = [(s[0][0], s[0][1:], s[1]) for s in sets]
    # now sets is list((main tag, [other tags], cardinality))

    assert len(sets) == len(set(tags))
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

    return structurized_data, set(tags)


@click.command(help='Generate tagset and nkjp2us mapping')
@click.option("--tagset-filepath", type=str, default="./data/tagmap_data/transitional_tagset.json")
@click.option("--conversion-map-filepath", type=str, default="./data/tagmap_data/nkjp2us.json")
@click.option("--min-cardinality", type=int, default=100)
def generate_tagset_and_conversion(
        tagset_filepath,
        conversion_map_filepath,
        min_cardinality,
):
    structurized_data, original_nkjp_tags = prepare_structurized_data()

    # conversion_function = {t + ':' + concat(d.tags): t + ':' + concat(d.tags) for t, l in structurized_data.items()
    #                        for d in l if d.tags}
    # conversion_function.update({t: t for t in structurized_data})
    conversion_function = {}
    result = defaultdict(list)

    investigated_tag = 'ADJ'
    print(list(structurized_data.keys())[0])
    for flexeme in structurized_data:
        # print(flexeme)
        flexeme_data = structurized_data[flexeme].copy()
        flexeme_data = sorted(flexeme_data, key=lambda x: x.card)

        if flexeme == investigated_tag:
            print(flexeme_data)
        smallest_subclass = flexeme_data[0]
        fin = []  # czym jest fin do cholery
        while smallest_subclass.card < min_cardinality and len(flexeme_data) > 0:
            if flexeme == investigated_tag:
                print("==============================")
                print(f"Flexeme data: {flexeme_data}")
            smallest_subclass = flexeme_data[0]
            best = Candidate(intersection_size=0, union_card=0, flexeme_subclass=None, index=None)

            # find the best match for current smallest subclass
            for i, match_candidate in enumerate(flexeme_data[1:]):
                merge_tags = get_longest_common_subchain(smallest_subclass.tags, match_candidate.tags)
                merge_card = smallest_subclass.card + match_candidate.card
                intersection_size = len(merge_tags)
                if intersection_size > best.intersection_size:
                    best = Candidate(intersection_size, merge_card, FlexemeSubclass(merge_tags, merge_card), i + 1)
                elif intersection_size == best.intersection_size and merge_card <= best.union_card:
                    best = Candidate(intersection_size, merge_card, FlexemeSubclass(merge_tags, merge_card), i + 1)

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

                # TODO co zrobić jeśli istnieje już klasa o tagu value? - stąd pochodzi ostatni bug

                if flexeme == investigated_tag:
                    print(f"MERGE {key_1}, {key_2} TO {value}")

                del (flexeme_data[best.index])
                del (flexeme_data[0])

                flexeme_data.append(best.flexeme_subclass)

            else:
                fin += [flexeme_data[0]]
                del (flexeme_data[0])

            # now flexeme_data[0] is the smallest subclass again
            flexeme_data = sorted(flexeme_data, key=lambda x: x.card)
            if flexeme_data:
                smallest_subclass = flexeme_data[0]

        flexeme_data += fin
        result[flexeme] += flexeme_data
        # dodaj do funkcji konversji wszystko co jest w flexseme data
        for subclass in flexeme_data:
            value = flexeme + ":" + concat(subclass.tags) if subclass.tags else flexeme
            conversion_function[value] = value

    # usunąć tagi których nie ma w nkjp z lewej strony conversion function
    to_remove = [tag for tag in conversion_function.keys() if tag not in original_nkjp_tags]
    to_remove.sort()
    for tag in to_remove:
        # print(f"Removing {tag}")
        del conversion_function[tag]

    # assert czy wszystkie tagi z nkjp są w conversion function
    nkjp_minus_conv = set(original_nkjp_tags) - set(conversion_function.keys())
    nkjp_minus_conv = list(nkjp_minus_conv)
    nkjp_minus_conv.sort()
    if len(nkjp_minus_conv) != 0:
        print(len(nkjp_minus_conv))
        print(nkjp_minus_conv)
        assert not nkjp_minus_conv

    assert len(conversion_function) == len(original_nkjp_tags)

    for flexeme in result:
        result[flexeme] = [subclass.convert() for subclass in result[flexeme]]

    # po prawej stronie converiosion function i w result powinny być te same tagi
    result_tags = [pos + ":" + e['tags'] if e['tags'] else pos for pos, l in result.items() for e in l]
    result_tags = set(result_tags)
    difference = set(conversion_function.values()) ^ result_tags
    difference = list(difference)
    difference.sort()
    print(len(difference))
    print(difference)
    assert len(difference) == 0

    # a new tagset (to generate tagmap)
    with open(tagset_filepath, 'w') as file:
        file.write(json.dumps(result, indent=4, sort_keys=True))

    # a mapping from original NKJP tagset to our smaller tagset (to convert nkjp)
    with open(conversion_map_filepath, 'w') as file:
        file.write(json.dumps(conversion_function, indent=4, sort_keys=True))


if __name__ == "__main__":
    generate_tagset_and_conversion()
