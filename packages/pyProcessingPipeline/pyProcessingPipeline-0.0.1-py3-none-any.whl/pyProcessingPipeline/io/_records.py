"""
Records
=======

Contains the definitions for database records,
which are the building blocks that make up a TimeSeriesSet.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Optional, final

from ..types import FloatArray
from ._database import (
    DatabaseSource,
    get_array_from_database,
    get_float_from_database,
    get_int_from_database,
    get_string_from_database,
)
from .exceptions import UnknownRecordError

logger = logging.getLogger(__name__)


class TimeSeriesRecord(ABC):
    """Single record contained within a TimeSeriesSet.

    This is the base class that is implemented by every
    record type, such as STS (SimulatedTimeSeries),
    imported WFDB series etc.

    Attributes
    ----------
    source : DatabaseSource
        The database where this record came from.
    record_id : int
        The unique ID of this record in the source database.
    data : FloatArray
        The actual timeseries / data contained within.
    sampling_rate : float
        The sampling rate for the data contained within this record.

    """

    _source: DatabaseSource
    _record_id: int

    _data: FloatArray
    _sampling_rate: float

    @abstractmethod
    def __init__(self, record_id: int) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.source} Record with ID {self.record_id}"

    @staticmethod
    def new(source: DatabaseSource, record_id: int) -> TimeSeriesRecord:
        """Create a new TimeSeriesRecord.

        This gets the record with the given ID from the given source table.

        This is custom for every database source table we have,
        so this function just dispatches the call to the right
        subclass."""
        match source:
            case DatabaseSource.SIMULATED_TIME_SERIES:
                return STSRecord(record_id=record_id)
            case DatabaseSource.WFDB:
                return WFDBRecord(record_id=record_id)
            case DatabaseSource.RAW_TIME_SERIES:
                return RTSRecord(record_id=record_id)
            case DatabaseSource.MACSIM_TIME_SERIES:
                return MTSRecord(record_id=record_id)
            case _:
                raise UnknownRecordError(f"Source {source} is unknown!")

    @final
    def _check_if_record_exists(self) -> None:
        """Checks wether the given record with id
        exists in the given source table.

        Raises
        ------
        UnknownRecordError
            If the given record is unknown.
        """
        stored_id = get_int_from_database(
            name="id", table=self.source, item_id=self.record_id
        )
        if stored_id != self.record_id:
            raise UnknownRecordError(
                f"Unknown record with Source {self._source.value}"
                f" and ID {self._record_id}!"
            )

    @property
    @final
    def source(self) -> DatabaseSource:
        """The database where this record came from."""
        return self._source

    @property
    @final
    def record_id(self) -> int:
        """The unique ID of this record in the source database."""
        return self._record_id

    @property
    @abstractmethod
    def data(self) -> FloatArray:
        """The timeseries data contained within this record."""
        raise NotImplementedError

    @property
    @abstractmethod
    def sampling_rate(self) -> float:
        """The sampling rate for the data contained within this record."""
        raise NotImplementedError


class STSRecord(TimeSeriesRecord):
    """Single record from the simulated time series table.

    Attributes
    ----------
    source : DatabaseSource
        The database where this record came from (STS).
    record_id : int
        The unique ID of this record in the STS database.
    data : FloatArray
        A two-dimensional numpy array, where the first entry contains
        the flow and the second entry contains the pressure.
    sampling_rate : float
        The sampling rate for the timeseries.
    flow : FloatArray
        The flowrate of this record, same as data[0].
    pressure : FloatArray
        The pressure timeseries of this record, same as data[1]
    """

    _source: DatabaseSource = DatabaseSource.SIMULATED_TIME_SERIES

    _flow: FloatArray
    _pressure: FloatArray

    _application_id: Optional[int]
    _node_id: Optional[int]
    _solver_run_id: Optional[int]

    def __init__(self, record_id: int) -> None:
        self._record_id = record_id
        self._check_if_record_exists()

    @property
    def data(self) -> FloatArray:
        if not hasattr(self, "_data"):
            data = get_array_from_database(
                name="data", table=self.source, item_id=self.record_id, dtype="float"
            )
            if data is None:
                raise ValueError(
                    f"Record {self.source.value}:{self.record_id} is missing data!"
                )
            # Since the STS data is made up of two timeseries, one for flow
            # and one for pressure, the returned array might have hugely
            # different amplitudes in its first and second half.
            self._data = data

        return self._data

    @property
    def sampling_rate(self) -> float:
        if not hasattr(self, "_sampling_rate"):
            rate = get_float_from_database(
                name="rate", table=self.source, item_id=self.record_id
            )
            if rate is None:
                raise ValueError(
                    f"Record {self.source.value}:{self.record_id}"
                    "is missing a sampling rate!"
                )
            self._sampling_rate = rate

        return self._sampling_rate

    @property
    def flow(self) -> FloatArray:
        """The flow that was simulated in the node
        during the corresponding solver run."""
        # Flow is contained in the first entry in our data.
        return self.data[: len(self.data) // 2]

    @property
    def pressure(self) -> FloatArray:
        """The pressure that was simulated in this node
        during the corresponding solver run."""
        # Pressure is contained in the second entry of our data.
        return self.data[(len(self.data) // 2) :]

    @property
    def application_id(self) -> Optional[int]:
        """The application id this simulation belongs to."""
        if not hasattr(self, "_application_id"):
            self._application_id = get_int_from_database(
                name="applicationId", table=self.source, item_id=self.record_id
            )
        return self._application_id

    @property
    def node_id(self) -> Optional[int]:
        """The node in the simulation this record belongs to."""
        if not hasattr(self, "_application_id"):
            self._node_id = get_int_from_database(
                name="nodeId", table=self.source, item_id=self.record_id
            )
        return self._node_id

    @property
    def solver_run_id(self) -> Optional[int]:
        """The solver run that created this record."""
        if not hasattr(self, "_application_id"):
            self._solver_run_id = get_int_from_database(
                name="solverRunId", table=self.source, item_id=self.record_id
            )
        return self._solver_run_id


class WFDBRecord(TimeSeriesRecord):
    """Single record that was imported to our database
    using the wfdb importer.
    """

    _source: DatabaseSource = DatabaseSource.WFDB

    _record_name: Optional[str]
    _comments: Optional[str]
    _signal_name: Optional[str]
    _signal_unit_id: Optional[int]
    _lastmodified: Optional[int]

    def __init__(self, record_id: int) -> None:
        self._record_id = record_id
        self._check_if_record_exists()

    @property
    def data(self) -> FloatArray:
        if not hasattr(self, "_data"):
            dtype = get_string_from_database(
                name="signal_type", table=self.source, item_id=self.record_id
            )
            if dtype is None:
                logger.warning("Could not find record dtype. Assuming double.")
            signal = get_array_from_database(
                name="p_signal",
                table=self.source,
                item_id=self.record_id,
                dtype=dtype or "double",  # type: ignore
            )
            if signal is None:
                raise ValueError(
                    f"Record {self.source.value}:{self.record_id}"
                    "is missing its p_signal!"
                )
            self._data = signal

        return self._data

    @property
    def sampling_rate(self) -> float:
        if not hasattr(self, "_sampling_rate"):
            rate = get_float_from_database(
                name="sampling_rate", table=self.source, item_id=self.record_id
            )
            if rate is None:
                raise ValueError(
                    f"Record {self.source}:{self.record_id} is missing a sampling rate!"
                )
            self._sampling_rate = rate

        return self._sampling_rate

    @property
    def record_name(self) -> Optional[str]:
        """Get the name of this record."""
        if not hasattr(self, "_record_name"):
            self._record_name = get_string_from_database(
                name="record_name", table=self.source, item_id=self.record_id
            )
        return self._record_name

    @property
    def comments(self) -> Optional[str]:
        """Get the comments for this record."""
        if not hasattr(self, "_comments"):
            self._comments = get_string_from_database(
                name="comments", table=self.source, item_id=self.record_id
            )
        return self._comments

    @property
    def signal_name(self) -> Optional[str]:
        """Get the signal name of this record."""
        if not hasattr(self, "_signal_name"):
            self._signal_name = get_string_from_database(
                name="sig_name", table=self.source, item_id=self.record_id
            )
        return self._signal_name

    @property
    def signal_unit_id(self) -> Optional[int]:
        """Get the signal unit's ID."""
        if not hasattr(self, "_signal_unit_id"):
            self._signal_unit_id = get_int_from_database(
                name="unit", table=self.source, item_id=self.record_id
            )
        return self._signal_unit_id

    @property
    def lastmodified(self) -> Optional[int]:
        """Get the time when this record was last modified."""
        if not hasattr(self, "_lastmodified"):
            self._lastmodified = get_int_from_database(
                name="lastmodified", table=self.source, item_id=self.record_id
            )
        return self._lastmodified


