from analysis import analyze, compare_countries_for_period
from data_loader import DEFAULT_DATA_PATH, load_eva_data
from data_preparation import prepare_records
from presentation import (
    present,
    present_period_comparison,
    prompt_country,
    prompt_year_range,
)


def main(data_path=DEFAULT_DATA_PATH) -> None:
    raw_records = load_eva_data(data_path)
    prepared_data = prepare_records(raw_records)
    known_countries = sorted({record.country for record in prepared_data.records})
    first_country = prompt_country(
        "Enter the first country (USA, or Russia): ", known_countries
    )
    second_country = prompt_country(
        "Enter the second country (USA, or Russia): ", known_countries
    )
    result = analyze(prepared_data, first_country, second_country)
    present(result)

    start_year, end_year = prompt_year_range()
    comparison = compare_countries_for_period(
        prepared_data, first_country, second_country, start_year, end_year
    )
    present_period_comparison(comparison)


if __name__ == "__main__":
    main()
