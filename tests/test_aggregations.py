"""Tests for each aggregation class, using the handmade shows from conftest.py."""

import logging

import pytest

from tvsummary import (
    Aggregation,
    AverageRatingByLanguage,
    GenreCounts,
    Show,
    ShowsWithoutGenre,
    UnratedCount,
)


def test_genre_counts_count_each_genre_once_per_show(shows: list[Show]) -> None:
    assert GenreCounts().compute(shows) == {"Drama": 2, "Comedy": 1}


def test_shows_without_genre_lists_their_names(shows: list[Show]) -> None:
    assert ShowsWithoutGenre().compute(shows) == ["C"]


def test_average_rating_skips_unrated_shows(shows: list[Show]) -> None:
    result = AverageRatingByLanguage().compute(shows)
    assert result == {"English": pytest.approx(8.0), "Japanese": pytest.approx(6.0)}


def test_unrated_count(shows: list[Show]) -> None:
    assert UnratedCount().compute(shows) == 1


@pytest.mark.parametrize(
    ("aggregation", "key"),
    [
        (GenreCounts(), "shows_per_genre"),
        (ShowsWithoutGenre(), "shows_without_genre"),
        (AverageRatingByLanguage(), "average_rating_by_language"),
        (UnratedCount(), "unrated_shows"),
    ],
)
def test_each_aggregation_uses_its_summary_key(
    aggregation: Aggregation, key: str
) -> None:
    assert aggregation.key == key


def test_the_base_class_must_be_overridden(shows: list[Show]) -> None:
    with pytest.raises(NotImplementedError):
        Aggregation("base").compute(shows)


def test_a_skipped_show_is_logged_as_a_warning(
    shows: list[Show], caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.WARNING):
        AverageRatingByLanguage().compute(shows)
    assert "Skipping 'B'" in caplog.text
