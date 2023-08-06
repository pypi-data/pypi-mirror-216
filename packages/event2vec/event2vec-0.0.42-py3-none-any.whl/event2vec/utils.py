from dataclasses import dataclass
from itertools import chain
from typing import List, Union

import pandas as pd
import polars as pl


def days_to_seconds(days: int) -> int:
    return days * 86400


def join_lists(list_2d: List[List[str]]) -> List[str]:
    return list(chain(*list_2d))


WINDOW_CENTER_LABEL = "center"
WINDOW_BACKWARD_LABEL = "backward"


def _get_window(radius_in_days: float, window_orientation: str, backend: str):
    """Create the window context for the cooccurrence matrix, adapted for each
    backend: in days for pandas, in seconds for spark.

    Args:
        radius_in_days (float): _description_
        window_orientation (str): _description_
        backend (str): Either pandas or spark

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if backend == "spark":
        # timesecond are necessary for the window function of spark
        radius_ = days_to_seconds(radius_in_days)
        # chose window orientation
    elif backend == "pandas":
        # radius_ = pd.to_timedelta(radius_in_days, unit="d")
        radius_ = radius_in_days
    if window_orientation == WINDOW_CENTER_LABEL:
        window_start = -radius_ / 2
        window_end = radius_ / 2
    elif window_orientation == WINDOW_BACKWARD_LABEL:
        window_start = -radius_
        window_end = 0
    else:
        raise ValueError(
            f"Choose window_orientation in {[WINDOW_CENTER_LABEL, WINDOW_BACKWARD_LABEL]}"
        )
    if backend == "spark":
        window_start = int(window_start)
        window_end = int(window_end)
    return window_start, window_end


@dataclass
class EventCohort:
    person: pd.DataFrame
    event: pd.DataFrame


DataFrameType = Union[pd.DataFrame, pl.DataFrame, pl.LazyFrame]


def get_embeddings_from_url(embedding_url):
    """Get the embedding from a url.
    The url should point to a parquet file with concept as columns and embedding
    as rows.

    Args:
        embedding_url (str): _description_

    Returns:
        _type_: _description_
    """
    embeddings = pd.read_parquet(embedding_url)
    return embeddings


def to_pandas(df: DataFrameType) -> pd.DataFrame:
    """Convert a polars dataframe to a pandas dataframe.

    Args:
        df (Union[pl.LazyFrame, pl.DataFrame]): _description_

    Returns:
        pd.DataFrame: _description_
    """
    if isinstance(df, pl.LazyFrame):
        df = df.collect().to_pandas()
    elif isinstance(df, pl.DataFrame):
        df = df.to_pandas()
    elif isinstance(df, pd.DataFrame):
        pass
    else:
        raise ValueError(
            f"df must be a polars dataframe or a pandas dataframe, got {type(df)} instead"
        )
    return df


def to_polars(df: DataFrameType) -> pl.DataFrame:
    """Convert a pandas dataframe to a polars dataframe.

    Args:
        df (Union[pl.LazyFrame, pl.DataFrame]): _description_

    Returns:
        pl.DataFrame: _description_
    """
    if isinstance(df, pl.LazyFrame):
        df = df.collect()
    elif isinstance(df, pl.DataFrame):
        pass
    elif isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)
    else:
        raise ValueError(
            f"df must be a polars dataframe or a pandas dataframe, got {type(df)} instead"
        )
    return df


def to_lazyframe(df: DataFrameType) -> pl.LazyFrame:
    """Convert a pandas dataframe to a polars dataframe.

     Args:
        df (Union[pl.LazyFrame, pl.DataFrame, pd.DataFrame]): _description_

    Returns:
        pl.DataFrame: _description_
    """
    if isinstance(df, pl.LazyFrame):
        pass
    else:
        df = to_polars(df).lazy()
    return df


def to(df: DataFrameType, backend: type) -> DataFrameType:
    if backend == pl.LazyFrame:
        return to_lazyframe(df)
    elif backend == pl.DataFrame:
        return to_polars(df)
    elif backend == pd.DataFrame:
        return to_pandas(df)
    else:
        raise ValueError(
            f"backend must be one of {[pl.LazyFrame, pl.DataFrame, pd.DataFrame]}, got {backend} instead"
        )


def check_colnames_subset(colnames_subset: List[str], colnames: List[str]):
    if colnames_subset is None:
        return True
    intersect_columns = set(colnames_subset).intersection(colnames)
    return intersect_columns == set(colnames_subset)
