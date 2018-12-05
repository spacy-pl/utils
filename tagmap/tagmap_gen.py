import os
import nltk
from tagmap.tagmap_draw import fleksem_to_pos

prefix = """from ..symbols import *
TAG_MAP = {
"""

corpus_path = os.path.abspath("../data/NKJP_1.2_nltk/")
corpus = nltk.corpus.reader.TaggedCorpusReader(root=corpus_path, fileids=".*")

tags = [x[1] for x in corpus.tagged_words()]
fqd = nltk.FreqDist(tags)
sets = fqd.most_common()
sets = [(s[0].split(':'), s[1], s[0]) for s in sets]
sets = [(s[0][0], s[0][1:], s[1], s[2]) for s in sets]
# we want a struct:
# main_tag : {
# list(
#     {tags: [other tags], card: cardinality}
# )
# }
structurized_data = {}
for s in sets:
    k = s[0]
    v = {'tags': s[1], 'card': s[2], 'postag': s[3]}
    if k in structurized_data.keys():
        structurized_data[k] += [v]
    else:
        structurized_data[k] = [v]

tagmap_list = []
for k, v in structurized_data.items():
    for v1 in v:
        tagmap_list += ["\"" + v1['postag'] +
                        "\": {POS: " + fleksem_to_pos[k] +
                        ", 'features': '" + ':'.join(v1['tags'])
                        + "'}"]
        # this could be done better by using dict and converting it to string later

prefix += ',\n'.join(tagmap_list)

prefix += "}"

print(prefix)