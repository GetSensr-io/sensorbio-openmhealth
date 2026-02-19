from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Iterable


def to_iso_string(timestamp_ms: int) -> str:
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def clamp01(x: float) -> float:
    if x < 0:
        return 0.0
    if x > 1:
        return 1.0
    return x


def iso_date_list(start_date: str, end_date: str) -> list[str]:
    """Inclusive list of YYYY-MM-DD strings in UTC."""
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError as e:
        raise ValueError("Invalid date range; expected YYYY-MM-DD") from e

    if end < start:
        return []

    days: list[str] = []
    d = start
    while d <= end:
        days.append(d.isoformat())
        d += timedelta(days=1)
    return days


@dataclass(frozen=True)
class TimeInterval:
    start_date_time: str
    end_date_time: str


def interval_from_ms(start_ms: int, end_ms: int) -> TimeInterval:
    return TimeInterval(start_date_time=to_iso_string(start_ms), end_date_time=to_iso_string(end_ms))


def as_utc_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


def ensure_ms_range(start_date: str, end_date: str) -> tuple[int, int]:
    start_dt = datetime.fromisoformat(f"{start_date}T00:00:00+00:00")
    end_dt = datetime.fromisoformat(f"{end_date}T23:59:59.999000+00:00")
    return int(start_dt.timestamp() * 1000), int(end_dt.timestamp() * 1000)
