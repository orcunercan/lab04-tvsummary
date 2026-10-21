"""Logging configuration. Only the entry point calls configure_logging."""

import logging


def configure_logging(level: str) -> None:
    """Show log messages at this level and above, with time, level and module."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
