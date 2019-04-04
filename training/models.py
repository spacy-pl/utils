import os
import tempfile
import json
from sklearn.model_selection import ParameterGrid
from dataclasses import dataclass, asdict

import click
import spacy
import pandas as pd


@dataclass
class TrainParams(object):
    n_iter: int=30
    early_stopping_iter: int=2
    n_examples: int=0
    use_gpu: int=0 # use -1 if no GPU
    noise_level: float=0.0
    gold_preproc: bool=True
    verbose: bool=False


@dataclass
class TestParams(object):
    gpu_id: int=1
    gold_preproc: bool=True
    displacy_path: str=None
    displacy_limit: int=25


class SpacyModel(object):
    """
    Base class for spaCy model wrappers that has sklearn-like interface
    which works nicely for evaluation and hyperparameter tuning.
    """
    def __init__(self, task: str, vectors_path: str, location: str, hyperparams: dict, lang: str='pl'):
        self.lang = lang
        self.task = task
        self.vectors_path = vectors_path
        self.location = location
        self.hyperparams = hyperparams

    @property
    def best_model_path(self):
        return os.path.join(self.location, 'model-best')

    @property
    def final_model_path(self):
        return os.path.join(self.location, 'model-final')

    @property
    def model_path(self):
        # models trained using older version of spaCy don't remember best iteration:
        if os.path.exists(self.best_model_path):
            return self.best_model_path
        else:
            return self.final_model_path

    @property
    def meta_path(self):
        return os.path.join(self.model_path, 'meta.json')

    def fit(self, train_path: str, dev_path: str, train_params: TrainParams=TrainParams()) -> dict:
        for key in self.hyperparams:
            os.environ[key] = str(self.hyperparams[key])
        spacy.cli.train(
            lang=self.lang,
            pipeline='tagger',
            output_path=self.location,
            train_path=train_path,
            dev_path=dev_path,
            vectors=self.vectors_path,
            base_model=None,
            **asdict(train_params)
        )
        self.meta = json.load(open(self.meta_path))
        return self.meta

    def score(self, data_path: str, test_params: TestParams=TestParams()) -> dict:
        self.scores = spacy.cli.evaluate(
            model=self.best_model_path,
            data_path=data_path,
            return_scores=True,
            **asdict(test_params)
        )
        return self.scores

@click.command("Demonstrates how to use model wrappers for hyperparameter grid search.")
@click.option('-v', '--vectors-path', required=True, type=str)
@click.option('-t', '--train-data-path', required=True, type=str)
@click.option('-d', '--dev-data-path', required=True, type=str)
@click.option('-T', '--test-data-path', required=True, type=str)
@click.option('-o', '--output-path', default=None, type=str)
def grid_search_example(vectors_path, train_data_path, dev_data_path, test_data_path, output_path):
    """
    Demonstrates how to use model wrappers for hyperparameter grid search.
    """
    param_grid = {
        'hidden_width': [64, 128],
        'dropout_from': [0.2, 0.4],
        'dropout_to': [0.4],
    }
    # using very small trainin sample for demonstration to complete quickly - these results are useless
    demo_train_params = TrainParams(n_iter=5, n_examples=100, use_gpu=-1)
    score_dfs = []
    print(f"Performing grid search on following hyperparameters: {list(param_grid.keys())}")
    for idx, hyperparams in enumerate(ParameterGrid(param_grid)):
        print(f"Checking parameter set #{idx+1}...")
        with tempfile.TemporaryDirectory() as tmp_location:
            model = SpacyModel('tagger', vectors_path, tmp_location, hyperparams)
            model.fit(train_data_path, dev_data_path, demo_train_params)
            scores = model.score(test_data_path)
            params_and_scores_row = pd.DataFrame({**hyperparams, **scores}, index=[idx])
            score_dfs.append(params_and_scores_row)
    print("Results:")
    result = pd.concat(score_dfs, axis='index')
    print(result)
    if output_path is not None:
        print(f"Saving to {output_path}")
        result.to_csv(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    grid_search_example()
