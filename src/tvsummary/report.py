"""Building the summary from a list of shows, and writing it to a JSON file."""

import json

from tvsummary.aggregations import (
    AverageRatingByLanguage,
    GenreCounts,
    ShowsWithoutGenre,
    UnratedCount,
)


def build_summary(shows, source_url):
    """Return the summary dict: the source, the record count, then one entry per aggregation."""
    aggregations = [
        GenreCounts(),
        ShowsWithoutGenre(),
        AverageRatingByLanguage(),
        UnratedCount(),
    ]
    summary = {"source_url": source_url, "records_processed": len(shows)}
    for aggregation in aggregations:
        summary[aggregation.key] = aggregation.compute(shows)
    return summary


def write_summary(summary, path):
    """Write the summary to a JSON file, creating its folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")