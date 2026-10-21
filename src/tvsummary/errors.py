"""The package's own errors. main() catches TVSummaryError and reports it."""


class TVSummaryError(Exception):
    """Base class for every error this package raises on purpose."""


class SourceError(TVSummaryError):
    """The TV show records could not be downloaded."""


class DataShapeError(TVSummaryError):
    """The downloaded data does not have the shape the program expects."""


class SettingsError(TVSummaryError):
    """The settings file is missing, unreadable or incomplete."""
