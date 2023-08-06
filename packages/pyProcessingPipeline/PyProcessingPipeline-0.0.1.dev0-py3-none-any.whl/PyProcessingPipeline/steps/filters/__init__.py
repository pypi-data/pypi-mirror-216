"""
Filters
=======

Contains different filter implementations as ProcessingSteps.
Filters are grouped by their type.

Modules
--------
bessel
    Filter implementations based on Bessel filters.
butterworth
    Filter implementations based on Butterworth filters.
chebyshev
    Filter implementations based on Chebyshev filters.
fir
    Finite-impulse-response filters
"""
from . import bessel, butterworth, chebyshev, fir

__all__ = ["bessel", "butterworth", "chebyshev", "fir"]
