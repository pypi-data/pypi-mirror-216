"""
Spectrum Features
=================

ProcessingSteps for producing features
from a signals frequency spectrum.

Classes
-------
ComplexHarmonics
    Compares the complex frequencies of two adjacent timeseries.
    Legacy.
"""
import logging
import math
from typing import Optional

import numpy as np
from scipy.signal import find_peaks

from ...exceptions import ProcessingException
from ...types import ProcessingStepInput
from ...util import batch_generator
from .._base import ProcessingStep

logger = logging.getLogger(__name__)


class UnequalSampleAmountException(ProcessingException):
    """Raised if the input signals don't have the same
    amount of samples."""


class ComplexHarmonics(ProcessingStep):
    """Step for extracting and comparing harmonic peaks
    from the frequency spectrum.

    This uses a simple fft and peak-find to search for a given
    amount of peaks in the frequency spectrum.
    It then compares two consecutive timeseries' peaks
    and returns their quotient.

    Attention: Peak-frequencies are assumed to be equal,
    so only phase and amplitude are actually compared.
    This step is implemented as a leftover from the
    original Matlab Pipeline and is probably not
    useful for general use, since it assumes two
    consecutive timeseries to be from the same
    patient.

    Example
    -------
    Assume that you have two timeseries where you want
    to calculate the quotient of both series' frequency peaks.

    >>> time = np.linspace(0, 10, 10*125) # 10 seconds with 125Hz
    >>> series1 = ( # Simple harmonics at 5, 10, 20, 40 Hz
    ...     np.sin(2*np.pi*5*time) +
    ...     np.sin(2*np.pi*10*time) +
    ...     np.sin(2*np.pi*20*time) +
    ...     np.sin(2*np.pi*40*time)
    ... )
    >>> series2 = ( # same as series1, but with added phase offsets
    ...     np.sin(2*np.pi*5*time + 0.5) +
    ...     np.sin(2*np.pi*10*time - 0.5) +
    ...     np.sin(2*np.pi*20*time + 1) +
    ...     np.sin(2*np.pi*40*time - 1)
    ... )

    To then calculate the difference between both frequency peaks,
    create a processing run

    >>> from pyProcessingPipeline import ProcessingRun
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the harmonic phase and amplitude",
    ... )

    and add this step:

    >>> processing_run.add_step(
    ...     ComplexHarmonics(
    ...         sampling_frequency=125,
    ...         num_peaks=4,
    ...         lower_bound=3.0,
    ...         upper_bound=50.0
    ...    )
    ... )
    >>> processing_run.run([series1, series2, series1, series2])

    The first amplitude and phase relationship is then

    >>> np.round(processing_run.results[0][:2], 2)
    array([ 0.88, -0.48])

    while the second amplitude/phase relationship is

    >>> np.round(processing_run.results[0][2:4], 2)
    array([0.88, 0.48])

    and so on.

    The io-mapping shows you which signals were used
    for comparing their harmonics:

    >>> processing_run.steps[0].input_mapping
    {0: 0, 1: 0, 2: 1, 3: 1}
    """

    _sampling_frequency: float
    _num_peaks: int
    _lower_bound: Optional[float]
    _upper_bound: Optional[float]

    def __init__(
        self,
        sampling_frequency: float,
        num_peaks: int,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
    ):
        """Create a feature extraction of frequency peaks.

        Parameters
        ----------
        sampling_frequency : float
            Frequency at which the signals were sampled, in Hz.
        num_peaks : int
            Number of peaks to extract from the frequency spectrum.
        lower_bound : Optional[float], default None
            Frequencies lower than this will be ignored, in Hz.
        upper_bound : Optional[float], default None
            Frequencies higher than this will be ignored, in Hz.
        """
        super().__init__(locals())
        self._sampling_frequency = sampling_frequency
        self._num_peaks = num_peaks
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    def run(self, step_input: ProcessingStepInput) -> None:
        self._init_results()

        # Make sure that all entries have the same length,
        # because otherwise their spectrums won't line up
        if not all(len(item) == len(step_input.data[0]) for item in step_input.data):
            raise UnequalSampleAmountException(
                "Not all timeseries have the same amount of samples! "
                + "Use preprocessing.Cut before running this step."
            )
        if len(step_input.data) % 2 != 0:
            logger.warning(
                "ComplexHarmonics requires an even amount of datasets. "
                "Step will drop the last dataset."
            )
            end_index = len(step_input.data) // 2 * 2
        else:
            end_index = len(step_input.data)

        # Early exit if no values are left after rounding.
        if end_index == 0:
            return

        output_index = 0
        samples_per_hz = len(step_input.data[0]) / self._sampling_frequency

        for input_index, item_batch in enumerate(
            batch_generator(step_input.data[:end_index], 2)
        ):
            try:
                first_spectrum = np.fft.fft(item_batch[0])
                second_spectrum = np.fft.fft(item_batch[1])
                lower_bound_index = math.floor(
                    (self._lower_bound or 0) * samples_per_hz
                )
                upper_bound_index = math.floor(
                    (self._upper_bound or self._sampling_frequency / 2) * samples_per_hz
                )
                # Set everything below lower_bound and above upper_bound to 0
                if lower_bound_index > 0:
                    first_spectrum[:lower_bound_index] = 0
                    first_spectrum[-lower_bound_index:] = 0
                    second_spectrum[:lower_bound_index] = 0
                    second_spectrum[-lower_bound_index:] = 0

                first_spectrum[upper_bound_index:-upper_bound_index] = 0
                second_spectrum[upper_bound_index:-upper_bound_index] = 0

                # Peak distance should be 0.8 times the max peak index,
                # assuming that the max peak is the fundamental frequency.
                peak_distance = math.floor(0.8 * np.argmax(np.abs(first_spectrum)))

                first_peaks, _ = find_peaks(
                    np.abs(first_spectrum), distance=peak_distance
                )
                second_peaks, _ = find_peaks(
                    np.abs(second_spectrum), distance=peak_distance
                )

                # Keep only the first n peaks
                first_peaks = first_peaks[: self._num_peaks]
                second_peaks = second_peaks[: self._num_peaks]

                logger.warning(
                    "Found peaks at index %s and %s", first_peaks, second_peaks
                )

                logger.warning("Peak distance %f", peak_distance)

                if not len(first_peaks) == len(second_peaks):
                    raise IndexError(
                        "Could not find the same amount of peaks "
                        + "for first and second spectrum!"
                    )

                # Now get the complex values at those peaks
                first_complex = first_spectrum[first_peaks]
                second_complex = second_spectrum[second_peaks]

                # And compare them with each other by picewiese division
                result = first_complex / second_complex
                result = np.stack([result.real, result.imag]).reshape(-1, order="F")
            except Exception as error:
                # Remember to multiply index by two, since we're using batches of 2
                logger.info(
                    "Could not get harmonix for signals %d, %d",
                    2 * input_index,
                    2 * input_index + 1,
                )
                self._input_mapping[2 * input_index] = None
                self._input_mapping[2 * input_index + 1] = None
                raise error
            else:
                # Remember to multiply index by two, since we're using batches of 2
                self._input_mapping[2 * input_index] = output_index
                self._input_mapping[2 * input_index + 1] = output_index
                self._data.append(result)
                output_index += 1
