"""Manage Metrics."""

import csv
from datetime import datetime
from zoneinfo import ZoneInfo

from beartype import beartype
from pydantic import BaseModel

from .typing import Keys
from .uninstall import get_cache_dir


@beartype
def utcnow() -> datetime:
    """Return the current time in UTC."""
    return datetime.now(tz=ZoneInfo('UTC'))


class SessionMetrics(BaseModel):
    """Session metrics."""

    filename: str
    session_start: datetime
    session_end: datetime | None = None
    typed_correct: int = 0
    typed_incorrect: int = 0

    @classmethod
    def from_filename(cls, filename: str) -> 'SessionMetrics':  # noqa: RBT002
        """Initialize Metrics based on the filename."""
        return cls(filename=filename, session_start=utcnow())

    def end_session(self, keys: Keys) -> 'SessionMetrics':  # noqa: RBT002
        """Update the typed counters based on `Keys`."""
        self.session_end = utcnow()
        for key in keys.typed_all:
            if key.expected:
                if key.was_correct:
                    self.typed_correct += 1
                else:
                    self.typed_incorrect += 1
        return self


@beartype
def append_csv(metrics: SessionMetrics) -> None:
    """Write metrics to the global CSV."""
    csv_path = get_cache_dir() / 'metrics.csv'

    csv_columns = ['filename', 'session_start', 'session_end', 'typed_correct', 'typed_incorrect']
    if not csv_path.is_file():
        csv_path.parent.mkdir(exist_ok=True, parents=True)
        with csv_path.open(mode='w', newline='', encoding='utf-8') as _f:
            csv.writer(_f).writerow(csv_columns)  # nosemgrep

    ser_metrics = metrics.dict()
    metrics_row = [ser_metrics[_c] for _c in csv_columns]
    with csv_path.open('a', newline='', encoding='utf-8') as _f:
        csv.writer(_f).writerow(metrics_row)  # nosemgrep
