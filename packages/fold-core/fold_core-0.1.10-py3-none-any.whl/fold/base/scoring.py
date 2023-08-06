import importlib
from typing import Optional, Tuple

import pandas as pd

from ..utils.checks import (
    all_have_probabilities,
    get_prediction_column,
    get_probabilities_columns,
)
from ..utils.enums import ParsableEnum
from .classes import Artifact


class ScoreOn(ParsableEnum):
    predictions = "predictions"
    probabilities = "probabilities"


def score_results(
    result: pd.DataFrame,
    y: pd.Series,
    artifacts: Artifact,
    krisi_args: Optional[dict] = None,
):
    y, pred_point, probabilities, test_sample_weights = align_result_with_events(
        y=y,
        result=result,
        artifacts=artifacts,
    )
    if importlib.util.find_spec("krisi") is not None:
        from krisi import score

        return score(
            y=y,
            predictions=pred_point,
            probabilities=probabilities,
            sample_weight=test_sample_weights
            if test_sample_weights is not None
            else None,
            **(krisi_args if krisi_args is not None else {}),
        )
    else:
        raise ImportError(
            "krisi not installed. Please install krisi to use this function."
        )


def align_result_with_events(
    y: pd.Series,
    result: pd.DataFrame,
    artifacts: Artifact,
) -> Tuple[pd.Series, pd.Series, Optional[pd.DataFrame], Optional[pd.Series]]:
    events = Artifact.get_events(artifacts)
    test_sample_weights = Artifact.get_test_sample_weights(artifacts)

    probabilities = (
        get_probabilities_columns(result) if all_have_probabilities([result]) else None
    )
    pred_point = get_prediction_column(result)

    if events is not None:
        events = events.reindex(result.index).dropna()
        y = events.event_label
        test_sample_weights = events.event_test_sample_weights
        pred_point = pred_point.dropna()
        probabilities = probabilities.dropna() if probabilities is not None else None
        y = y[pred_point.index]
    else:
        test_sample_weights = (
            test_sample_weights[pred_point.index]
            if test_sample_weights is not None
            else None
        )
        y = y[pred_point.index]

    return y, pred_point, probabilities, test_sample_weights
