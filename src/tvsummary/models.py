"""The record class: one TV show from the TVmaze API."""


class Show:
    """One TV show, with missing or malformed values cleaned on creation.

    After a Show is created, the rest of the program can rely on:
    - name is always a string
    - genres is always a list (empty if the API gave none)
    - language and rating are either a real value or None
    """

    def __init__(self, raw):
        self.name = raw.get("name") or "Unknown"
        self.language = raw.get("language")
        self.genres = raw.get("genres") or []
        self.rating = (raw.get("rating") or {}).get("average")

    def __str__(self):
        rating_text = self.rating if self.rating is not None else "unrated"
        genre_text = ", ".join(self.genres) if self.genres else "no genre"
        return f"{self.name} ({self.language}), rating {rating_text}, genres: {genre_text}"