import numpy as np

from .utils import rolling_window


class SingularSpectrumAnalysis:
    """Singular Spectrum Analysis (SSA).

    A decomposition method that splits time series into several
    components. Each of them has meaningful interpretation,
    including noise or residuals. SSA relates to the spectrum of
    eigenvalues in singular value decomposition of a covariance matrix.

    Parameters
    ----------
    window_size : int or float (default=10)
        Size of the sliding window. If float, it represents
        the percentage of the size of each time series and must be
        between 0 and 1. The window size will be computed as
        ``max(2, ceil(window_size * n_timestamps))``.

    References
    ----------
    .. [1] N. Golyandina, and A. Zhigljavsky.
            "Singular Spectrum Analysis for Time Series."
            Springer-Verlag Berlin Heidelberg (2013).
    .. [2] Donoho, David L., and Matan Gavish.
            "The optimal hard threshold for singular values is 4/√ 3."
            arXiv preprint arXiv:1305.5870 4 (2013).
    .. [3] Johann Faouzi and Hicham Janati.
            "pyts: A python package for time series classification."
            Journal of Machine Learning Research, 21(46):1−6, 2020.
    """

    def __init__(
        self,
        window_size: int,
    ) -> None:
        self._window_size = window_size

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform data using SSA to extract noise or residuals.

        Parameters
        ----------
        data : pandas Series or DataFrame, shape = (n_timestamps, n_series)
            Input data.

        Returns
        -------
        X_noise : np.ndarray, shape = (n_timestamp, n_series)
            Extracted noise.
        """
        # TODO: Set batch computation
        n_series, n_timestamps = X.shape
        n_windows = int(n_timestamps - self._window_size + 1)
        # 1. Constructing trajectory matrix
        X_window = np.transpose(
            rolling_window(X, n_series, n_timestamps, self._window_size),
            axes=(0, 2, 1),
        ).copy()
        X_tranpose = np.matmul(X_window, np.transpose(X_window, axes=(0, 2, 1)))
        # 2. Decomposing trajectory covariance matrix
        w, v = np.linalg.eigh(X_tranpose)
        w, v = w[:, ::-1], v[:, :, ::-1]
        # 3. Constructing element matrices for potential signal only
        r = self._rank_calculation(w)
        X_elem = self._outer_dot(v, X_window, n_series, n_windows, r)
        if self._window_size >= n_windows:
            X_elem = np.transpose(X_elem, axes=(0, 2, 1))
            gap = self._window_size
        else:
            gap = n_windows
        # 4. Reconstructing time series (signal & noise)
        X_signal = self._diagonal_averaging(
            X_elem, n_series, n_timestamps, n_windows, gap
        )
        X_noise = X - X_signal
        return X_noise.T

    def _rank_calculation(self, w: np.ndarray, threshold: float = 2.858) -> np.ndarray:
        """
        Define the trajectory matrix ranks as a threshold
            for splitting signal and noise.

        Parameters
        ----------
        w : np.ndarray
            The eigenvalues.
        threshold : float
            The hard limit to determine the rank of trajectory matrices
            (default=2.858).

        Returns
        -------
        ranks : np.ndarray
            The rank of trajectory matrices.
        """
        rank = (w > 0).sum(axis=1)
        ranks = np.array(
            [
                (w[i, :r] >= np.median(w[i, :r]) * threshold).sum()
                for i, r in enumerate(rank)
            ]
        )
        return ranks

    def _outer_dot(
        self,
        v: np.ndarray,
        X: np.ndarray,
        n_series: int,
        n_windows: int,
        r: np.ndarray,
    ) -> np.ndarray:
        """
        Perform outer dot to construct element matrices
            for potential signal only.

        Parameters
        ----------
        v : np.ndarray
            The eigenvectors.
        X : np.ndarray
            The trajectory matrices.
        n_series : int
            Number of time series (metrics).
        n_windows : int
            The number of rows of the trajectory matrix.
        r : np.ndarray
            The rank of trajectory matrices.

        Returns
        -------
        X_new : np.ndarray
            The element matrices.
        """
        X_new = np.empty(shape=(n_series, self._window_size, n_windows))
        for i in range(n_series):
            rank = int(r[i])
            X_reduced = np.empty(shape=(rank, self._window_size, n_windows))
            for j in range(rank):
                X_reduced[j] = np.dot(np.outer(v[i, :, j], v[i, :, j]), X[i])
            X_new[i] = X_reduced.sum(axis=0)
        return X_new

    def _diagonal_averaging(
        self,
        X: np.ndarray,
        n_series: int,
        n_timestamps: int,
        n_windows: int,
        gap: int,
    ) -> np.ndarray:
        """
        Reconstruct the element matrices into time series.

        Parameters
        ----------
        X : np.ndarray
            The element matrices.
        n_metrics : int
            Number of time series (metrics).
        n_timestamps : int
            The length of time variable in the input data.
        n_windows : int
            The number of rows of the trajectory matrix.
        gap : int
            Either n_windows OR window_size.

        Returns
        -------
        X_new : np.ndarray
            The new time series (reflect signal only, no noise).
        """
        X_new = np.empty(shape=(n_series, n_timestamps))
        first_row = [(0, col) for col in range(n_windows)]
        last_col = [(row, n_windows - 1) for row in range(1, self._window_size)]
        indices = first_row + last_col
        for i in range(n_series):
            for j, k in indices:
                X_new[i, j + k] = np.diag(X[i, :, ::-1], gap - j - k - 1).mean()
        return X_new
