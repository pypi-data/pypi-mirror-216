# Copyright (c) 2022 - Present Myalo UG (haftungbeschränkt) (Mark Aron Szulyovszky, Daniel Szemerey) <info@dreamfaster.ai>. All rights reserved. See LICENSE in root folder.


from __future__ import annotations

from typing import Callable, List, Optional, Union

import pandas as pd

from fold.base.classes import Artifact

from ..base import Composite, Pipelines, Transformations, get_concatenated_names
from ..transformations.columns import SelectColumns
from ..transformations.dev import Identity
from ..utils.dataframe import ResolutionStrategy, concat_on_columns_with_duplicates
from ..utils.list import wrap_in_double_list_if_needed, wrap_in_list


class Concat(Composite):
    """
    Concatenates the results of multiple pipelines.

    Parameters
    ----------

    pipelines : Pipelines
        A list of pipelines to be applied to the data, independently of each other.
    if_duplicate_keep : Union[ResolutionStrategy, str], optional
        How to handle duplicate columns, by default ResolutionStrategy.first

    Examples
    --------
        >>> from fold.loop import train_backtest
        >>> from fold.splitters import SlidingWindowSplitter
        >>> from fold.composites import Concat
        >>> from fold.utils.tests import generate_sine_wave_data
        >>> X, y  = generate_sine_wave_data()
        >>> splitter = SlidingWindowSplitter(train_window=0.5, step=0.2)
        >>> pipeline = Concat([
        ...     lambda X: X.assign(sine_plus_1=X["sine"] + 1),
        ...     lambda X: X.assign(sine_plus_2=X["sine"] + 2),
        ... ])
        >>> preds, trained_pipeline = train_backtest(pipeline, X, y, splitter)
        >>> preds.head()
                             sine_plus_1  sine_plus_2    sine
        2021-12-31 15:40:00       1.0000       2.0000 -0.0000
        2021-12-31 15:41:00       1.0126       2.0126  0.0126
        2021-12-31 15:42:00       1.0251       2.0251  0.0251
        2021-12-31 15:43:00       1.0377       2.0377  0.0377
        2021-12-31 15:44:00       1.0502       2.0502  0.0502
    """

    ResolutionStrategy = ResolutionStrategy
    properties = Composite.Properties()

    def __init__(
        self,
        pipelines: Pipelines,
        if_duplicate_keep: Union[ResolutionStrategy, str] = ResolutionStrategy.first,
        name: Optional[str] = None,
    ) -> None:
        self.pipelines = pipelines
        self.if_duplicate_keep = ResolutionStrategy.from_str(if_duplicate_keep)
        self.name = name or "Concat-" + get_concatenated_names(pipelines)

    def postprocess_result_primary(
        self, results: List[pd.DataFrame], y: Optional[pd.Series]
    ) -> pd.DataFrame:
        return concat_on_columns_with_duplicates(results, self.if_duplicate_keep)

    def postprocess_artifacts_primary(
        self,
        primary_artifacts: List[Artifact],
        results: List[pd.DataFrame],
        original_artifact: Artifact,
        fit: bool,
    ) -> pd.DataFrame:
        return concat_on_columns_with_duplicates(
            primary_artifacts, self.if_duplicate_keep
        )

    def get_children_primary(self) -> Pipelines:
        return self.pipelines

    def clone(self, clone_children: Callable) -> Concat:
        clone = Concat(
            pipelines=clone_children(self.pipelines),
            if_duplicate_keep=self.if_duplicate_keep,
        )
        clone.properties = self.properties
        clone.name = self.name
        return clone


class Pipeline(Composite):
    """
    An optional wrappers that is equivalent to using a single array for the transformations.
    It executes the transformations sequentially, in the order they are provided.

    Parameters
    ----------

    pipeline : Pipeline
        A list of transformations or models to be applied to the data.

    """

    properties = Composite.Properties(primary_only_single_pipeline=True)

    def __init__(self, pipeline: Pipeline, name: Optional[str] = None) -> None:
        self.pipeline = wrap_in_double_list_if_needed(pipeline)
        self.name = name or "Pipeline-" + get_concatenated_names(pipeline)

    def postprocess_result_primary(
        self, results: List[pd.DataFrame], y: Optional[pd.Series]
    ) -> pd.DataFrame:
        return results[0]

    def get_children_primary(self) -> Pipelines:
        return self.pipeline

    def clone(self, clone_children: Callable) -> Pipeline:
        clone = Pipeline(pipeline=clone_children(self.pipeline))
        clone.properties = self.properties
        clone.name = self.name
        return clone


def TransformColumn(
    columns: Union[List[str], str],
    pipeline: Transformations,
    name: Optional[str] = None,
) -> Composite:
    """
    Transforms a single or multiple columns using the given pipeline.
    """
    return Concat(
        [
            [SelectColumns(columns)] + wrap_in_list(pipeline),
            Identity(),
        ],
        if_duplicate_keep=ResolutionStrategy.first,
        name=name,
    )
