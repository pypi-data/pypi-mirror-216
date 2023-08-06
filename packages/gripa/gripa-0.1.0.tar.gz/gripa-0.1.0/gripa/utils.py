import numpy as np
from numpy.lib.stride_tricks import as_strided


def rolling_window(
    X: np.ndarray,
    n_series: int,
    n_timestamps: int,
    window_size: int,
    rolling_step: int = 1,
) -> np.ndarray:
    """ """
    overlap = window_size - rolling_step
    shape_new = (
        n_series,
        (n_timestamps - overlap) // rolling_step,
        window_size // 1,
    )
    s0, s1 = X.strides
    strides_new = (s0, rolling_step * s1, s1)
    return as_strided(X, shape=shape_new, strides=strides_new)
