import os
import json

from collections import defaultdict

import click
import nltk

from strategies import JustPOS

CORPUS_PATH = os.path.abspath("./data/NKJP_1.2_nltk/")


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
