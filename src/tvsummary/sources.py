"""Fetching the TV show records. This is the only module that imports requests."""

import requests

from tvsummary.errors import DataShapeError, SourceError
from tvsummary.models import Show


def to_shows(raw_records: object) -> list[Show]:
    """Turn the downloaded data into Show objects, checking its shape first."""
    if not isinstance(raw_records, list):
        raise DataShapeError(
            f"Expected a list of shows, got {type(raw_records).__name__}."
        )
    shows: list[Show] = []
    for raw in raw_records:
        if not isinstance(raw, dict):
            raise DataShapeError("Every record in the response must be a JSON object.")
        shows.append(Show(raw))
    return shows


class TVMazeSource:
    """Downloads TV show records from the TVmaze API as Show objects."""

    def __init__(self, url: str, timeout: float) -> None:
        self.url = url
        self.timeout = timeout

    def download(self) -> object:
        """Download the raw JSON data. Network problems become a SourceError."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as error:
            raise SourceError(f"Could not reach {self.url}: {error}") from error
        try:
            return response.json()
        except ValueError as error:
            raise DataShapeError(
                f"The response from {self.url} is not valid JSON."
            ) from error

    def fetch(self) -> list[Show]:
        """Download the records and return them as a list of Show objects."""
        return to_shows(self.download())
