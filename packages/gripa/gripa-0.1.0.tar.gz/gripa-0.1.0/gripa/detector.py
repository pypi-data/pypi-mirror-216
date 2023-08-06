from math import ceil
from typing import Optional, Union

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_array

from ._hpf import HighPassFilter
from ._ssa import SingularSpectrumAnalysis
from .base import BaseDetector


class Gripa(BaseEstimator, BaseDetector):
    """ """

    def __init__(
        self, window_size: Union[int, float] = 11, algorithm: str = 'hpf', **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._window_size: Union[int, float] = window_size
        self._window_size_int: Optional[int] = None
        self._algorithm: str = algorithm

    def fit(self, data: Union[pd.DataFrame, pd.Series]) -> "BaseDetector":
        """ """
        self.validate_input_type(data)
        if data.isnull().values.any():  # type: ignore
            raise ValueError("Data contains missing values. Please handle it properly.")
        else:
            pass
        if isinstance(data, pd.Series):
            df = data.copy().to_frame()
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        n_timestamps = df.shape[0]
        self._window_size_int = self.validate_params(
            self._algorithm, self._window_size, n_timestamps
        )
        X = df.to_numpy().T
        X = check_array(X, dtype='float64')
        if self._algorithm == 'hpf':
            X_noise = HighPassFilter(self._window_size_int).transform(X)
        elif self._algorithm == 'ssa':
            X_noise = SingularSpectrumAnalysis(self._window_size_int).transform(X)
        self.anomaly_score = np.abs(stats.zscore(X_noise))
        if self.anomaly_score is not None:
            if isinstance(data, pd.DataFrame):
                self.anomaly_score = pd.DataFrame(
                    self.anomaly_score, index=data.index, columns=data.columns
                )
            elif isinstance(data, pd.Series):
                self.anomaly_score = pd.Series(
                    self.anomaly_score.ravel(),  # type: ignore
                    index=data.index,
                    name=data.name,
                )
        else:
            raise ValueError('The algorithm failed to produce anomaly scores.')
        return self

    @staticmethod
    def validate_input_type(data: Union[pd.DataFrame, pd.Series]) -> None:
        """ """
        if not isinstance(data, (pd.DataFrame, pd.Series)):
            raise TypeError('Input data must be pandas Series or DataFrame.')
        else:
            pass

    @staticmethod
    def validate_params(
        algorithm: str, window_size: Union[int, float], n_timestamps: int
    ) -> int:
        """ """
        if algorithm not in ['hpf', 'ssa']:
            raise ValueError('Parameter "algorithm" should be "hpf" or "ssa".')
        if not isinstance(window_size, (int, np.integer, float, np.floating)):
            raise TypeError('Parameter "window_size" should be integer or float.')
        if isinstance(window_size, (int, np.integer)):
            if not 2 <= window_size <= n_timestamps:
                raise ValueError(
                    'If "window_size" is an integer, it must be greater '
                    'than or equal to 2 and lower than or equal to '
                    'n_timestamps (got {}).'.format(window_size)
                )
            else:
                final_window_size = window_size
        else:
            if not 0 < window_size <= 1:
                raise ValueError(
                    'If "window_size" is a float, it must be greater '
                    'than 0 and lower than or equal to 1 '
                    '(got {}).'.format(window_size)
                )
            else:
                final_window_size = int(max(2, ceil(window_size * n_timestamps)))
        return final_window_size
