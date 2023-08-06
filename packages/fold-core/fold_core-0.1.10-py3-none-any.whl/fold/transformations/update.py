# Copyright (c) 2022 - Present Myalo UG (haftungbeschränkt) (Mark Aron Szulyovszky, Daniel Szemerey) <info@dreamfaster.ai>. All rights reserved. See LICENSE in root folder.


from typing import Optional, Tuple

import pandas as pd

from ..base import Artifact, Transformation, fit_noop


class DontUpdate(Transformation):
    properties = Transformation.Properties(requires_X=False)

    def __init__(self, transformation: Transformation) -> None:
        self.transformation = transformation
        self.name = f"DontUpdate-{transformation.name}"

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        sample_weights: Optional[pd.Series] = None,
    ) -> Optional[Artifact]:
        self.transformation.fit(X, y, sample_weights)

    def transform(
        self, X: pd.DataFrame, in_sample: bool
    ) -> Tuple[pd.DataFrame, Optional[Artifact]]:
        return self.transformation.transform(X, in_sample), None

    update = fit_noop
