"""Building the summary and the run record, and writing them as JSON files."""

import json
import logging
import platform
from importlib import metadata
from pathlib import Path

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    FeaturedShows,
    GenreCounts,
    ShowsWithoutGenre,
    UnratedCount,
)
from tvsummary.config import Settings
from tvsummary.models import Show

logger = logging.getLogger(__name__)


def build_summary(shows: list[Show], settings: Settings) -> dict[str, object]:
    """Return the summary: source, record count, then one entry per aggregation."""
    aggregations: list[Aggregation] = [
        GenreCounts(),
        ShowsWithoutGenre(),
        AverageRatingByLanguage(),
        UnratedCount(),
        FeaturedShows(settings.sample_size, settings.seed),
    ]
    summary: dict[str, object] = {
        "source_url": settings.source_url,
        "records_processed": len(shows),
    }
    for aggregation in aggregations:
        summary[aggregation.key] = aggregation.compute(shows)
    return summary


def build_run_info(settings: Settings) -> dict[str, object]:
    """Record the settings and tool versions, so someone else can repeat the run."""
    return {
        "settings": {
            "source_url": settings.source_url,
            "timeout": settings.timeout,
            "output_dir": str(settings.output_dir),
            "seed": settings.seed,
            "sample_size": settings.sample_size,
            "log_level": settings.log_level,
        },
        "python": platform.python_version(),
        "pytest": metadata.version("pytest"),
        "mypy": metadata.version("mypy"),
        "ruff": metadata.version("ruff"),
    }


def write_json(data: dict[str, object], path: Path) -> None:
    """Write a dictionary to a JSON file, creating its folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    logger.info("Wrote %s", path)
