import argparse
import json
import os
from collections import defaultdict

import settings


def get_rule(aff_code):
    lemma_suf, ends = aff_code.split('>')
    if ',' in ends:
        lemma_end, word_end = ends.split(',')
        lemma_end = lemma_end.strip()[1:]
        word_end = word_end.strip()
        word_suf = lemma_suf[:-len(lemma_end)] + word_end
    else:
        word_end = ends
        word_suf = lemma_suf + word_end
    return {'word_suf': word_suf, "lemma_suf": lemma_suf}


def read_flag(lines):
    flag = settings.NO_FLAG_SGN
    for aff_code, comment in lines:
        if aff_code.startswith('flag*'):
            flag = aff_code[5]
        else:
            yield flag, aff_code, comment


def extract_information(lines):
    lines = [l.strip() for l in lines]
    lines = skip_uninteresting(lines)
    lines = [l.replace('\t', '') for l in lines]
    # remove empty
    lines = [l for l in lines if l.replace(' ', '') != '']
    lines = [split_on_comment(line) for line in lines]
    lines = [l for l in lines if l[0] != '' or l[1] != '']
    return lines


def skip_uninteresting(lines):
    i = 0
    while "suffixes" not in lines[i]:
        i += 1
    return lines[(i+1):]


def split_on_comment(line):
    if line[0] == '#':
        comment = line[1:]
        aff_code = ''
    else:
        splitted = line.split("#")
        aff_code = splitted[0]
        if len(splitted) > 1:
            comment = splitted[1]
        else:
            comment = ''
    return aff_code.strip().replace(' ', ''), comment.strip()


def save_comments(args, comments):
    with open(args.description_file, "w", encoding='utf-8') as f:
        for flag, c in comments.items():
            f.write("\n===== " + flag + " =====\n")
            f.write('\n'.join(c) + '\n')


def parse_aff_lines(lines):
    processed = extract_information(lines)

    rule_groups = defaultdict(list)
    comments = defaultdict(list)
    for flag, aff_code, comment in read_flag(processed):
        # case: comment line
        if aff_code == '' and comment != '':
            comments[flag].append(comment)
        # case: rule line
        elif aff_code != '':
            rule = get_rule(aff_code)
            rule_groups[flag].append(rule)
        else:
            raise Exception("Unexpected empty line! (on flag: {})".format(flag))

    return rule_groups, comments


def main(args):

    with open(args.ispell_rules, "rb") as f:
            lines = f.readlines()
    lines = [l.decode('iso-8859-2') for l in lines]

    rule_groups, comments = parse_aff_lines(lines)

    if os.path.isfile(args.private_rules):
        with open(args.private_rules, 'r') as f:
            lines = f.readlines()
        priv_rule_groups, priv_comments = parse_aff_lines(lines)

        for key, rules in priv_rule_groups.items():
            rule_groups[key] += rules
        for key, c in priv_comments.items():
            comments[key] += c

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(rule_groups, f)

    if args.verbose:
        for f, r in rule_groups.items():
            print(f, len(r))

    if args.flags:
        save_comments(args, comments)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract rules from ispell aff file to more convenient form")
    parser.add_argument('-r', '--ispell_rules', type=str, help="Ispell aff file path",
                        default=settings.ISPELL_RULES)
    parser.add_argument('-o', '--output', type=str, help="Output file path",
                        default=settings.LEMMA_RULES)
    parser.add_argument('-v', '--verbose', help="Display additional info",
                        action='store_true')
    parser.add_argument('-f', '--flags', help="Generate flags description file",
                        action='store_true')
    parser.add_argument('--description_file', type=str, help="Descrition file path",
                        default=settings.FLAGS_DESC)
    parser.add_argument('--private_rules', type=str, help="Relative path to private rules file",
                        default=settings.PRIVATE_RULES)
    args = parser.parse_args()
    main(args)