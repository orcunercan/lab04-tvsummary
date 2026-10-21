"""Entry point: download the shows, build the summary and write it to a file."""

import logging
import sys

from tvsummary import config
from tvsummary.errors import TVSummaryError
from tvsummary.logging_setup import configure_logging
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import TVMazeSource

logger = logging.getLogger(__name__)


def main():
    configure_logging("INFO")
    source = TVMazeSource(config.SOURCE_URL, config.TIMEOUT)
    try:
        shows = source.fetch()
    except TVSummaryError as error:
        logger.error("Stopped: %s", error)
        sys.exit(str(error))

    summary = build_summary(shows, config.SOURCE_URL)
    write_summary(summary, config.OUTPUT_PATH)
    print(f"Processed {summary['records_processed']} shows.")
    print(f"Summary written to {config.OUTPUT_PATH}")


if __name__ == "__main__":
    main()
