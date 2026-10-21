"""Tests for sources.py. None of them use the network."""

import pytest
import requests

from tvsummary import sources
from tvsummary.errors import DataShapeError, SourceError


def test_a_failed_download_raises_a_source_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(*args: object, **kwargs: object) -> None:
        raise requests.ConnectionError("no network")

    monkeypatch.setattr(sources.requests, "get", fake_get)
    source = sources.TVMazeSource("https://example.invalid", timeout=1)
    with pytest.raises(SourceError, match="Could not reach"):
        source.fetch()


def test_records_become_show_objects() -> None:
    shows = sources.to_shows([{"name": "A"}, {"name": "B"}])
    assert [show.name for show in shows] == ["A", "B"]


def test_a_response_that_is_not_a_list_is_rejected() -> None:
    with pytest.raises(DataShapeError, match="Expected a list"):
        sources.to_shows({"name": "A"})


def test_a_record_that_is_not_an_object_is_rejected() -> None:
    with pytest.raises(DataShapeError, match="JSON object"):
        sources.to_shows(["just a string"])