class RTSRecord(TimeSeriesRecord):
    """Single record from the RawTimeSeries table."""

    _source: DatabaseSource = DatabaseSource.RAW_TIME_SERIES

    _measurement_id: Optional[int]
    _signal_name: Optional[str]
    _signal_unit_id: Optional[int]
    _frequency_lowpass: Optional[float]
    _frequency_highpass: Optional[float]
    _characteristic_time_series: Optional[FloatArray]

    def __init__(self, record_id: int) -> None:
        self._record_id = record_id
        self._check_if_record_exists()

    @property
    def data(self) -> FloatArray:
        if not hasattr(self, "_data"):
            data = get_array_from_database(
                name="data", table=self.source, item_id=self.record_id, dtype="float"
            )
            if data is None:
                raise ValueError(
                    f"Record {self.source}:{self.record_id} is missing its p_signal!"
                )
            self._data = data

        return self._data

    @property
    def sampling_rate(self) -> float:
        if not hasattr(self, "_sampling_rate"):
            rate = get_float_from_database(
                name="sampling_rate", table=self.source, item_id=self.record_id
            )
            if rate is None:
                raise ValueError(
                    f"Record {self.source}:{self.record_id} is missing a sampling rate!"
                )
            self._sampling_rate = rate

        return self._sampling_rate

    @property
    def measurement_id(self) -> Optional[int]:
        """Get the record's MeasurementID."""
        if not hasattr(self, "_measurement_id"):
            self._measurement_id = get_int_from_database(
                name="measurementId", table=self.source, item_id=self.record_id
            )

        return self._measurement_id

    @property
    def signal_name(self) -> Optional[str]:
        """Get this record's signal name."""
        if not hasattr(self, "_signal_name"):
            self._signal_name = get_string_from_database(
                name="signalName", table=self.source, item_id=self.record_id
            )

        return self._signal_name

    @property
    def signal_unit_id(self) -> Optional[int]:
        """Get this record's unit id."""
        if not hasattr(self, "_signal_unit_id"):
            self._signal_unit_id = get_int_from_database(
                name="unit", table=self.source, item_id=self.record_id
            )

        return self._signal_unit_id

    @property
    def frequency_lowpass(self) -> Optional[float]:
        """Get the frequency of the records applied lowpass."""
        if not hasattr(self, "_frequency_lowpass"):
            self._frequency_lowpass = get_float_from_database(
                name="freqLP", table=self.source, item_id=self.record_id
            )

        return self._frequency_lowpass

    @property
    def frequency_highpass(self) -> Optional[float]:
        """Get the frequency of the applied highpass for this record."""
        if not hasattr(self, "_frequency_highpass"):
            self._frequency_highpass = get_float_from_database(
                name="freqHP", table=self.source, item_id=self.record_id
            )

        return self._frequency_highpass

    @property
    def characteristic_time_series(
        self,
    ) -> Optional[FloatArray]:
        """Get the characteristic time series CTS based on this record."""
        if not hasattr(self, "_characteristic_time_series"):
            self._characteristic_time_series = get_array_from_database(
                name="cts", table=self.source, item_id=self.record_id, dtype="float"
            )

        return self._characteristic_time_series


