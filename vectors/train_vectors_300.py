from gensim.models import Word2Vec

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import nkjp


DIMENSION=300
OUTPUT_NAME="data/vectors_300.txt"

corpus=nkjp.load_corpus()
sents=corpus.sents()
model=Word2Vec(sentences=sents, size=DIMENSION, min_count=1, workers=4)
model.wv.save_word2vec_format(OUTPUT_NAME)

