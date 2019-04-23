import os
import json
import argparse

from flexemes2UD import flexeme_to_pos

PREFIX = """# coding: utf8
from __future__ import unicode_literals
from ...symbols import POS, PUNCT, SYM, ADJ, CCONJ, SCONJ, NUM, DET, ADV, ADP, X, VERB
from ...symbols import NOUN, PROPN, PART, INTJ, PRON, AUX


TAG_MAP_AUX = {
"""


def main(args):
    with open(os.path.expanduser(args.tagset_filepath), 'r') as f:
        structurized_data = json.load(f)

    tagmap_list = []
    for k, v in structurized_data.items():
        for v1 in v:
            tagmap_list += [
                "    \"" + ':'.join([k]+v1['tags']) +
                "\": {POS: " + flexeme_to_pos[k] +
                "}"
            ]
            # this could be done better by using dict and converting it to string later

    res = PREFIX

    res += ',\n'.join(tagmap_list)

    res += ",\n}"

    with open(os.path.expanduser(args.tagmap_filepath), 'w') as f:
        f.write(res)


if __name__ == "__main__":
    TAGSET_FILEPATH = './data/tagmap_data/transitional_tagset.json'
    TAGMAP_FILEPATH = './data/tagmap_data/tag_map_aux.py'

    parser = argparse.ArgumentParser()
    parser.add_argument('--tagset_filepath', type=str, default=TAGSET_FILEPATH)
    parser.add_argument('--tagmap_filepath', type=str, default=TAGMAP_FILEPATH)
    args = parser.parse_args()

    main(args)
