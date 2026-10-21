"""Fetching the TV show records. This is the only module that imports requests."""

import requests

from tvsummary.models import Show


class DownloadError(Exception):
    """Raised when the TV show records cannot be downloaded."""


class TVMazeSource:
    """Downloads TV show records from the TVmaze API as Show objects."""

    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout

    def fetch(self):
        """Download the records and return them as a list of Show objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            raw_records = response.json()
        except requests.RequestException as error:
            raise DownloadError(
                f"Could not download data from {self.url}: {error}"
            ) from error
        return [Show(raw) for raw in raw_records]