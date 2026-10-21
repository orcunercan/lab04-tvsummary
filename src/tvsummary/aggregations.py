"""Aggregations: a base class and one subclass per calculation in the summary."""


class Aggregation:
    """Base class for one calculation over a list of Show objects.

    Each subclass sets the key its result is stored under in the summary,
    and overrides compute to do its own calculation.
    """

    def __init__(self, key):
        self.key = key

    def compute(self, shows):
        """Return the result for this aggregation. Subclasses override this."""
        raise NotImplementedError


class GenreCounts(Aggregation):
    """Number of shows in each genre. A show with several genres counts in each."""

    def __init__(self):
        super().__init__("shows_per_genre")

    def compute(self, shows):
        counts = {}
        for show in shows:
            for genre in show.genres:
                counts[genre] = counts.get(genre, 0) + 1
        return counts


class ShowsWithoutGenre(Aggregation):
    """Names of shows that have no genre listed."""

    def __init__(self):
        super().__init__("shows_without_genre")

    def compute(self, shows):
        return [show.name for show in shows if not show.genres]


class AverageRatingByLanguage(Aggregation):
    """Average rating per language. Shows with no rating or language are skipped."""

    def __init__(self):
        super().__init__("average_rating_by_language")

    def compute(self, shows):
        totals = {}
        for show in shows:
            if show.language is None or show.rating is None:
                continue
            rating_sum, count = totals.get(show.language, (0, 0))
            totals[show.language] = (rating_sum + show.rating, count + 1)
        return {language: round(rating_sum / count, 2)
                for language, (rating_sum, count) in totals.items()}


class UnratedCount(Aggregation):
    """Number of shows with no average rating."""

    def __init__(self):
        super().__init__("unrated_shows")

    def compute(self, shows):
        return sum(1 for show in shows if show.rating is None)