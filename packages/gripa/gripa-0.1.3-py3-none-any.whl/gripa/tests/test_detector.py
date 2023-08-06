import random

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from ..detector import Gripa

random.seed(10)


@pytest.fixture(scope="module")
def anomalous_frame_in():
    N = 40
    data1 = np.random.rand(N)
    data1[10] *= 10e3
    data2 = np.random.rand(N)
    data2[20] *= 10e3
    data3 = np.random.rand(N)
    data3[30] *= 10e3
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    frame = pd.DataFrame(
        {"metric1": data1, "metric2": data2, "metric3": data3}, index=t
    )
    return frame


@pytest.fixture(scope="module")
def anomalous_frame_out():
    N = 40
    data1 = [False] * N
    data1[10] = True
    data2 = [False] * N
    data2[20] = True
    data3 = [False] * N
    data3[30] = True
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    frame = pd.DataFrame(
        {"metric1": data1, "metric2": data2, "metric3": data3}, index=t
    )
    return frame


@pytest.fixture(scope="module")
def normal_frame_in():
    N = 40
    data1 = np.random.rand(N)
    data2 = np.random.rand(N)
    data3 = np.random.rand(N)
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    frame = pd.DataFrame(
        {"metric1": data1, "metric2": data2, "metric3": data3}, index=t
    )
    return frame


@pytest.fixture(scope="module")
def normal_frame_out():
    N = 40
    data1 = [False] * N
    data2 = [False] * N
    data3 = [False] * N
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    frame = pd.DataFrame(
        {"metric1": data1, "metric2": data2, "metric3": data3}, index=t
    )
    return frame


@pytest.fixture(scope="module")
def anomalous_series_in():
    N = 40
    data = np.random.rand(N)
    data[20] *= 10e3
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    series = pd.Series(data, name="metric1", index=t)
    return series


@pytest.fixture(scope="module")
def anomalous_series_out():
    N = 40
    data = [False] * N
    data[20] = True
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    series = pd.Series(data, name="metric1", index=t)
    return series


@pytest.fixture(scope="module")
def normal_series_in():
    N = 40
    data = np.random.rand(N)
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    series = pd.Series(data, name="metric1", index=t)
    return series


@pytest.fixture(scope="module")
def normal_series_out():
    N = 40
    data = [False] * N
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    series = pd.Series(data, name="metric1", index=t)
    return series


@pytest.fixture(scope="module")
def array_in():
    data = np.random.rand(40, 3)
    return data


@pytest.fixture(scope="module")
def missing_frame_in():
    N = 40
    data1 = np.random.rand(N)
    data1[10] = None
    data2 = np.random.rand(N)
    data2[20] = None
    data3 = np.random.rand(N)
    data3[30] = None
    t = pd.date_range('2022-01-01', periods=N, freq='15T')
    frame = pd.DataFrame(
        {"metric1": data1, "metric2": data2, "metric3": data3}, index=t
    )
    return frame


def test_anomalous_frame(
    anomalous_frame_in: pd.DataFrame, anomalous_frame_out: pd.DataFrame
) -> None:
    tsad_model = Gripa(algorithm='hpf')
    tsad_model.fit(anomalous_frame_in.copy())
    assert tsad_model.anomaly_score is not None
    assert tsad_model.anomaly_score.shape == anomalous_frame_in.shape
    assert all(tsad_model.anomaly_score.index == anomalous_frame_in.index)
    assert all(tsad_model.anomaly_score.columns == anomalous_frame_in.columns)
    anomalies = tsad_model.fit_predict(anomalous_frame_in.copy())
    assert anomalies is not None
    assert anomalies.shape == anomalous_frame_in.shape
    assert all(anomalies.index == anomalous_frame_in.index)
    assert all(anomalies.columns == anomalous_frame_in.columns)
    assert_frame_equal(
        anomalies,  # type: ignore
        anomalous_frame_out.copy(),
    )
    tsad_model = Gripa(algorithm='ssa')
    tsad_model.fit(anomalous_frame_in.copy())
    assert tsad_model.anomaly_score is not None
    assert tsad_model.anomaly_score.shape == anomalous_frame_in.shape
    assert all(tsad_model.anomaly_score.index == anomalous_frame_in.index)
    assert all(tsad_model.anomaly_score.columns == anomalous_frame_in.columns)
    anomalies = tsad_model.fit_predict(anomalous_frame_in.copy())
    assert anomalies is not None
    assert anomalies.shape == anomalous_frame_in.shape
    assert all(anomalies.index == anomalous_frame_in.index)
    assert all(anomalies.columns == anomalous_frame_in.columns)
    assert_frame_equal(
        anomalies,  # type: ignore
        anomalous_frame_out.copy(),
    )


def test_normal_frame(
    normal_frame_in: pd.DataFrame, normal_frame_out: pd.DataFrame
) -> None:
    tsad_model = Gripa(algorithm='hpf')
    tsad_model.fit(normal_frame_in.copy())
    assert tsad_model.anomaly_score is not None
    assert tsad_model.anomaly_score.shape == normal_frame_in.shape
    assert all(tsad_model.anomaly_score.index == normal_frame_in.index)
    assert all(tsad_model.anomaly_score.columns == normal_frame_in.columns)
    anomalies = tsad_model.fit_predict(normal_frame_in.copy())
    assert anomalies is not None
    assert anomalies.shape == normal_frame_in.shape
    assert all(anomalies.index == normal_frame_in.index)
    assert all(anomalies.columns == normal_frame_in.columns)
    assert_frame_equal(
        anomalies,  # type: ignore
        normal_frame_out.copy(),
    )
    tsad_model = Gripa(algorithm='ssa')
    tsad_model.fit(normal_frame_in.copy())
    assert tsad_model.anomaly_score is not None
    assert tsad_model.anomaly_score.shape == normal_frame_in.shape
    assert all(tsad_model.anomaly_score.index == normal_frame_in.index)
    assert all(tsad_model.anomaly_score.columns == normal_frame_in.columns)
    anomalies = tsad_model.fit_predict(normal_frame_in.copy())
    assert anomalies is not None
    assert anomalies.shape == normal_frame_in.shape
    assert all(anomalies.index == normal_frame_in.index)
    assert all(anomalies.columns == normal_frame_in.columns)
    assert_frame_equal(
        anomalies,  # type: ignore
        normal_frame_out.copy(),
    )


