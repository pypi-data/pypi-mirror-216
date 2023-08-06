"""
Type Definitions
================

Type definitions and abstract base classes used in
the processing package.

Types
-----
FloatArray
    Numpy array that contains either floats or doubles.
ProcessingStepOutput
    A list of FloatArrays.

Classes
-------
ListBasedProcessingStepInput
    Unpersistable input for a ProcessingStep. Is automatically
    generated from any sequence of arrays given to a ProcessingRun,
    which allows runs to be used without storing data in our Database.
Model
    A trained model of any kind, mostly created by classifying
    processing steps.
ProcessingStepInput
    Abstract base class for every Input to a ProcessingStep.
    The ProcessingStep class itself inherits from this base class,
    so that every Step can also be used as an input for
    any other Step.
StepLog
    A single log entry, which can be used by processing
    steps to store additional data. StepLogs are persisted
    in our database.
"""
from abc import ABC, abstractmethod
from typing import Any, TypedDict

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float32 | np.float64]

ProcessingStepOutput = list[FloatArray]


class StepLog(TypedDict):
    """Single log element used for storing
    ProcessingStep metadata associated to a single
    input element."""

    element_index: int
    description: str
    value: Any


class Model(TypedDict):
    """Model output of a ProcessingStep."""

    name: str
    model: Any


class ProcessingStepInput(ABC):
    """Defines the interface for all inputs
    that can be used for a processing step.
    This includes TimeSeries, other ProcessingSteps
    and whatever else we might implement in the future.

    Having a single interface enables processings steps to
    not care about the specific type of input, and instead
    rely on a common way of accessing the underlying data.
    """

    @property
    @abstractmethod
    def data(self) -> ProcessingStepOutput:
        """Returns the underlying data as a list.

        The list-type is needed to allow random
        integer access to each element. This enables
        us to create input/output mappings and access
        data outside of for-loops.

        Returns
        -------
        ProcessingStepOutput
            The raw data provided by the input. Every
            entry is a numpy array to unify access, even
            if the output is only a single number.
        """
        raise NotImplementedError


class ListBasedProcessingStepInput(ProcessingStepInput):
    """ProcessingStepInput used for simple list inputs.

    This allows ProcessingRuns to be used with unpersisted
    inputs, e.g. simple in-memory arrays or any other
    data you can load into numpy arrays.

    Can not be persisted in our database, since the input
    was not persisted itself.

    Lists of arrays are simply wrapped and can be accessed
    using the data-method:

    >>> input_arrays = [np.ones(5), np.zeros(5)]
    >>> step_input = ListBasedProcessingStepInput(input_arrays)
    >>> step_input.data
    [array([1., 1., 1., 1., 1.]), array([0., 0., 0., 0., 0.])]

    While lists of lists are cast into a list of arrays

    >>> input_lists = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    >>> step_input = ListBasedProcessingStepInput(input_lists)
    >>> step_input.data
    [array([1, 2, 3]), array([4, 5]), array([6, 7, 8, 9])]
    """

    _data: list[FloatArray]

    def __init__(self, input_list: list[FloatArray] | list[Any]) -> None:
        self._data = [np.array(item) for item in input_list]

    @property
    def data(self) -> ProcessingStepOutput:
        return self._data
