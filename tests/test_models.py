"""Tests for the Show class and two aggregations, using handmade records and no network."""

import unittest

from tvsummary import GenreCounts, Show, UnratedCount


class TestShow(unittest.TestCase):
    """Show should clean missing or malformed values when it is created."""

    def test_complete_record_keeps_its_values(self):
        show = Show({"name": "Test Show", "language": "English",
                     "genres": ["Drama", "Comedy"], "rating": {"average": 7.5}})
        self.assertEqual(show.name, "Test Show")
        self.assertEqual(show.genres, ["Drama", "Comedy"])
        self.assertEqual(show.rating, 7.5)

    def test_missing_genres_become_an_empty_list(self):
        show = Show({"name": "No Genre", "genres": None})
        self.assertEqual(show.genres, [])

    def test_null_rating_becomes_none(self):
        show = Show({"name": "Unrated", "rating": {"average": None}})
        self.assertIsNone(show.rating)

    def test_missing_rating_object_becomes_none(self):
        show = Show({"name": "No Rating Field"})
        self.assertIsNone(show.rating)


class TestAggregations(unittest.TestCase):
    """Aggregations should give the right result for a small handmade list of shows."""

    def setUp(self):
        self.shows = [
            Show({"name": "A", "language": "English", "genres": ["Drama"], "rating": {"average": 8.0}}),
            Show({"name": "B", "language": "English", "genres": ["Drama", "Comedy"], "rating": None}),
            Show({"name": "C", "language": "Japanese", "genres": [], "rating": {"average": 6.0}}),
        ]

    def test_genre_counts_count_each_genre_once_per_show(self):
        self.assertEqual(GenreCounts().compute(self.shows), {"Drama": 2, "Comedy": 1})

    def test_unrated_count(self):
        self.assertEqual(UnratedCount().compute(self.shows), 1)


if __name__ == "__main__":
    unittest.main()