import os
import tempfile
import json
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import ParameterSampler
from scipy.stats.distributions import uniform, norm
from dataclasses import dataclass, asdict

import click
import spacy
import pandas as pd
import numpy as np

from models import SpacyModel


@dataclass
class TrainParams(object):
    n_iter: int = 60
    early_stopping_iter: int = 2
    n_examples: int = 0
    use_gpu: int = 0  # use -1 if no GPU
    noise_level: float = 0.0
    gold_preproc: bool = True
    verbose: bool = False


@dataclass
class TestParams(object):
    gpu_id: int = 1
    gold_preproc: bool = True
    displacy_path: str = None
    displacy_limit: int = 25


@click.command("Demonstrates how to use model wrappers for hyperparameter grid search.")
@click.option('-v', '--vectors-path', required=True, type=str)
@click.option('-t', '--train-data-path', required=True, type=str)
@click.option('-d', '--dev-data-path', required=True, type=str)
@click.option('-T', '--test-data-path', required=True, type=str)
@click.option('-o', '--output-path', default=None, type=str)
@click.option('-n', '--sample-number', default=30, type=int)
def grid_search_example(
        vectors_path,
        train_data_path,
        dev_data_path,
        test_data_path,
        output_path,
        sample_number,
):
    """
    Demonstrates how to use model wrappers for hyperparameter grid search.
    """
    param_grid = {
        'dropout_from': np.arange(0.2, 0.6, 0.05),
        'l2_penalty': [10 ** p for p in np.arange(-7, -4, 0.5)],
        'token_vector_width': [128, 265],
    }
    # using very small trainin sample for demonstration to complete quickly - these results are useless
    demo_train_params = TrainParams()
    score_dfs = []
    print(f"Performing grid search on following hyperparameters: {list(param_grid.keys())}")
    for idx, hyperparams in enumerate(ParameterSampler(param_grid, n_iter=sample_number, random_state=42)):
        print(f"Checking parameter set #{idx + 1}...")
        with tempfile.TemporaryDirectory() as tmp_location:
            model = SpacyModel('tagger', vectors_path, tmp_location, hyperparams)
            model.fit(train_data_path, dev_data_path, demo_train_params)
            scores = model.score(test_data_path)
            params_and_scores_row = pd.DataFrame({**hyperparams, **scores}, index=[idx])
            score_dfs.append(params_and_scores_row)

            # to make sure we can stop program without loosing data
            result = pd.concat(score_dfs, axis='index')
            if output_path is not None:
                result.to_csv(output_path, index=False)

    print("Results:")
    result = pd.concat(score_dfs, axis='index')
    print(result)
    if output_path is not None:
        print(f"Saving to {output_path}")
        result.to_csv(output_path, index=False)
    print("Done.")


if __name__ == "__main__":
    grid_search_example()
