# Welcome to Gripa


## Introduction

Gripa is a python package for time series anomaly detection. The name of Gripa is taken from Scandinavian languages, which means grab or catch or seize, and not meant as Flu in Spanish :smile:.

### Why Gripa?

* **Gripa is light-weight.** Try Gripa before you build LSTM or Transformer for your time series anomaly detection.
* **Gripa is accurate.** Gripa has two available algorithms that perform very well in detecting anomalies on your time series data.
* **Gripa is comprehensive.** Gripa can detect three types of anomaly: global anomaly, contextual anomaly, and level-shift.

## Quick Start

### Installation

> **`Python 3.9`** or higher is required.

```sh
python -m pip install gripa
```

### Usage

```sh
# Load data
from gripa import Gripa

detector = Gripa()
anomalies = Gripa.fit_predict(data)
```

## API Reference

There is only one module, `gripa.Gripa`, that can be used for detecting anomalies in time series.

> *class* gripa.**Gripa**(*window_size=11, algorithm="hpf", threshold=3*)

### Parameters
* `window_size`: *int or float, default=11*
* `algorithm`: *{"hpf", "ssa"}, default="hpf"*
* `threshold`: *float, default=3*

### Attributes
* `anomaly_score`: score for labelling anomaly

### Methods
* `fit(X)`: train the Gripa model, which can generate attribute `anomaly_score`
* `fit_predict(X)`: train and generate anomaly labels (`True` or `False`)

## Contact

Hamid Dimyati - <hamid.dimyati@outlook.com>
