import os
import json

from collections import defaultdict

import click
import nltk

from strategies import JustPOS

CORPUS_PATH = os.path.abspath("./data/NKJP_1.2_nltk/")


def assert_empty(set, message):
    if len(set) != 0:
        print(list(set).sort())
        raise AssertionError(message)


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

    return structured_data, set(tags)


@click.command(help='Generate tagset and nkjp2us mapping')
@click.option("--tagset-filepath", type=str, default="./data/tagmap_data/transitional_tagset.json")
@click.option("--conversion-map-filepath", type=str, default="./data/tagmap_data/nkjp2us.json")
@click.option("--min-cardinality", type=int, default=100)
@click.option("--strategy", type=str)
def generate_tagset_and_conversion(
        tagset_filepath,
        conversion_map_filepath,
        min_cardinality,
        strategy
):
    structured_data, original_nkjp_tags = prepare_structured_data()

    if strategy == 'justpos':
        strategy_obj = JustPOS()
    else:
        raise ValueError(f"Strategy {strategy} does not exist")

    conversion_function, transitional_tagset = strategy_obj.prepare_conversion(structured_data)

    # assert original nkjp tags and conversion function keys are exactly the same
    diff_keys_original = set(original_nkjp_tags) ^ set(conversion_function.keys())
    assert_empty(diff_keys_original, "Conversion function keys differ from nkjp tags")

    # assert results of conversion equal tags in tagset
    tagset_tags = [pos + ":" + e['tags'] if e['tags'] else pos for pos, l in transitional_tagset.items() for e in l]
    diff_conversion_tagset = set(conversion_function.values()) ^ set(tagset_tags)
    assert_empty(diff_conversion_tagset, "Tagset and right side of conversion function differ")

    with open(tagset_filepath, 'w') as file:
        file.write(json.dumps(transitional_tagset, indent=4, sort_keys=True))

    with open(conversion_map_filepath, 'w') as file:
        file.write(json.dumps(conversion_function, indent=4, sort_keys=True))


if __name__ == "__main__":
    generate_tagset_and_conversion()
