"""Reading the settings file into a frozen Settings object."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from tvsummary.errors import SettingsError

DEFAULT_SETTINGS_PATH = Path("config") / "tvsummary.toml"


@dataclass(frozen=True)
class Settings:
    """Every value one run needs. Frozen, so it cannot change during a run."""

    source_url: str
    timeout: float
    output_dir: Path
    seed: int
    sample_size: int
    log_level: str


def load_settings(path: Path) -> Settings:
    """Read the TOML file into Settings. Missing or bad values raise SettingsError."""
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except OSError as error:
        raise SettingsError(
            f"Cannot read the settings file {path}: {error.strerror}"
        ) from error
    except tomllib.TOMLDecodeError as error:
        raise SettingsError(f"{path} is not valid TOML: {error}") from error
    try:
        return Settings(
            source_url=str(raw["source_url"]),
            timeout=float(raw["timeout"]),
            output_dir=Path(raw["output_dir"]),
            seed=int(raw["seed"]),
            sample_size=int(raw["sample_size"]),
            log_level=str(raw["log_level"]),
        )
    except KeyError as error:
        raise SettingsError(f"{path} is missing the setting {error}.") from error
    except (TypeError, ValueError) as error:
        raise SettingsError(
            f"{path} has a setting of the wrong type: {error}"
        ) from error
