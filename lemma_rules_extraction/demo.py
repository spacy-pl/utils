import json
import argparse
import re

import settings


def main(args):
    with open(settings.LEMMA_RULES, "r") as f:
        rule_groups = json.load(f)
    with open(settings.LEMMA_WORDS, "r") as f:
        word_groups = json.load(f)

    lemmas = set()
    for f, r in rule_groups.items():
        for rule in r:
            if re.search(r'{}$'.format(rule['word_suf']), args.word.upper()):
                new_word_suf = rule['word_suf'].replace('[', '([').replace(']', '])')
                new_lemma_suf = re.sub(r'\[.*\]', r'\\1', rule['lemma_suf'])
                lemma = re.sub(r'{}$'.format(new_word_suf), r'{}'.format(new_lemma_suf), args.word.upper())
                if args.verbose:
                    print(args.word, rule['word_suf'], rule['lemma_suf'], lemma)
                lemmas.add(lemma)
                
    result = set()
    lemmas = {l.lower() for l in lemmas}
    print("Possible lemmas", lemmas)
    for f, w in word_groups.items():
        for word in w:
            if word in lemmas:
                result.add(word)
    print("Confirmed lemmas", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lemmatize word')
    parser.add_argument('word', type=str, help='word to lemmatize')
    parser.add_argument('--pos', type=str, help='pos tag of word')
    parser.add_argument('-v', '--verbose', help="Display additional info",
                        action='store_true')
    args = parser.parse_args()
    main(args)
