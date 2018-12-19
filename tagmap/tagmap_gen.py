import os
import json
from tagmap_draw import fleksem_to_pos

prefix = """from ..symbols import *
TAG_MAP = {
"""

with open(os.path.expanduser('./data/pos.json'), 'r') as f:
    structurized_data = json.load(f)

tagmap_list = []
for k, v in structurized_data.items():
    for v1 in v:
        tagmap_list += [
            "\"" + ':'.join([k]+v1['tags']) +
            "\": {POS: " + fleksem_to_pos[k] +
            ", 'features': '" + ':'.join(v1['tags'])
            + "'}"
        ]
        # this could be done better by using dict and converting it to string later

res = prefix

res += ',\n'.join(tagmap_list)

res += "}"

with open(os.path.expanduser('./data/tagmap.py'), 'w') as f:
    f.write(res)
