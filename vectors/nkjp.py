import nltk
import os


def load_corpus():
    corpus_path = os.path.abspath("./data/NKJP_1.2_nltk/")
    corpus = nltk.corpus.reader.TaggedCorpusReader(root=corpus_path, fileids=".*")
    return corpus
