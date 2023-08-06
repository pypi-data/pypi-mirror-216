"""
IO-Exceptions
=============

Contains all io-related exceptions.
Every exception is a subclass of the
main ProcessingException, so that they can
all be intercepted using a simple
::

    try:
        something()
    except ProcessingException:
        ...

"""

from ..exceptions import ProcessingException


class UnknownSetError(ProcessingException):
    """Raised if a TimeSeriesSet with a given ID does not exist."""


class UnknownSourceError(ProcessingException):
    """Raised if a TimeSeriesSet's Source Table is unknown."""


class EmptySetError(ProcessingException):
    """Raised if a TimeSeriesSet contains no records."""


class UnknownRecordError(ProcessingException):
    """Raised if a record with a given source and id does not exist."""


class MissingTablesError(ProcessingException):
    """Raised if the database given is missing a required table.
    If this is the case, the database setup was probably skipped."""


class DatabaseConnectionNotSetError(ProcessingException):
    """Raised if the database connection has not been setup
    before trying to access the database.
    Call setup_database_connection first.
    """
