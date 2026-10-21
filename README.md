# TV Shows Summary (tvsummary)

An installable Python package that downloads TV show records from the TVmaze API and summarizes them: shows per genre, shows without a genre, average rating by language, the number of unrated shows, and a short list of featured shows chosen at random from a fixed seed. This is the Lab 03 package hardened with tests, its own errors, logging, type hints, linting and a settings file.

## Setup

```
conda env create -f environment.yml
conda activate tvsummary-lab04
pip install -r requirements.txt
pip install -e .
```

## Run

```
python -m tvsummary.main
python -m tvsummary.main --config config/tvsummary.toml
```

The program writes `data/processed/summary.json` and `data/processed/run_info.json`. Without `--config` it reads `config/tvsummary.toml`.

## Check it

```
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
```

All four pass. The settings for ruff, mypy and pytest are in `pyproject.toml`, so everyone gets the same results.

## Settings

All settings are in `config/tvsummary.toml`:

- `source_url`: the TVmaze API address the shows are downloaded from.
- `timeout`: how many seconds to wait for the download before giving up.
- `output_dir`: the folder where `summary.json` and `run_info.json` are written.
- `seed`: the seed for the random generator that picks the featured shows.
- `sample_size`: how many featured shows to pick.
- `log_level`: which log messages are shown (`DEBUG`, `INFO`, `WARNING` or `ERROR`).

## Errors and exit codes

Every error the package raises on purpose belongs to one family, defined in `errors.py`. Only `main()` catches them.

| Error class | When it is raised | What the user sees |
|---|---|---|
| `TVSummaryError` | Base class of the family; never raised directly | Caught in `main()` to cover every case below |
| `SettingsError` | The settings file is missing, is not valid TOML, lacks a setting, or has a value of the wrong type | `Error: Cannot read the settings file ...` or `Error: ... is missing the setting ...` |
| `SourceError` | The download fails: no network, a timeout, or an HTTP error from the server | `Error: Could not reach https://api.tvmaze.com/...` |
| `DataShapeError` | The response is not valid JSON, is not a list, or contains a record that is not a JSON object | `Error: Expected a list of shows, ...` or a similar one-line message |

Each failure is also logged at ERROR level, and the program stops without a traceback.

- **Exit code 0**: the run succeeded and both output files were written.
- **Exit code 1**: an expected failure from the table above stopped the run.

A traceback appears only for a bug, which is a mistake in the code rather than an expected failure.

## Reproducing a run

The seed is in `config/tvsummary.toml` (`seed = 42`, `sample_size = 5`). The featured shows are chosen with a private `random.Random(seed)` generator, so the same seed always gives the same list. With the committed settings the list is:

```
How I Met Your Mother, American Horror Story, Homeland, The Fosters, The Walking Dead
```

Each run writes `data/processed/run_info.json`, which records every setting used, the Python version, and the versions of pytest, mypy and ruff.

To get exactly the same `featured_shows` list, a classmate also needs:

- the same settings file, especially `seed`, `sample_size` and `source_url`;
- the same input data, because the list is drawn from the shows the API returns, and TVmaze can change the first page over time;
- the same Python version (fixed at 3.11 in `environment.yml`), because the random generator's output can change between Python versions;
- the same package versions, pinned in `requirements.txt`.

## What the tests cover

The suite in `tests/` has 32 tests and needs no network. Shared fixtures are in `tests/conftest.py`.

- **`Show`**: a complete record keeps its values; a missing, `null` or empty genre list becomes an empty list; a missing or `null` rating becomes `None` (parametrized tests).
- **Aggregations**: each aggregation class is tested on hand-made records, including the seeded `FeaturedShows`, where a test proves that the same seed gives the same list. One test uses `caplog` to check the warning logged for a skipped show.
- **Sources**: a failed download raises `SourceError` (using `monkeypatch` to make `requests.get` fail), and data with the wrong shape raises `DataShapeError` (`pytest.raises` with `match`).
- **Settings**: a complete file is read, settings cannot be changed afterwards, and a missing or incomplete file raises `SettingsError` (using `tmp_path`).
- **`main()`**: a missing settings file and a failed download both return exit code 1 and print a line starting with `Error:`; a successful run returns 0 and writes both files into a temporary folder.

**Not tested:** the real download from TVmaze. A test that depends on the internet fails whenever the network or the API does, so it would not be trusted. The network path is covered with a fake `requests.get` instead, and the real download is checked by running the program.

## Known limitations

- Only the first page of the API (240 shows) is downloaded, so only two languages appear in the averages.
- Averages are not weighted by how many ratings each show has on TVmaze.
- An unknown `log_level` value in the settings file (for example `"LOUD"`) is not checked when the settings are loaded and stops the program with a traceback.
- The featured shows depend on what the API returns, so the list can change if TVmaze changes its first page, even with the same seed.
- The list of aggregations is fixed inside `build_summary`.