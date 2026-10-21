"""Entry point: download the shows, build the summary and write it to a file."""

import sys

from tvsummary import config
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import DownloadError, TVMazeSource


def main():
    source = TVMazeSource(config.SOURCE_URL, config.TIMEOUT)
    try:
        shows = source.fetch()
    except DownloadError as error:
        sys.exit(str(error))

    summary = build_summary(shows, config.SOURCE_URL)
    write_summary(summary, config.OUTPUT_PATH)
    print(f"Processed {summary['records_processed']} shows.")
    print(f"Summary written to {config.OUTPUT_PATH}")


if __name__ == "__main__":
    main()