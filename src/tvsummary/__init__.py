"""tvsummary: summarize TV show records by genre and language."""

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    FeaturedShows,
    GenreCounts,
    ShowsWithoutGenre,
    UnratedCount,
)
from tvsummary.config import Settings, load_settings
from tvsummary.errors import DataShapeError, SettingsError, SourceError, TVSummaryError
from tvsummary.models import Show
from tvsummary.report import build_run_info, build_summary, write_json
from tvsummary.sources import TVMazeSource, to_shows

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "FeaturedShows",
    "GenreCounts",
    "ShowsWithoutGenre",
    "UnratedCount",
    "Settings",
    "load_settings",
    "DataShapeError",
    "SettingsError",
    "SourceError",
    "TVSummaryError",
    "Show",
    "build_run_info",
    "build_summary",
    "write_json",
    "TVMazeSource",
    "to_shows",
]
