"""Utilities."""

from datetime import datetime


def dirname_now():
    """A directory with the current time as its name."""
    now = datetime.now()
    return now.isoformat(timespec="microseconds").replace(":", "-").replace(".", "_")
