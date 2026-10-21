"""tvsummary: summarize TV show records by genre and language."""

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    GenreCounts,
    ShowsWithoutGenre,
    UnratedCount,
)
from tvsummary.models import Show
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import DownloadError, TVMazeSource

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "GenreCounts",
    "ShowsWithoutGenre",
    "UnratedCount",
    "Show",
    "build_summary",
    "write_summary",
    "DownloadError",
    "TVMazeSource",
]