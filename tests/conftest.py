"""Shared fixtures for the tvsummary tests."""

import pytest

from tvsummary import Show


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
