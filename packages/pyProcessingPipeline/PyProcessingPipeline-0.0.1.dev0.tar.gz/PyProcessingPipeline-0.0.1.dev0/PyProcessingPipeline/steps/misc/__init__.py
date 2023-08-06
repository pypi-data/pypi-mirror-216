"""
Misc Steps
==========

Contains misc steps for e.g. manipulating a series' length.

Classes
-------
Average
    Averages multiple timeseries into a single one
Cut
    Cuts the beginning and end off of a timeseries
Split
    Splits a single timeseries into multiple smaller subseries
Unite
    Unites multiple series into a larger series.
    Can be seen as the inverse of Split.
"""
from ._cut import Cut
from ._split import Split
from ._statistics import Average
from ._unite import Unite

__all__ = ["Average", "Cut", "Split", "Unite"]
