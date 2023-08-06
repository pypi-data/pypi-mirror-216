"""
Step Database Lookup
====================

Defines the names under which
every processing step is stored in the database.

This allows us to recreate previously stored runs
by knowing which step name corresponds to which
Python step class.

The lookup is defined statically so that type checkers
can know at compile time what steps exist.

The names are defined in their own file so that we do
not create a circular dependency between lookup
and processing step.
"""
from ._base import ProcessingStep
from ._step_identifiers import StepIdentifier
from .feature_extraction.spectrum import ComplexHarmonics
from .filters.bessel import LowpassBessel
from .filters.butterworth import LowpassButter
from .filters.chebyshev import LowpassCheby1, LowpassCheby2
from .filters.fir import LowpassFIR
from .misc.cut import Cut
from .misc.split import Split
from .misc.statistics import Average
from .misc.unite import Unite
from .preprocessing.averaging import CoherentAveraging
from .preprocessing.baseline_correction import FIRBaselineCorrection
from .preprocessing.normalization import NormalizeFundamentalFrequency

# mypy: disable-error-code="dict-item"

#: Contains the Lookup from StepIdentifier to the actual ProcessingStep.
StepLookup: dict[StepIdentifier, ProcessingStep] = {
    # Features
    StepIdentifier.FEATURE_COMPLEX_HARMONICS.name: ComplexHarmonics,
    # Filters
    StepIdentifier.FILTERS_LOWPASS_BESSEL.name: LowpassBessel,
    StepIdentifier.FILTERS_LOWPASS_BUTTERWORTH.name: LowpassButter,
    StepIdentifier.FILTERS_LOWPASS_CHEBYSHEV.name: LowpassCheby1,
    StepIdentifier.FILTERS_LOWPASS_CHEBYSHEV2.name: LowpassCheby2,
    StepIdentifier.FILTERS_FIR_LOWPASS.name: LowpassFIR,
    # Misc
    StepIdentifier.MISC_CUT.name: Cut,
    StepIdentifier.MISC_SPLIT.name: Split,
    StepIdentifier.MISC_UNITE.name: Unite,
    StepIdentifier.MISC_AVERAGE_OVER.name: Average,
    # Preprocessing
    StepIdentifier.PREPROCESSING_COHERENT_AVERAGING.name: CoherentAveraging,
    StepIdentifier.PREPROCESSING_BASELINE_CORRECTION_FIR.name: FIRBaselineCorrection,
    StepIdentifier.PREPROCESSING_NORMALIZE_FUNDAMENTAL_FREQ.name: NormalizeFundamentalFrequency,
}
