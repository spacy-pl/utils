import os
import re
import json

with open('./data/nkjp2us.json', 'r') as f:
    tag_conversion_map = json.load(f)

tag_conversion = [{'old': k.lower(), 'new': v.lower()} for k, v in tag_conversion_map.items()]
tag_conversion = sorted(tag_conversion, key=lambda x: len(x['new']))
nkjp_path = os.path.expanduser('./data/NKJP_1.2_nltk/')
nkjp_path_converted = os.path.expanduser(nkjp_path[:-1]+'_converted/')
if not os.path.isdir(nkjp_path_converted):
    os.mkdir(nkjp_path_converted)
nkjp_files = os.listdir(nkjp_path)
nkjp_files = [file for file in nkjp_files if os.path.isfile(os.path.join(nkjp_path, file))]
fails = []
for corpus_file in nkjp_files:
    with open(os.path.join(nkjp_path, corpus_file), 'r') as f:
        try:
            res = f.read()
            print(nkjp_path+corpus_file)
            for tag_pair in tag_conversion:
                res = re.sub(tag_pair['old']+"[^:]", tag_pair['new'], res)

            with open(nkjp_path_converted+corpus_file, 'w+') as g:
                g.write(res)

        except Exception as e:
            print(e)
            print(corpus_file)
            fails += [corpus_file]


if len(fails) > 0:
    print("Failed:")
    print(fails)
