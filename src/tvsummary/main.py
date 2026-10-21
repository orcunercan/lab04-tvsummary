"""Entry point. Run it with: python -m tvsummary.main [--config PATH]"""

import argparse
import logging
import sys
from pathlib import Path

from tvsummary.config import DEFAULT_SETTINGS_PATH, load_settings
from tvsummary.errors import TVSummaryError
from tvsummary.logging_setup import configure_logging
from tvsummary.report import build_run_info, build_summary, write_json
from tvsummary.sources import TVMazeSource

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    """Read the command-line options. Only --config is supported."""
    parser = argparse.ArgumentParser(description="Summarize TV show records.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_SETTINGS_PATH,
        help="path to the TOML settings file",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the program and return its exit code: 0 for success, 1 for failure."""
    args = parse_args(argv)
    configure_logging("INFO")
    try:
        settings = load_settings(args.config)
        logging.getLogger().setLevel(settings.log_level)
        shows = TVMazeSource(settings.source_url, settings.timeout).fetch()
        summary = build_summary(shows, settings)
        summary_path = settings.output_dir / "summary.json"
        write_json(summary, summary_path)
        write_json(build_run_info(settings), settings.output_dir / "run_info.json")
    except TVSummaryError as error:
        logger.error("Stopped: %s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Processed {summary['records_processed']} shows.")
    print(f"Summary written to {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
