"""
Preprocessing
=============

ProcessingSteps for preprocessing.
This includes tasks like removal of baselines, averaging signals
or normalization.

Modules
-------
averaging
    Steps for averaging signals.
baseline_correction
    Steps for removing a signals baseline.
normalization
    Steps for normalizing timeseries.
"""
from . import averaging, baseline_correction, normalization

__all__ = ["averaging", "baseline_correction", "normalization"]
