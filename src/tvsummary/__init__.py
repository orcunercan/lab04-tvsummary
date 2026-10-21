"""tvsummary: summarize TV show records by genre and language."""

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    GenreCounts,
    ShowsWithoutGenre,
    UnratedCount,
)
from tvsummary.errors import DataShapeError, SettingsError, SourceError, TVSummaryError
from tvsummary.models import Show
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import TVMazeSource, to_shows

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "GenreCounts",
    "ShowsWithoutGenre",
    "UnratedCount",
    "DataShapeError",
    "SettingsError",
    "SourceError",
    "TVSummaryError",
    "Show",
    "build_summary",
    "write_summary",
    "TVMazeSource",
    "to_shows",
]
