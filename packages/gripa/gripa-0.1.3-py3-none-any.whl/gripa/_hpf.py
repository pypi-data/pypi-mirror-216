import numpy as np

from .utils import rolling_window


class HighPassFilter:
    """High-Pass (HP) Filter.

    A filtering method that separates the high-frequency noise
    or residuals from time series. Inter-quartile range (IQR) mean
    is utilised to get the low-frequency signals (smoothed time series).

    Parameters
    ----------
    window_size : int or float (default=13)
        Size of the sliding window. If float, it represents
        the percentage of the size of each time series and must be
        between 0 and 1. The window size will be computed as
        ``max(2, ceil(window_size * n_timestamps))``.

    References
    ----------
    .. [1] Lee Redner.
            "A note on the use of nonlinear filtering in computer graphics"
            IEEE Computer Graphics and Applications, 10(3), pp. 23-29.
    """

    def __init__(
        self,
        window_size: int,
    ) -> None:
        self._window_size = window_size

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform data using HP filter to extract noise or residuals.

        Parameters
        ----------
        data : pandas Series or DataFrame, shape = (n_timestamps, n_metrics)
            Input data.

        Returns
        -------
        X_noise : np.ndarray, shape = (n_timestamp, n_metrics)
            Extracted noise.
        """
        # 1. Constructing trajectory matrix
        n_series, n_timestamps = X.shape
        X_middle = rolling_window(X, n_series, n_timestamps, self._window_size).copy()
        # 2. Filling the starting & ending boundary
        n_top = int(np.ceil((self._window_size - 1) / 2))
        X_top = self._fix_starting_boundary(X, n_top)
        n_bottom = int(self._window_size - n_top - 1)
        X_bottom = self._fix_ending_boundary(X, n_bottom)
        # 3. Compiling the final signal
        X_window = np.concatenate((X_top, X_middle, X_bottom), axis=1)
        # 4. Calculating IQR mean
        median_id = self._window_size // 2
        q1_id = median_id // 2
        q3_id = median_id + (self._window_size - median_id) // 2
        X_window = np.sort(X_window, axis=2)
        X_signal = X_window[:, :, q1_id : q3_id + 1].mean(axis=2)
        X_noise = X - X_signal
        return X_noise.T

    def _fix_starting_boundary(
        self,
        X: np.ndarray,
        n_top: int,
    ) -> np.ndarray:
        """
        Fill the gap in the beginning of time series.

        Parameters
        ----------
        data : pandas Series or DataFrame, shape = (n_timestamps, n_series)
            Input data.
        n_top : int
            Number of gap in the starting time series.

        Returns
        -------
        X : np.ndarray
            Rolling-window matrices to fill the gap in the starting points.
        """
        n_series, _ = X.shape
        indices = np.array(range(self._window_size))
        n = self._window_size + n_top - 1
        extension = np.zeros(shape=(n_series, n), dtype=float)
        extension[:, n_top:] = X[:, indices[: self._window_size - 1]]
        extension[:, 0:n_top] = X[:, indices[n_top:0:-1]]
        X_top = rolling_window(extension, n_series, n, self._window_size).copy()
        return X_top

    def _fix_ending_boundary(
        self,
        X: np.ndarray,
        n_bottom: int,
    ) -> np.ndarray:
        """
        #TODO: change from pandas to numpy
        Fill the gap in the ending of time series.

        Parameters
        ----------
        data : pandas Series or DataFrame, shape = (n_timestamps, n_series)
            Input data.
        n_top : int
            Number of gap in the ending time series.

        Returns
        -------
        X : np.ndarray
            Rolling-window matrices to fill the gap in the ending points.
        """
        n_series, n_timestamps = X.shape
        indices = np.array(range(n_timestamps - self._window_size, n_timestamps))
        n = self._window_size + n_bottom - 1
        extension = np.zeros((n_series, n), float)
        extension[:, :-n_bottom] = X[:, indices[-(self._window_size - 1) :]]
        extension[:, -n_bottom:] = X[:, indices[-2 : -2 - n_bottom : -1]]
        X_bottom = rolling_window(extension, n_series, n, self._window_size).copy()
        return X_bottom
