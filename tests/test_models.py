"""Tests for the Show record class, using handmade records and no network."""

import pytest

from tvsummary import Show


def test_a_complete_record_keeps_its_values() -> None:
    show = Show(
        {
            "name": "Test Show",
            "language": "English",
            "genres": ["Drama", "Comedy"],
            "rating": {"average": 7.5},
        }
    )
    assert show.name == "Test Show"
    assert show.language == "English"
    assert show.genres == ["Drama", "Comedy"]
    assert show.rating == 7.5


@pytest.mark.parametrize(
    "raw",
    [
        {"name": "X", "genres": None},
        {"name": "X", "genres": []},
        {"name": "X"},
    ],
)
def test_a_missing_genre_list_becomes_an_empty_list(raw: dict) -> None:
    assert Show(raw).genres == []


@pytest.mark.parametrize(
    "raw",
    [
        {"name": "X", "rating": {"average": None}},
        {"name": "X", "rating": None},
        {"name": "X"},
    ],
)
def test_a_missing_rating_becomes_none(raw: dict) -> None:
    assert Show(raw).rating is None


def test_a_missing_name_becomes_unknown() -> None:
    assert Show({}).name == "Unknown"


def test_str_describes_an_unrated_show_with_no_genre() -> None:
    text = str(Show({"name": "X", "language": "English"}))
    assert text == "X (English), rating unrated, genres: no genre"
