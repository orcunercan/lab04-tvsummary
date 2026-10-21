"""The record class: one TV show from the TVmaze API."""

from typing import Any


class Show:
    """One TV show, with missing or malformed values cleaned on creation.

    After a Show is created, the rest of the program can rely on:
    - name is always a string
    - genres is always a list (empty if the API gave none)
    - language and rating are either a real value or None
    """

    def __init__(self, raw: dict[str, Any]) -> None:
        # raw is JSON from the API, so its values have no fixed type yet.
        # This is the one place they are cleaned into the types below.
        self.name: str = raw.get("name") or "Unknown"
        self.language: str | None = raw.get("language")
        self.genres: list[str] = raw.get("genres") or []
        self.rating: float | None = (raw.get("rating") or {}).get("average")

    def __str__(self) -> str:
        rating_text = self.rating if self.rating is not None else "unrated"
        genre_text = ", ".join(self.genres) if self.genres else "no genre"
        return (
            f"{self.name} ({self.language}), rating {rating_text}, genres: {genre_text}"
        )
