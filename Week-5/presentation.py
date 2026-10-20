import matplotlib.pyplot as plt

from analysis import AnalysisResult, PeriodComparison


def prompt_country(prompt: str, allowed_countries=("USA", "Russia")) -> str:
    allowed_countries = tuple(sorted(set(allowed_countries)))
    while True:
        country = input(prompt).strip()
        if country in allowed_countries:
            return country
        if country == "USSR" and "Russia" in allowed_countries:
            return "Russia"
        if country == "America" and "USA" in allowed_countries:
            return "USA"
        choices = ", ".join(allowed_countries)
        print(f"Unknown country. Please enter one of: {choices}.")


def prompt_year_range() -> tuple[int, int]:
    while True:
        try:
            start_year = int(input("Enter the start year: ").strip())
            end_year = int(input("Enter the end year: ").strip())
        except ValueError:
            print("Invalid year. Please enter whole-number years.")
            continue
        if start_year > end_year:
            print("Invalid year range. Start year must not exceed end year.")
            continue
        return start_year, end_year


def present(result: AnalysisResult) -> None:
    """Print analysis results and save/display the cumulative-hours plot."""
    for diagnostic in result.diagnostics:
        print(diagnostic)

    category_total = sum(result.category_counts.values())
    print("EVA duration categories:")
    for category, count in result.category_counts.items():
        percentage = count / category_total * 100 if category_total else 0
        print(f"{category}: {count} ({percentage:.2f}%)")

    print(
        f"{result.first_country} total EVA duration: "
        f"{result.first_country_total:.2f} hours"
    )
    print(
        f"{result.second_country} total EVA duration: "
        f"{result.second_country_total:.2f} hours"
    )
    print(f"Greater total: {result.greater_country}")

    plt.plot(result.cumulative_dates, result.cumulative_hours)
    plt.xlabel("Year")
    plt.ylabel("Cumulative EVA duration (hours)")
    plt.tight_layout()
    plt.savefig("cumulative_duration.png")
    plt.show()


def present_period_comparison(result: PeriodComparison) -> None:
    print(
        f"EVA activity comparison ({result.start_year}–{result.end_year}, inclusive):"
    )
    for summary in (result.country_a, result.country_b):
        average = (
            f"{summary.average_duration_hours:.2f} hours"
            if summary.average_duration_hours is not None
            else "unavailable"
        )
        print(f"{summary.country}:")
        print(f"  Total number of EVAs: {summary.eva_count}")
        print(f"  Total EVA duration: {summary.total_duration_hours:.2f} hours")
        print(f"  Average EVA duration: {average}")
    print(f"Greater total EVA duration: {result.greater_total_country}")
