import os
import json
import argparse

from tagmap_draw import fleksem_to_pos

PREFIX = """# coding: utf8
from __future__ import unicode_literals
from ..symbols import *\n
TAG_MAP = {
"""


def main(args):
    with open(os.path.expanduser(args.tagset_filepath), 'r') as f:
        structurized_data = json.load(f)

    tagmap_list = []
    for k, v in structurized_data.items():
        for v1 in v:
            tagmap_list += [
                "    \"" + ':'.join([k]+v1['tags']) +
                "\": {POS: " + fleksem_to_pos[k] +
                "}"
            ]
            # this could be done better by using dict and converting it to string later

    res = PREFIX

    res += ',\n'.join(tagmap_list)

    res += "}"

    with open(os.path.expanduser(args.tagmap_filepath), 'w') as f:
        f.write(res)


if __name__ == "__main__":
    TAGSET_FILEPATH = './data/tagmap_data/transitional_tagset.json'
    TAGMAP_FILEPATH = './data/tagmap_data/tag_map.py'

    parser = argparse.ArgumentParser()
    parser.add_argument('--tagset_filepath', type=str, default=TAGSET_FILEPATH)
    parser.add_argument('--tagmap_filepath', type=str, default=TAGMAP_FILEPATH)
    args = parser.parse_args()

    main(args)
