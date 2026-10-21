"""Tests for main(): the exit code and what the user sees. No network is used."""

from pathlib import Path

import pytest
import requests

from tvsummary import sources
from tvsummary.main import main


def test_a_missing_settings_file_exits_with_code_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(["--config", str(tmp_path / "none.toml")])
    assert exit_code == 1
    assert "Error: Cannot read the settings file" in capsys.readouterr().err


def test_a_failed_download_exits_with_code_1(
    settings_file: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_get(*args: object, **kwargs: object) -> None:
        raise requests.ConnectionError("no network")

    monkeypatch.setattr(sources.requests, "get", fake_get)
    exit_code = main(["--config", str(settings_file)])
    assert exit_code == 1
    assert "Error: Could not reach" in capsys.readouterr().err


def test_a_successful_run_writes_both_files(
    settings_file: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_download(self: sources.TVMazeSource) -> object:
        return [{"name": "A", "language": "English", "rating": {"average": 7.0}}]

    monkeypatch.setattr(sources.TVMazeSource, "download", fake_download)
    monkeypatch.chdir(tmp_path)
    exit_code = main(["--config", str(settings_file)])
    assert exit_code == 0
    assert (tmp_path / "out" / "summary.json").exists()
    assert (tmp_path / "out" / "run_info.json").exists()
