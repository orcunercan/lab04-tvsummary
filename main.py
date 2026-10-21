"""Entry point: download the shows, build the summary and write it to a file."""

import logging
import sys

from tvsummary.config import DEFAULT_SETTINGS_PATH, load_settings
from tvsummary.errors import TVSummaryError
from tvsummary.logging_setup import configure_logging
from tvsummary.report import build_run_info, build_summary, write_json
from tvsummary.sources import TVMazeSource

logger = logging.getLogger(__name__)


def main():
    try:
        settings = load_settings(DEFAULT_SETTINGS_PATH)
    except TVSummaryError as error:
        sys.exit(str(error))
    configure_logging(settings.log_level)
    try:
        shows = TVMazeSource(settings.source_url, settings.timeout).fetch()
    except TVSummaryError as error:
        logger.error("Stopped: %s", error)
        sys.exit(str(error))

    summary = build_summary(shows, settings)
    write_json(summary, settings.output_dir / "summary.json")
    write_json(build_run_info(settings), settings.output_dir / "run_info.json")
    print(f"Processed {summary['records_processed']} shows.")
    print(f"Summary written to {settings.output_dir / 'summary.json'}")


if __name__ == "__main__":
    main()
