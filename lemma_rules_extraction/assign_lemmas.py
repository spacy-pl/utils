import argparse
import json
from collections import defaultdict

import settings


def make_flag_word_dict(splitted):
    words_dict = defaultdict(list)
    for word, flags in splitted:
        for f in flags:
            words_dict[f].append(word)
    return words_dict


def decode_and_split(lines):
    lines = [l.decode('iso-8859-2').strip() for l in lines]
    splitted = [(l.split('/')) if '/' in l else (l, settings.NO_FLAG_SGN) for l in lines]
    return splitted


def main(args):
    with open(args.dict, "rb") as f:
            lines = f.readlines()

    splitted = decode_and_split(lines)
    words_dict = make_flag_word_dict(splitted)

    if args.verbose:
        for f, w in words_dict.items():
            print(f, len(w))

    with open(args.output, "w") as f:
        json.dump(words_dict, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assigns lemmas to lemmatization rule flags')
    parser.add_argument('-d', '--dict', type=str, help='Ispell dict path',
                        default=settings.ISPELL_DICT)
    parser.add_argument('-o', '--output', type=str, help='Output file path',
                        default=settings.LEMMA_WORDS)
    parser.add_argument('-v', '--verbose', help='Display additional info',
                        action='store_true')
    args = parser.parse_args()
    main(args)
