# TV Shows Summary (tvsummary)

An installable Python package that downloads TV show records from the TVmaze API, counts shows per genre, lists shows without a genre, averages ratings by language, counts unrated shows, and writes the results to a JSON file. This is the Lab 02 program restructured into classes and modules, with the same output.

## Data source

https://api.tvmaze.com/shows?page=0

Each record is one TV show, with fields such as name, language, genres and rating. The first page returns 240 shows.

## Setup

```
conda env create -f environment.yml
conda activate tvsummary
pip install -r requirements.txt
pip install -e .
```

## Run

```
python main.py
```

The summary is written to `data/processed/summary.json`. If the download fails, for example with no internet connection, the program prints a clear message and exits without a traceback.

## Test

```
python -m unittest discover -s tests
```

The tests use handmade records and need no network.

## Layout

- `main.py`: thin entry point. Wires the pieces together and prints messages, including the error message when the download fails.
- `src/tvsummary/__init__.py`: re-exports the public names, so a user can write `from tvsummary import Show`.
- `src/tvsummary/config.py`: the source URL, timeout and output path, so every setting lives in one place.
- `src/tvsummary/models.py`: the `Show` class, one cleaned record. Separate because every other module depends on it.
- `src/tvsummary/sources.py`: `TVMazeSource` and `DownloadError`. The only module that imports `requests`, so the network dependency is isolated.
- `src/tvsummary/aggregations.py`: the `Aggregation` base class and its four subclasses.
- `src/tvsummary/report.py`: builds the summary dictionary and writes it as JSON.
- `tests/test_models.py`: unit tests for `Show` and two aggregations.

## What moved where

| Lab 02 (`records.py`) | Lab 03 |
|---|---|
| `SOURCE_URL`, `OUTPUT` constants, timeout written inside `fetch_records` | `config.py`: `SOURCE_URL`, `TIMEOUT`, `OUTPUT_PATH` |
| `fetch_records` | `sources.py`: `TVMazeSource.fetch`, now returns `Show` objects |
| Missing-value checks repeated across functions, e.g. `show.get("genres") or []` and `(show.get("rating") or {}).get("average")` | `models.py`: `Show.__init__` |
| `shows_per_genre` | `aggregations.py`: `GenreCounts.compute` |
| `shows_without_genre` | `aggregations.py`: `ShowsWithoutGenre.compute` |
| `rating_totals_by_language` and `average_rating_by_language` | `aggregations.py`: `AverageRatingByLanguage.compute` |
| `count_unrated` | `aggregations.py`: `UnratedCount.compute` |
| `build_summary` | `report.py`: `build_summary`, now loops over aggregation objects |
| `write_summary` | `report.py`: `write_summary`, now also creates the output folder |
| `main`, catching `requests.RequestException` | `main.py`: `main`, catching `DownloadError`; `TVMazeSource.fetch` converts the `requests` error |

## Design choices

- **`Show`** exists so that missing or malformed data is handled in one place. In Lab 02 the nested rating check was written twice, in two different functions. Now `Show.__init__` guarantees that `genres` is always a list and that `rating` and `language` are either a value or `None`, so the rest of the code can use `show.genres` and `show.rating` directly.
- **`TVMazeSource`** keeps the URL and timeout together and turns raw dictionaries into `Show` objects. It also converts network errors into its own `DownloadError`, so `main.py` can report a failed download without importing `requests`.
- **`Aggregation` and its subclasses** use inheritance because every calculation has the same shape: take a list of shows, return one result, store it under a key in the summary. The base class provides the `key` and the `compute` method that every subclass overrides. `build_summary` loops over a list of aggregation objects and calls `compute` on each one without checking which subclass it is.
- **Adding one more aggregation** only needs a new subclass that calls `super().__init__("its_key")` and overrides `compute`, plus one more object in the list in `build_summary`. No other code changes.
- **Same output as Lab 02.** The calculation order and rounding were kept, and the new `summary.json` was compared with the Lab 02 one using `git diff --no-index`; the files are identical.

## Known limitations

- Only the first page of the API (240 shows) is downloaded, so only two languages appear in the averages.
- Averages are not weighted by how many ratings each show has on TVmaze.
- The list of aggregations is fixed inside `build_summary`. Choosing them from outside would need an extra parameter.
- The tests cover `Show` and two of the four aggregations.
- Messages are printed rather than logged.