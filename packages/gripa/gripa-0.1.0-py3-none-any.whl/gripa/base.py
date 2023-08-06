from abc import ABC, abstractmethod
from typing import Optional, Union

import pandas as pd


class BaseDetector(ABC):
    """ """

    def __init__(
        self,
        threshold: float = 3.0,
    ) -> None:
        super().__init__()
        self._threshold: float = threshold
        self.anomaly_score: Optional[Union[pd.DataFrame, pd.Series]] = None

    def fit_predict(
        self, data: Union[pd.DataFrame, pd.Series]
    ) -> Union[pd.DataFrame, pd.Series]:
        """ """
        self.fit(data)
        if self.anomaly_score is not None:
            return self.anomaly_score > self._threshold
        else:
            raise ValueError('The algorithm failed to produce anomaly scores.')

    @abstractmethod
    def fit(self, data: Union[pd.DataFrame, pd.Series]) -> "BaseDetector":
        return self
