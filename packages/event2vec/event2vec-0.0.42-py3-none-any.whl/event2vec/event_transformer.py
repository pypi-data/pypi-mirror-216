from pathlib import Path
from typing import List, Union

import numpy as np
import pandas as pd
import polars as pl
import scipy.sparse as sp
from loguru import logger
from sklearn.base import BaseEstimator

from event2vec.config import (
    COLNAME_FOLLOWUP_START,
    COLNAME_PERSON,
    COLNAME_SOURCE_CODE,
    COLNAME_START,
    COLNAME_VALUE,
    OBSERVATION_END,
    OBSERVATION_START,
)
from event2vec.svd_ppmi import event2vec
from event2vec.utils import (
    DataFrameType,
    check_colnames_subset,
    to,
    to_lazyframe,
    to_pandas,
    to_polars,
)


class EventTransformerMixin:
    """Mixin class for all event transformers that requires y at the transform
    step (to align the person id with the features)."""

    def fit_transform(self, X, y=None, **fit_params):  # pragma: no cover
        """
        Fit to data, then transform it.

        Fits transformer to `X` and `y` with optional parameters `fit_params`
        and returns a transformed version of `X`.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input samples.

        y :  array-like of shape (n_samples,) or (n_samples, n_outputs),
            Target values.

        **fit_params : dict
            Additional fit parameters.

        Returns
        -------
        X_new : ndarray array of shape (n_samples, n_features_new)
            Transformed array.
        """
        # fit method of arity 2 (supervised transformation)

        return self.fit(X, y, **fit_params).transform(X)


class OneHotEvent(EventTransformerMixin, BaseEstimator):
    """
    From a event table, create a vocabulary at fit, and pivot the data for a
    count one-hot encoding, ie. count for each code in the vocabulary, and for
    each patient if the event is present or not.
    """

    def __init__(
        self,
        event: DataFrameType,
        n_min_events: int = 10,
        colname_demographics: List[str] = None,
        decay_half_life_in_days: np.array = np.array([0]),
        vocabulary: List[str] = None,
    ) -> None:
        self.vocabulary = vocabulary
        self.n_min_events = n_min_events
        self.colname_demographics = colname_demographics
        self.decay_half_life_in_days = decay_half_life_in_days
        if isinstance(event, pd.DataFrame):
            self.dataframe_type = pl.DataFrame
            self.event = to_polars(event)
        else:
            self.dataframe_type = type(event)
            self.event = event

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.DataFrame = None,
    ):
        # force types
        X_typed = to(X, self.dataframe_type)
        X_event = self.event.join(
            X_typed.select([COLNAME_PERSON]), on=COLNAME_PERSON, how="inner"
        )

        if check_colnames_subset(
            colnames_subset=self.colname_demographics, colnames=X.columns
        ):
            self.colname_demographics_ = self.colname_demographics
        else:
            raise ValueError(
                f"Demographics columns {self.colname_demographics} not in X"
            )
        if self.vocabulary is None:
            self.vocabulary_ = build_vocabulary(
                event=X_event,
                n_min_events=self.n_min_events,
            )
        else:
            self.vocabulary_ = self.vocabulary
        return self

    def transform(self, X: pd.DataFrame) -> np.array:
        X_typed = to(X.reset_index(drop=True), self.dataframe_type)

        X_event = self.event.join(
            X_typed.select([COLNAME_PERSON]), on=COLNAME_PERSON, how="inner"
        )
        X_counts = make_counts_pl(
            event=X_event,
            person_id=X_typed.select([COLNAME_PERSON]),
            decay_half_life_in_days=self.decay_half_life_in_days,
            vocabulary=self.vocabulary_,
            sparse=True,
        ).toarray()

        X_columns = []
        for decay in self.decay_half_life_in_days:
            for code_ in self.vocabulary_:
                X_columns.append(f"{code_}__decay_{decay}")

        X_df = pd.DataFrame(X_counts, columns=X_columns)
        if self.colname_demographics_ is not None:
            X_df = pd.concat(
                [to_pandas(X_typed.select(self.colname_demographics_)), X_df],
                axis=1,
            )
        return X_df


