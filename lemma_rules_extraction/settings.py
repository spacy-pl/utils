# -*- coding: utf-8 -*-
from os.path import realpath, dirname
from os.path import join as pjoin

settings_path = realpath(__file__)
settings_dir = dirname(settings_path)

NO_FLAG_SGN = '_'

LEMMATIZER_DATA_DIR = pjoin(settings_dir, '../data/lemmatizer_data/')

ISPELL_DICT = pjoin(settings_dir, '../data/lemmatizer_data/polish.dic')
ISPELL_RULES = pjoin(settings_dir, '../data/lemmatizer_data/polish.aff')
PRIVATE_RULES = pjoin(settings_dir, '../data/lemmatizer_data/private.aff')

LEMMA_WORDS = pjoin(settings_dir, '../data/lemmatizer_data/words.json')
LEMMA_RULES = pjoin(settings_dir, '../data/lemmatizer_data/rules.json')
FLAGS_DESC = pjoin(settings_dir, '../data/lemmatizer_data/flag_desc.txt')

LEMMA_SOURCES_DIR = pjoin(LEMMATIZER_DATA_DIR, 'lemma_sources')
