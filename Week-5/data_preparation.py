from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class PreparedRecord:
    date: datetime
    duration_hours: float
    country: str


@dataclass(frozen=True)
class PreparedData:
    """Validated dated records, category durations, and legacy diagnostics."""

    records: tuple[PreparedRecord, ...]
    category_durations: tuple[float, ...]
    diagnostics: tuple[str, ...]


def _duration_in_hours(duration_text: Any) -> float:
    hours, minutes = map(int, duration_text.split(":"))
    return hours + minutes / 60


def prepare_records(raw_records: list[dict[str, Any]]) -> PreparedData:
    """Parse records while preserving the original script's skip/report rules."""
    records: list[PreparedRecord] = []
    category_durations: list[float] = []
    diagnostics: list[str] = []

    for eva in raw_records:
        date_text = eva.get("date")
        duration_text = eva.get("duration")
        country = eva.get("country")

        if not duration_text:
            continue

        try:
            duration_hours = _duration_in_hours(duration_text)
        except (TypeError, ValueError):
            if date_text and country:
                diagnostics.append("Malformed time/duration")
            continue

        category_durations.append(duration_hours)

        if not date_text or not country:
            continue

        try:
            date = datetime.fromisoformat(date_text)
        except (TypeError, ValueError):
            diagnostics.append("Malformed time/duration")
            continue

        records.append(PreparedRecord(date, duration_hours, country))

    return PreparedData(tuple(records), tuple(category_durations), tuple(diagnostics))