class Event2vecFeaturizer(EventTransformerMixin, BaseEstimator):
    """
    Transformer for the event2vec model.
    """

    def __init__(
        self,
        event: DataFrameType,
        output_dir: str = None,
        colname_code: str = COLNAME_SOURCE_CODE,
        colname_demographics: List[str] = None,
        window_radius_in_days=30,
        window_orientation: str = "center",
        matrix_type: str = "numpy",
        backend="pandas",
        d: int = 150,
        smoothing_factor: float = 0.75,
        k: int = 1,
        n_min_events: int = 10,
        vocabulary: List[str] = None,
        decay_half_life_in_days: np.array = np.array([0]),
    ) -> None:
        if isinstance(event, pd.DataFrame):
            self.dataframe_type = pl.DataFrame
            self.event = to_polars(event)
        else:
            self.dataframe_type = type(event)
            self.event = event
        self.output_dir = output_dir
        self.colname_code = colname_code
        self.window_orientation = window_orientation
        self.window_radius_in_days = window_radius_in_days
        self.matrix_type = matrix_type
        self.backend = backend
        self.d = d
        self.smoothing_factor = smoothing_factor
        self.k = k
        self.n_min_events = n_min_events
        self.vocabulary = vocabulary
        self.colname_demographics = colname_demographics
        self.decay_half_life_in_days = decay_half_life_in_days

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.DataFrame = None,
    ):
        X_typed = to(X, self.dataframe_type)
        X_event = self.event.join(
            to_polars(X_typed.select([COLNAME_PERSON])),
            on=COLNAME_PERSON,
            how="inner",
        )
        if check_colnames_subset(
            colnames_subset=self.colname_demographics, colnames=X.columns
        ):
            self.colname_demographics_ = self.colname_demographics
        else:
            raise ValueError(
                f"Demographics columns {self.colname_demographics} not in X"
            )
        if self.vocabulary is None:
            self.vocabulary_ = build_vocabulary(
                event=X_event,
                n_min_events=self.n_min_events,
            )
        else:
            self.vocabulary_ = self.vocabulary
        restricted_event = restrict_to_vocabulary(
            event=X_event,
            vocabulary=self.vocabulary_,
        )
        # TODO: for now event2vec only supports pandas.
        embedding = event2vec(
            events=to_pandas(restricted_event),
            output_dir=self.output_dir,
            colname_concept=self.colname_code,
            window_radius_in_days=self.window_radius_in_days,
            window_orientation=self.window_orientation,
            matrix_type=self.matrix_type,
            backend=self.backend,
            d=self.d,
            smoothing_factor=self.smoothing_factor,
            k=self.k,
        )
        for v in self.vocabulary_:
            if v not in embedding.columns:
                embedding[v] = np.zeros(shape=embedding.shape[0])
        # order the columns to correspond to the vocabulary.
        self.embedding_ = embedding[self.vocabulary_]
        return self

    def transform(self, X: pd.DataFrame) -> np.array:
        # passing the person ids is necessary to aligne make_counts aggregated
        # rows with the person ids in y.
        X_typed = to(X.reset_index(drop=True), self.dataframe_type)

        X_event = self.event.join(
            X_typed.select([COLNAME_PERSON]), on=COLNAME_PERSON, how="inner"
        )
        X_counts = make_counts_pl(
            event=X_event,
            person_id=X_typed.select([COLNAME_PERSON]),
            decay_half_life_in_days=self.decay_half_life_in_days,
            vocabulary=self.vocabulary_,
            sparse=True,
        )
        embedding_array_ = sp.csr_matrix(
            self.embedding_[self.vocabulary_].values
        )

        embedding_accumulator = [embedding_array_.transpose()] * len(
            self.decay_half_life_in_days
        )
        embedding_repeated = sp.block_diag(embedding_accumulator)
        X_embedded = X_counts.dot(embedding_repeated)
        X_embedded = X_embedded.toarray()

        X_embedded_columns = []
        embedding_dimension = embedding_array_.shape[0]
        for decay_ in self.decay_half_life_in_days:
            for i in range(embedding_dimension):
                X_embedded_columns.append(f"dim_{i}__decay_{decay_}")
        X_embedded_df = pd.DataFrame(X_embedded, columns=X_embedded_columns)
        if self.colname_demographics_ is not None:
            X_embedded_df = pd.concat(
                [
                    to_pandas(X_typed.select(self.colname_demographics_)),
                    X_embedded_df,
                ],
                axis=1,
            )
        return X_embedded_df


