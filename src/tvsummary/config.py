"""Settings in one place: where the data comes from and where the summary goes."""

from pathlib import Path

SOURCE_URL = "https://api.tvmaze.com/shows?page=0"
TIMEOUT = 10
OUTPUT_PATH = Path("data") / "processed" / "summary.json"