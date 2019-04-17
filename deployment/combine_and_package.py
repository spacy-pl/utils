import tempfile
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
    combined = spacy.load(blank_vectors_path)

    if pos_path:
        pos = spacy.load(pos_path)
        combined.add_pipe(get_component(pos, 'tagger', "POS Tagger"), 'tagger')
    if tree_path:
        tree = spacy.load(tree_path)
        combined.add_pipe(get_component(tree, 'parser', "Dependency Tree Parser"), 'parser')
    if ner_path:
        ner = spacy.load(ner_path)
        combined.add_pipe(get_component(ner, 'ner', "Entity Recognizer"), 'ner')
    return combined


@click.command(help="Combine three trained models into one and package it for convenient use.")
@click.option('-o', '--output-path', type=str)
@click.option('-p', '--pos-path', type=str)
@click.option('-t', '--tree-path', type=str)
@click.option('-n', '--ner-path', type=str)
@click.option('-b', '--blank-vectors-path', type=str)
def main(
        pos_path,
        tree_path,
        ner_path,
        output_path,
        blank_vectors_path,
):
    new_model = combine(pos_path, tree_path, ner_path, blank_vectors_path)
    with tempfile.TemporaryDirectory() as tmp_model_path:
        new_model.to_disk(tmp_model_path)
        cli.package(tmp_model_path, output_path, create_meta=True)


if __name__ == '__main__':
    main()
