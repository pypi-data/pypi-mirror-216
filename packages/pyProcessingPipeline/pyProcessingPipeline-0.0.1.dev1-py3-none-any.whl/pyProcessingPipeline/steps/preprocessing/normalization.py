"""
Normalization
=============

ProcessingSteps for normalization.

Classes
-------
NormalizeFundamentalFrequency
    Used for normalizing a timeseries' fundamental frequency.
"""

import logging

import numpy as np

from ...types import FloatArray, ProcessingStepInput
from .._base import ProcessingStep

logger = logging.getLogger(__name__)


class NormalizeFundamentalFrequency(ProcessingStep):
    """Normalize the fundamental frequency's amplitude to 1.

    This finds the fundamental frequency, calculates it's power
    and normalizes the signal so that the amplitude of the fundamental
    frequency is about 1.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> # Sample signal with 10 periods and an amplitude of 0.1
    >>> signal = 0.1 * np.sin(10 * np.linspace(0, 2*np.pi, 200))
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that normalizes the fundamental frequency",
    ... )
    >>> processing_run.add_step(NormalizeFundamentalFrequency())
    >>> processing_run.run([signal])
    >>> # Amplitude of Signal should be 0.10
    >>> round(max(signal), 1)
    0.1

    >>> # Amplitude after processing should be about 1.0
    >>> round(max(processing_run.results[0]), 1)
    1.0

    The input mapping shows which input got mapped to which output:
    >>> processing_run.steps[0].input_mapping
    {0: 0}
    """

    def __init__(self) -> None:
        super().__init__(locals())

    def run(self, step_input: ProcessingStepInput) -> None:
        self._init_results()

        output_index = 0
        for input_index, item in enumerate(step_input.data):
            try:
                normalized = self._normalize(item)
            except Exception:
                logger.warning("Could not normalize signal %d", input_index)
                self._input_mapping[input_index] = None
            else:
                self._data.append(normalized)
                self._input_mapping[input_index] = output_index
                output_index += 1

    def _normalize(self, data: FloatArray) -> FloatArray:
        """Calculates the datas fft, finds the fundamental
        frequency and divides the signal by the power of
        that frequency."""
        # Make sure that the mean of the signal is 0:
        zero_mean: FloatArray = data - data.mean()
        # Calculate fft and make it symmetrical
        fft = np.fft.fft(zero_mean)
        fft = np.fft.fftshift(fft)
        # Zero-centered power
        power = np.sqrt(fft * np.conjugate(fft)) * (2.0 / len(zero_mean))
        # Find the amplitue of fundamental frequency
        fundamental_amplitude = max(power)
        # and normalize the signal
        normalized: FloatArray = zero_mean / np.real(fundamental_amplitude)

        return normalized
