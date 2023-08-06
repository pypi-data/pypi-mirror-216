import json
import os
from pathlib import Path
from typing import Dict, Tuple, Union

import numpy as np
import pandas as pd
import polars as pl
from loguru import logger
from scipy.sparse import csr_matrix, save_npz
from sklearn.feature_extraction.text import CountVectorizer

from event2vec.config import COLNAME_PERSON
from event2vec.utils import (
    WINDOW_BACKWARD_LABEL,
    WINDOW_CENTER_LABEL,
    _get_window,
)


def build_cooccurrence_matrix_polars(
    events: Union[pl.DataFrame, pl.LazyFrame],
    output_dir: str = None,
    radius_in_days: int = 30,
    window_orientation: str = "center",
    colname_concept: str = "event_source_concept_id",
    max_patients_by_block: int = 10000,
) -> Tuple[np.array, np.array, Dict]:
    """
    Polars method for building the cooccurrence matrix.
    [WIP]

    Parameters
    ----------
    events : DataFrame
        _description_
    output_dir : str, optional
        _description_, by default None
    radius_in_days : int, optional
        _description_, by default 30
    window_orientation : str, optional
        _description_, by default "center"
    colname_concept : str, optional
        _description_, by default "event_source_concept_id"

    Returns
    -------
    Tuple[np.array, np.array, Dict]
        _description_
    """
    window_start, window_end = _get_window(
        radius_in_days=radius_in_days,
        window_orientation=window_orientation,
        backend="pandas",
    )
    window = window_end - window_start
    if window_orientation == WINDOW_CENTER_LABEL:
        center = True
    elif window_orientation == WINDOW_BACKWARD_LABEL:
        center = False
    else:
        raise ValueError(
            f"Choose window_orientation in {[WINDOW_CENTER_LABEL, WINDOW_BACKWARD_LABEL]}"
        )
    vocabulary_ = events[colname_concept].unique()
    unique_patients = events.person_id.unique()
    n_blocks = len(unique_patients) // max_patients_by_block
    if n_blocks == 0:
        n_blocks = 1
    # iterate over patient blocks
    full_coocurrence_matrix = csr_matrix((len(vocabulary_), len(vocabulary_)))
    for block_id in range(n_blocks):
        if block_id != n_blocks - 1:
            block_patients = unique_patients[
                block_id
                * max_patients_by_block : (block_id + 1)
                * max_patients_by_block
            ]
        else:
            block_patients = unique_patients[
                block_id * max_patients_by_block :
            ]
        block_events = events.merge(
            pd.DataFrame({COLNAME_PERSON: block_patients}),
            how="inner",
            on=COLNAME_PERSON,
        )
        events_sorted = block_events.sort_values(["person_id", "start"])
        events_in_window = events_sorted.groupby("person_id")[
            [colname_concept, "start"]
        ].rolling(
            on="start", window=str(window) + "D", center=center, closed="both"
        )
        sep_tok = "<SEP>"
        # TODO: explode the memory usage
        windowed_events = [
            sep_tok.join(w.tolist()) for w in events_in_window[colname_concept]
        ]
        # TODO: we can do better than joining the word and then making the
        # countvectorizer split them. Eg. build a dummy analyzer that does nothing
        transformer = CountVectorizer(
            analyzer=lambda x: x.split(sep_tok),
            vocabulary=vocabulary_,
            lowercase=False,
        )
        sparse_counts = transformer.fit_transform(windowed_events)
        encoder = transformer.vocabulary_
        vocabulary_size = len(encoder.keys())
        context_encoded = (
            events_sorted[colname_concept].apply(lambda x: encoder[x]).values
        )
        # use fast sparse matrix product to sum each occurrence by context
        rows = np.arange(len(context_encoded))
        cols = context_encoded
        values = np.ones(len(context_encoded))
        context_matrix = csr_matrix(
            (values, (rows, cols)),
            shape=(len(context_encoded), vocabulary_size),
        ).transpose()
        sparse_cooccurrence = context_matrix.dot(sparse_counts)
        # Have to withdraw the diagonal to avoid double counting
        contexts_ix, n_contexts = np.unique(
            context_encoded, return_counts=True
        )
        diagonal_context = csr_matrix(
            (n_contexts, (contexts_ix, contexts_ix)),
            shape=(vocabulary_size, vocabulary_size),
        )

        block_cooccurrence_matrix = sparse_cooccurrence - diagonal_context
        full_coocurrence_matrix = (
            full_coocurrence_matrix + block_cooccurrence_matrix
        )

    if output_dir is not None:
        logger.info(
            f"Saving coocurrence_matrix, event_count and vocabulary at {output_dir}"
        )
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        path2matrix = str(Path(output_dir) / "cooccurrence_matrix.npz")
        logger.info(f"Saving cooccurrence matrix as parquet at: {path2matrix}")
        save_npz(path2matrix, full_coocurrence_matrix)

        with open(os.path.join(output_dir, "vocabulary.json"), "w") as file:
            json.dump(encoder, file)
        np.save(os.path.join(output_dir, "event_count.npy"), n_contexts)
    return full_coocurrence_matrix, n_contexts, encoder
