"""Shared fixtures for the tvsummary tests."""

from pathlib import Path

import pytest

from tvsummary import Show

SETTINGS_TEXT = """
source_url = "https://example.invalid/shows"
timeout = 5
output_dir = "out"
seed = 7
sample_size = 2
log_level = "DEBUG"
"""


@pytest.fixture
def shows() -> list[Show]:
    """Three handmade shows: a full record, an unrated one and one with no genre."""
    return [
        Show(
            {
                "name": "A",
                "language": "English",
                "genres": ["Drama"],
                "rating": {"average": 8.0},
            }
        ),
        Show(
            {
                "name": "B",
                "language": "English",
                "genres": ["Drama", "Comedy"],
                "rating": {"average": None},
            }
        ),
        Show(
            {
                "name": "C",
                "language": "Japanese",
                "genres": [],
                "rating": {"average": 6.0},
            }
        ),
    ]


@pytest.fixture
def settings_file(tmp_path: Path) -> Path:
    """A complete settings file in a temporary folder."""
    path = tmp_path / "tvsummary.toml"
    path.write_text(SETTINGS_TEXT, encoding="utf-8")
    return path