class Event2vecPretrained(Event2vecFeaturizer):
    def __init__(
        self,
        event: DataFrameType,
        embeddings: Union[str, Path, pd.DataFrame],
        colname_demographics: str = None,
        colname_code: str = COLNAME_SOURCE_CODE,
        n_min_events: int = 10,
        decay_half_life_in_days: np.array = np.array([0]),
        vocabulary: List[str] = None,
    ) -> None:
        if isinstance(event, pd.DataFrame):
            self.dataframe_type = pl.DataFrame
            self.event = to_polars(event)
        else:
            self.dataframe_type = type(event)
            self.event = event
        self.colname_code = colname_code
        self.n_min_events = n_min_events
        self.colname_demographics = colname_demographics
        self.vocabulary = vocabulary
        self.decay_half_life_in_days = decay_half_life_in_days
        if isinstance(embeddings, str) | isinstance(embeddings, Path):
            self.embeddings = pd.read_parquet(embeddings)
        else:
            self.embeddings = embeddings

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.DataFrame = None,
    ):
        # force types
        X_typed = to(X, self.dataframe_type)
        X_event = self.event.join(
            X_typed.select([COLNAME_PERSON]),
            on=COLNAME_PERSON,
            how="inner",
        )
        if check_colnames_subset(
            colnames_subset=self.colname_demographics, colnames=X.columns
        ):
            self.colname_demographics_ = self.colname_demographics
        else:
            raise ValueError(
                f"Demographics columns {self.colname_demographics} not in X"
            )
        if self.vocabulary is None:
            self.vocabulary = build_vocabulary(
                event=X_event,
                n_min_events=self.n_min_events,
            )
        self.vocabulary_ = list(
            set(self.embeddings.columns).intersection(set(self.vocabulary))
        )
        #
        self.embedding_ = self.embeddings
        return self


## Utils ##
def build_vocabulary(
    event: DataFrameType,
    colname_code: str = COLNAME_SOURCE_CODE,
    n_min_events: int = 10,
) -> List[str]:
    """Create a vocabulary list from a event dataframe.

    Args:
        event (DataFrameType): _description_
        colname_code (str, optional): _description_. Defaults to COLNAME_SOURCE_CODE.
        n_min_events (int, optional): _description_. Defaults to 10.

    Returns:
        List[str]: vocabulary codes.
    """
    n_event_by_code = (
        to_lazyframe(event)
        .select(colname_code)
        .groupby(colname_code)
        .count()
        .collect()
        .to_pandas()
    )
    restricted_codes = n_event_by_code[
        n_event_by_code["count"] >= n_min_events
    ]
    restricted_codes = restricted_codes.sort_values(colname_code)
    return restricted_codes[colname_code].values


def restrict_to_vocabulary(
    event: DataFrameType,
    vocabulary: List,
    colname_code: str = COLNAME_SOURCE_CODE,
) -> DataFrameType:
    restricted_event = to_lazyframe(event).join(
        to_lazyframe(pd.DataFrame(vocabulary, columns=[colname_code])),
        on=colname_code,
        how="inner",
    )
    return to(restricted_event, type(event))