def test_anomalous_series(
    anomalous_series_in: pd.Series, anomalous_series_out: pd.Series
) -> None:
    tsad_model = Gripa(algorithm='hpf')
    tsad_model.fit(anomalous_series_in.copy())
    assert tsad_model.anomaly_score is not None
    assert tsad_model.anomaly_score.shape == anomalous_series_in.shape
    assert all(tsad_model.anomaly_score.index == anomalous_series_in.index)
    assert tsad_model.anomaly_score.name == anomalous_series_in.name
    anomalies = tsad_model.fit_predict(anomalous_series_in.copy())
    assert anomalies is not None
    assert anomalies.shape == anomalous_series_in.shape
    assert all(anomalies.index == anomalous_series_in.index)
    assert anomalies.name == anomalous_series_in.name
    assert_series_equal(
        anomalies,  # type: ignore
        anomalous_series_out.copy(),
    )
    tsad_model = Gripa(algorithm='ssa')
    tsad_model.fit(anomalous_series_in.copy())
    assert tsad_model.anomaly_score is not None
    assert tsad_model.anomaly_score.shape == anomalous_series_in.shape
    assert all(tsad_model.anomaly_score.index == anomalous_series_in.index)
    assert tsad_model.anomaly_score.name == anomalous_series_in.name
    anomalies = tsad_model.fit_predict(anomalous_series_in.copy())
    assert anomalies is not None
    assert anomalies.shape == anomalous_series_in.shape
    assert all(anomalies.index == anomalous_series_in.index)
    assert anomalies.name == anomalous_series_in.name
    assert_series_equal(
        anomalies,  # type: ignore
        anomalous_series_out.copy(),
    )


def test_normal_series(
    normal_series_in: pd.Series, normal_series_out: pd.Series
) -> None:
    tsad_model = Gripa(algorithm='hpf')
    tsad_model.fit(normal_series_in.copy())
    assert tsad_model.anomaly_score is not None
    assert tsad_model.anomaly_score.shape == normal_series_in.shape
    assert all(tsad_model.anomaly_score.index == normal_series_in.index)
    assert tsad_model.anomaly_score.name == normal_series_in.name
    anomalies = tsad_model.fit_predict(normal_series_in.copy())
    assert anomalies is not None
    assert anomalies.shape == normal_series_in.shape
    assert all(anomalies.index == normal_series_in.index)
    assert anomalies.name == normal_series_in.name
    assert_series_equal(
        anomalies,  # type: ignore
        normal_series_out.copy(),
    )
    tsad_model = Gripa(algorithm='ssa')
    tsad_model.fit(normal_series_in.copy())
    assert tsad_model.anomaly_score is not None
    assert tsad_model.anomaly_score.shape == normal_series_in.shape
    assert all(tsad_model.anomaly_score.index == normal_series_in.index)
    assert tsad_model.anomaly_score.name == normal_series_in.name
    anomalies = tsad_model.fit_predict(normal_series_in.copy())
    assert anomalies is not None
    assert anomalies.shape == normal_series_in.shape
    assert all(anomalies.index == normal_series_in.index)
    assert anomalies.name == normal_series_in.name
    assert_series_equal(
        anomalies,  # type: ignore
        normal_series_out.copy(),
    )


def test_input_type(array_in: np.ndarray) -> None:
    tsad_model = Gripa(algorithm='hpf')
    with pytest.raises(
        TypeError, match='Input data must be pandas Series or DataFrame.'
    ):
        tsad_model.fit(array_in.copy())  # type: ignore
    tsad_model = Gripa(algorithm='ssa')
    with pytest.raises(
        TypeError, match='Input data must be pandas Series or DataFrame.'
    ):
        tsad_model.fit(array_in.copy())  # type: ignore


def test_input_missing(missing_frame_in: pd.DataFrame) -> None:
    tsad_model = Gripa(algorithm='hpf')
    with pytest.raises(
        ValueError, match='Data contains missing values. Please handle it properly.'
    ):
        _ = tsad_model.fit_predict(missing_frame_in.copy())
    tsad_model = Gripa(algorithm='ssa')
    with pytest.raises(
        ValueError, match='Data contains missing values. Please handle it properly.'
    ):
        _ = tsad_model.fit_predict(missing_frame_in.copy())


def test_wrong_parameter(normal_series_in: pd.Series) -> None:
    tsad_model = Gripa(algorithm='random')
    with pytest.raises(
        ValueError, match='Parameter "algorithm" should be "hpf" or "ssa".'
    ):
        tsad_model.fit(normal_series_in)
    tsad_model = Gripa(window_size='random')  # type: ignore
    with pytest.raises(
        TypeError, match='Parameter "window_size" should be integer or float.'
    ):
        tsad_model.fit(normal_series_in)
