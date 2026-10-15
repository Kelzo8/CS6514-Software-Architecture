from dataclasses import dataclass

from data_preparation import PreparedData


CATEGORY_NAMES = ("Short", "Standard", "Long")


@dataclass(frozen=True)
class AnalysisResult:
    category_counts: dict[str, int]
    country_totals: dict[str, float]
    first_country: str
    second_country: str
    first_country_total: float
    second_country_total: float
    greater_country: str
    cumulative_dates: tuple
    cumulative_hours: tuple[float, ...]
    diagnostics: tuple[str, ...]


def analyze(
    prepared_data: PreparedData, first_country: str, second_country: str
) -> AnalysisResult:
    """Calculate category counts, country totals, and cumulative EVA hours."""
    category_counts = {name: 0 for name in CATEGORY_NAMES}
    for duration_hours in prepared_data.category_durations:
        if duration_hours < 4:
            category_counts["Short"] += 1
        elif duration_hours < 7:
            category_counts["Standard"] += 1
        else:
            category_counts["Long"] += 1

    country_totals: dict[str, float] = {}
    for record in prepared_data.records:
        country_totals[record.country] = (
            country_totals.get(record.country, 0.0) + record.duration_hours
        )

    sorted_records = sorted(prepared_data.records, key=lambda record: record.date)
    cumulative_dates = []
    cumulative_hours = []
    total_hours = 0.0
    for record in sorted_records:
        total_hours += record.duration_hours
        cumulative_dates.append(record.date)
        cumulative_hours.append(total_hours)

    first_total = country_totals.get(first_country, 0.0)
    second_total = country_totals.get(second_country, 0.0)
    if first_total > second_total:
        greater_country = first_country
    elif second_total > first_total:
        greater_country = second_country
    else:
        greater_country = "Neither country; both totals are equal"

    return AnalysisResult(
        category_counts=category_counts,
        country_totals=country_totals,
        first_country=first_country,
        second_country=second_country,
        first_country_total=first_total,
        second_country_total=second_total,
        greater_country=greater_country,
        cumulative_dates=tuple(cumulative_dates),
        cumulative_hours=tuple(cumulative_hours),
        diagnostics=prepared_data.diagnostics,
    )
