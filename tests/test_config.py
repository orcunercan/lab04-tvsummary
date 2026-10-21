"""Tests for reading the settings file. Each test uses its own temporary folder."""

from pathlib import Path

import pytest

from tvsummary import SettingsError, load_settings


def test_a_complete_settings_file_is_read(settings_file: Path) -> None:
    settings = load_settings(settings_file)
    assert settings.seed == 7
    assert settings.sample_size == 2
    assert settings.output_dir == Path("out")


def test_settings_cannot_be_changed_after_loading(settings_file: Path) -> None:
    settings = load_settings(settings_file)
    with pytest.raises(AttributeError):
        settings.seed = 99  # type: ignore[misc]


def test_a_missing_settings_file_raises_a_settings_error(tmp_path: Path) -> None:
    with pytest.raises(SettingsError, match="Cannot read the settings file"):
        load_settings(tmp_path / "missing.toml")


def test_an_incomplete_settings_file_raises_a_settings_error(tmp_path: Path) -> None:
    path = tmp_path / "incomplete.toml"
    path.write_text('source_url = "https://example.invalid"\n', encoding="utf-8")
    with pytest.raises(SettingsError, match="missing the setting"):
        load_settings(path)
