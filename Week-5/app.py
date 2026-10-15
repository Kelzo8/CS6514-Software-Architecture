from analysis import analyze
from data_loader import DEFAULT_DATA_PATH, load_eva_data
from data_preparation import prepare_records
from presentation import present, prompt_country


def main(data_path=DEFAULT_DATA_PATH) -> None:
    raw_records = load_eva_data(data_path)
    first_country = prompt_country("Enter the first country (USA, or Russia): ")
    second_country = prompt_country("Enter the second country (USA, or Russia): ")
    prepared_data = prepare_records(raw_records)
    result = analyze(prepared_data, first_country, second_country)
    present(result)


if __name__ == "__main__":
    main()
