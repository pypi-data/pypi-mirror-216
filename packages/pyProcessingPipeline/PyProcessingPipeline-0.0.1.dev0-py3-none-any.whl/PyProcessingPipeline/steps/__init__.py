"""
Processing Steps
================

Steps are the building block of the processing package.
Every step implements a specific data manipulation step,
like filtering, cutting, averaging, and many more.

Steps, together with the ProcessingRun, can make it easier
to create and share scripts for data processing.

E.g. to filter a signal and cut off the begining and end,
you would simply create a run that contains the right steps

>>> from PyProcessingPipeline import ProcessingRun
>>> import PyProcessingPipeline.steps as prs
>>> import numpy as np
>>> signal = np.sin(np.linspace(0, 2*np.pi, 100))
>>> pr = ProcessingRun(
...     name="ExampleRun",
...     description="Run that does some things :)",
... )
>>> pr.add_step(
...     prs.filters.butterworth.LowpassButter(
...         cutoff_frequency=1.5,
...         filter_order=3,
...         sampling_frequency=125,
...     )
... )
>>> pr.add_step(
...     prs.misc.Cut(
...         global_lower_bound=10,
...         global_upper_bound=90
...     )
... )
>>> pr.run([signal])

Modules
--------
filters
    Contains filters for filtering a signal.
misc
    Contains miscellaneous functions, like cutting, uniting...
preprocessing
    Contains steps specifically made for preprocessing, like Baseline removal
"""
from . import filters, misc, preprocessing

__all__ = ["filters", "misc", "preprocessing"]