def get_feature_sparsity(X: np.array):  # pragma: no cover
    return (X == 0).sum() / (X.shape[0] * X.shape[1])


def _assert_event_columns(
    event: pd.DataFrame, other_required_columns: List[str] = None
):
    """Check that the event table has the required columns.

    Args:
        event (pd.DataFrame): _description_
        other_required_columns (List[str], optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_
    """
    expected_columns = [COLNAME_PERSON, COLNAME_SOURCE_CODE, COLNAME_START]
    if other_required_columns is not None:
        expected_columns += other_required_columns
    missing_columns = set(expected_columns).difference(set(event.columns))
    if len(missing_columns) > 0:
        raise ValueError(
            f"Missing columns {missing_columns} in the event table."
        )


def make_counts_pl(
    event: DataFrameType,
    person_id: DataFrameType,
    decay_half_life_in_days: np.array = np.array([0, 7]),
    vocabulary: List[str] = None,
    sparse: bool = True,
) -> Union[np.ndarray, sp.csr_matrix]:
    # TODO: warning: inplace modification of event
    _assert_event_columns(
        event, other_required_columns=[COLNAME_FOLLOWUP_START]
    )
    is_lazy_ = isinstance(event, pl.LazyFrame)
    if vocabulary is None:
        vocabulary = event.select(COLNAME_SOURCE_CODE).unique()
        if is_lazy_:
            vocabulary = vocabulary.collect()
        vocabulary = vocabulary.to_series().to_list()
        vocabulary.sort()
    X_accumulator = []
    event = event.with_columns(pl.lit(1).alias(COLNAME_VALUE))
    if is_lazy_:
        person_id_ = to_lazyframe(person_id)
    else:
        person_id_ = to_polars(person_id)
    event = person_id_.select(COLNAME_PERSON).join(
        event,
        on=COLNAME_PERSON,
        how="inner",
    )
    event = event.with_columns(
        (
            (
                pl.col(COLNAME_FOLLOWUP_START) - pl.col(COLNAME_START)
            ).dt.seconds()
            / (24 * 3600)
        ).alias("delta_to_followup")
    )

    for half_life in decay_half_life_in_days:
        if half_life < 0:
            raise ValueError(f"half_life should be positive, got {half_life}")
        # not necessary to set as a variable
        if half_life > 0:
            event = event.with_columns(
                (np.exp(-pl.col("delta_to_followup") / half_life)).alias(
                    COLNAME_VALUE
                )
            )
        # not using pivot since it is not supported by lazy frames
        decayed_X = event.groupby([COLNAME_PERSON, COLNAME_SOURCE_CODE],).agg(
            pl.sum(COLNAME_VALUE),
        )
        # TODO: might be possible to push the collect a little further (after the concatenation)
        if is_lazy_:
            decayed_X = decayed_X.collect()
        decayed_X = decayed_X.pivot(
            index=COLNAME_PERSON,
            columns=COLNAME_SOURCE_CODE,
            values=COLNAME_VALUE,
            aggregate_function="sum",
        )
        for code_ in vocabulary:
            if code_ not in decayed_X.columns:
                decayed_X = decayed_X.with_columns(pl.lit(0).alias(code_))
        decayed_X = decayed_X.select([COLNAME_PERSON, *vocabulary])
        decayed_X.columns = [
            col + f"_count_decay_{half_life}" if col != COLNAME_PERSON else col
            for col in decayed_X.columns
        ]
        # size N x vocabulary
        decayed_X_aligned = (
            to_polars(person_id_)
            .select(COLNAME_PERSON)
            .join(decayed_X, on=COLNAME_PERSON, how="left")
            .fill_null(0)
            .drop(columns=COLNAME_PERSON)
        )
        if sparse:
            decayed_X_aligned = sp.csr_matrix(decayed_X_aligned)
        X_accumulator.append(decayed_X_aligned)
    if sparse:
        X = sp.hstack(X_accumulator)
    else:
        X = np.concatenate(X_accumulator, axis=1)
    return X
