import matplotlib.pyplot as plt

from analysis import AnalysisResult


def prompt_country(prompt: str) -> str:
    while True:
        country = input(prompt).strip()
        if country in ("USA", "Russia"):
            return country
        if country == "USSR":
            return "Russia"
        if country == "America":
            return "USA"
        print("Invalid country. Please enter USA, Russia, or USSR.")


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
