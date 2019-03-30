import click
import shutil

import spacy
from spacy import cli


def get_component(model, spacy_name, full_name):
    for name, component in model.pipeline:
        if name == spacy_name:
            return component
    raise ValueError("There is no component '{}' in selected model!".format(full_name))


def combine(
        pos_path,
        tree_path,
        ner_path,
        blank_vectors_path,
):
    pos = spacy.load(pos_path)
    tree = spacy.load(tree_path)
    ner = spacy.load(ner_path)

    combined = spacy.load(blank_vectors_path)
    combined.add_pipe(get_component(pos, 'tagger', "POS Tagger"), 'tagger')
    combined.add_pipe(get_component(tree, 'parser', "Dependency Tree Parser"), 'parser')
    combined.add_pipe(get_component(ner, 'ner', "Entity Recognizer"), 'ner')
    return combined


@click.command(help="Combine three trained models into one and package it for convenient use.")
@click.option('--output-path', type=str)
@click.option('--pos-path', type=str)
@click.option('--tree-path', type=str)
@click.option('--ner-path', type=str)
@click.option('--blank-vectors-path', type=str)
def main(
        pos_path,
        tree_path,
        ner_path,
        output_path,
        blank_vectors_path,
):
    TMP_MODEL_PATH = './models/tmp_for_package/'
    new_model = combine(pos_path, tree_path, ner_path, blank_vectors_path)
    new_model.to_disk(TMP_MODEL_PATH)

    cli.package(TMP_MODEL_PATH, output_path, create_meta=True)
    shutil.rmtree(TMP_MODEL_PATH)


if __name__ == '__main__':
    main()