class MTSRecord(TimeSeriesRecord):
    """Single record from the MacSim simualated timeseries table.

    All data is expected to be stored as float-arrays.
    """

    _source: DatabaseSource = DatabaseSource.MACSIM_TIME_SERIES

    _macsim_id: Optional[int]
    _node_id: Optional[int]
    _signal_name: Optional[str]
    _signal_type: Optional[int]
    _characteristic_time_series: Optional[FloatArray]

    def __init__(self, record_id: int) -> None:
        self._record_id = record_id
        self._check_if_record_exists()

    @property
    def data(self) -> FloatArray:
        if not hasattr(self, "_data"):
            data = get_array_from_database(
                name="data", table=self.source, item_id=self.record_id, dtype="float"
            )
            if data is None:
                raise ValueError(
                    f"Record {self.source}:{self.record_id} is missing its p_signal!"
                )
            self._data = data

        return self._data

    @property
    def sampling_rate(self) -> float:
        if not hasattr(self, "_sampling_rate"):
            rate = get_float_from_database(
                name="sampling_rate", table=self.source, item_id=self.record_id
            )
            if rate is None:
                raise ValueError(
                    f"Record {self.source}:{self.record_id} is missing a sampling rate!"
                )
            self._sampling_rate = rate

        return self._sampling_rate

    @property
    def macsim_id(self) -> Optional[int]:
        """Get the ID of the Macsim run this record came from."""
        if not hasattr(self, "_macsim_id"):
            self._macsim_id = get_int_from_database(
                name="macSimId", table=self.source, item_id=self.record_id
            )

        return self._macsim_id

    @property
    def node_id(self) -> Optional[int]:
        """Get the node id this record was recorded at."""
        if not hasattr(self, "_node_id"):
            self._node_id = get_int_from_database(
                name="nodeId", table=self.source, item_id=self.record_id
            )

        return self._node_id

    @property
    def signal_name(self) -> Optional[str]:
        """Get the signal name for this record."""
        if not hasattr(self, "_signal_name"):
            self._signal_name = get_string_from_database(
                name="signalname", table=self.source, item_id=self.record_id
            )

        return self._signal_name

    @property
    def signal_type(self) -> Optional[int]:
        """Get the signal type of this record."""
        if not hasattr(self, "_signal_type"):
            self._signal_type = get_int_from_database(
                name="type", table=self.source, item_id=self.record_id
            )

        return self._signal_type

    @property
    def characteristic_time_series(
        self,
    ) -> Optional[FloatArray]:
        """Get the characteristic timeseries based on this record."""
        if not hasattr(self, "_characteristic_time_series"):
            self._characteristic_time_series = get_array_from_database(
                name="cts", table=self.source, item_id=self.record_id, dtype="float"
            )

        return self._characteristic_time_series
