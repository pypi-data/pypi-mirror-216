# Copyright (c) 2022 - Present Myalo UG (haftungbeschränkt) (Mark Aron Szulyovszky, Daniel Szemerey) <info@dreamfaster.ai>. All rights reserved. See LICENSE in root folder.


from typing import List, Optional, Tuple, Union

import pandas as pd

from fold.utils.checks import is_X_available

from ..base import Artifact, Transformation, Tunable, fit_noop
from ..utils.list import flatten, transform_range_to_list, wrap_in_list


class AddLagsY(Transformation, Tunable):
    """
    Adds past values of `y`.

    Parameters
    ----------
    lags : List[int], range
        A list of lags (of the target) to add as features.

    Examples
    --------
    ```pycon
    >>> from fold.loop import train_backtest
    >>> from fold.splitters import SlidingWindowSplitter
    >>> from fold.transformations import AddLagsY
    >>> from fold.utils.tests import generate_sine_wave_data
    >>> _, y  = generate_sine_wave_data()
    >>> splitter = SlidingWindowSplitter(train_window=0.5, step=0.2)
    >>> pipeline = AddLagsY([1,2,3])
    >>> preds, trained_pipeline = train_backtest(pipeline, None, y, splitter)
    >>> preds.head()
                         y_lag_1  y_lag_2  y_lag_3
    2021-12-31 15:40:00  -0.0000  -0.0126  -0.0251
    2021-12-31 15:41:00   0.0126  -0.0000  -0.0126
    2021-12-31 15:42:00   0.0251   0.0126  -0.0000
    2021-12-31 15:43:00   0.0377   0.0251   0.0126
    2021-12-31 15:44:00   0.0502   0.0377   0.0251

    ```
    """

    def __init__(
        self,
        lags: Union[List[int], range],
        name: Optional[str] = None,
        params_to_try: Optional[dict] = None,
    ) -> None:
        if not isinstance(lags, range) and not isinstance(lags, List):
            raise ValueError("lags must be a range or a List")
        self.lags = sorted(transform_range_to_list(lags))
        self.properties = Transformation.Properties(
            requires_X=False,
            mode=Transformation.Properties.Mode.online,
            memory_size=max(self.lags),
            _internal_supports_minibatch_backtesting=True,
        )
        self.params_to_try = params_to_try
        self.name = name or f"AddLagsY-{self.lags}"

    def transform(
        self, X: pd.DataFrame, in_sample: bool
    ) -> Tuple[pd.DataFrame, Optional[Artifact]]:
        lags = pd.DataFrame([], index=X.index)

        past_y = (
            self._state.memory_y if in_sample else self._state.memory_y.reindex(X.index)
        )
        lags = pd.concat(
            [past_y.shift(lag)[-len(X) :].rename(f"y_lag_{lag}") for lag in self.lags],
            axis="columns",
        ).fillna(0.0)
        if is_X_available(X):
            return pd.concat([X, lags], axis="columns"), None
        else:
            # If X is just an DataFrame with zeros, then just return the lags
            return lags, None

    fit = fit_noop
    update = fit_noop


class AddLagsX(Transformation, Tunable):
    """
    Adds past values of `X` for the desired column(s).

    Parameters
    ----------
    columns_and_lags : List[ColumnAndLag], ColumnAndLag
        A tuple (or a list of tuples) of the column name and a single or a list of lags to add as features.

    Examples
    --------
    ```pycon
    >>> from fold.loop import train_backtest
    >>> from fold.splitters import SlidingWindowSplitter
    >>> from fold.transformations import AddLagsX
    >>> from fold.utils.tests import generate_sine_wave_data
    >>> X, y  = generate_sine_wave_data()
    >>> splitter = SlidingWindowSplitter(train_window=0.5, step=0.2)
    >>> pipeline = AddLagsX([("sine", 1), ("sine", [2,3])])
    >>> preds, trained_pipeline = train_backtest(pipeline, X, y, splitter)
    >>> preds.head()
                           sine  sine_lag_1  sine_lag_2  sine_lag_3
    2021-12-31 15:40:00 -0.0000     -0.0126     -0.0251     -0.0377
    2021-12-31 15:41:00  0.0126     -0.0000     -0.0126     -0.0251
    2021-12-31 15:42:00  0.0251      0.0126     -0.0000     -0.0126
    2021-12-31 15:43:00  0.0377      0.0251      0.0126     -0.0000
    2021-12-31 15:44:00  0.0502      0.0377      0.0251      0.0126

    ```
    """

    ColumnAndLag = Tuple[str, Union[int, List[int]]]

    def __init__(
        self,
        columns_and_lags: Union[List[ColumnAndLag], ColumnAndLag],
        name: Optional[str] = None,
        params_to_try: Optional[dict] = None,
    ) -> None:
        self.columns_and_lags = wrap_in_list(columns_and_lags)
        self.params_to_try = params_to_try

        def check_and_transform_if_needed(
            column_and_lag: AddLagsX.ColumnAndLag,
        ) -> AddLagsX.ColumnAndLag:
            column, lags = column_and_lag
            if (
                not isinstance(lags, int)
                and not isinstance(lags, List)
                and not isinstance(lags, range)
            ):
                raise ValueError("lags must be an int or a List or a range")
            lags = sorted(
                transform_range_to_list([lags] if isinstance(lags, int) else lags)
            )
            return column, lags

        self.columns_and_lags = list(
            map(check_and_transform_if_needed, self.columns_and_lags)
        )
        self.properties = Transformation.Properties(
            requires_X=True,
            memory_size=max(flatten([l for _, l in self.columns_and_lags])),
        )
        self.name = name or f"AddLagsX-{self.columns_and_lags}"

    def transform(
        self, X: pd.DataFrame, in_sample: bool
    ) -> Tuple[pd.DataFrame, Optional[Artifact]]:
        lagged_columns = []
        for column, lags in self.columns_and_lags:
            for lag in lags:
                selected = X if column == "all" else X[column].to_frame()
                lagged_columns.append(
                    selected.shift(lag)[-len(X) :].add_suffix(f"_lag_{lag}")
                )
        return pd.concat([X] + lagged_columns, axis="columns").fillna(0.0), None

    fit = fit_noop
    update = fit_noop
