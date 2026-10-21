"""Building the summary from a list of shows, and writing it to a JSON file."""

import json
import logging
from pathlib import Path

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    GenreCounts,
    ShowsWithoutGenre,
    UnratedCount,
)
from tvsummary.models import Show

logger = logging.getLogger(__name__)


def build_summary(shows: list[Show], source_url: str) -> dict[str, object]:
    """Return the summary: source, record count, then one entry per aggregation."""
    aggregations: list[Aggregation] = [
        GenreCounts(),
        ShowsWithoutGenre(),
        AverageRatingByLanguage(),
        UnratedCount(),
    ]
    summary: dict[str, object] = {
        "source_url": source_url,
        "records_processed": len(shows),
    }
    for aggregation in aggregations:
        summary[aggregation.key] = aggregation.compute(shows)
    return summary


def write_summary(summary: dict[str, object], path: Path) -> None:
    """Write the summary to a JSON file, creating its folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logger.info("Wrote the summary to %s", path)
