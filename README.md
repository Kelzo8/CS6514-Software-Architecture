# CS6514 - Software Architecture Repo

By Nandakishore Vinayakrishnan - 23070854

## Week 5 EVA analysis application

The Week 5 application analyzes EVA duration data from `Week-5/eva-data.json`. It reports duration categories and all-time country totals, creates a cumulative-duration plot, and compares two countries' EVA counts and durations over an inclusive year range.

### Requirements

- Python 3.9 or later.
- Matplotlib, used to create the cumulative-duration plot.

### Set up

From the repository root, create and activate a virtual environment, then install Matplotlib:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install matplotlib
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

### Run the application

From the repository root:

```bash
cd Week-5
python evacodev2.py
```

Enter two country names found in the dataset, then a start year and end year. The period includes both endpoint years. The existing aliases `USSR` and `America` are accepted for Russia and USA. The application reads the data file from the `Week-5` directory and saves `cumulative_duration.png` in the current working directory. It also displays the chart when the active Matplotlib backend supports a display window.

#### Example

For a comparison of USA and Russia in 1965, enter:

```text
Enter the first country (USA, or Russia): USA
Enter the second country (USA, or Russia): Russia
Enter the start year: 1965
Enter the end year: 1965
```

The report includes both endpoint years. For the supplied data, it looks like this:

```text
EVA activity comparison (1965–1965, inclusive):
USA:
  Total number of EVAs: 1
  Total EVA duration: 0.60 hours
  Average EVA duration: 0.60 hours
Russia:
  Total number of EVAs: 0
  Total EVA duration: 0.00 hours
  Average EVA duration: unavailable
Greater total EVA duration: USA
```

If you enter 2020 and 2021, neither country has a matching EVA in the supplied data. Both averages are reported as unavailable and the comparison reports a tie.

### Module structure

| Module | Responsibility |
|---|---|
| `data_loader.py` | Reads JSON data and returns raw EVA records. |
| `data_preparation.py` | Validates records and prepares parsed dates, durations, and diagnostics. |
| `analysis.py` | Calculates duration categories, country totals, cumulative hours, and selected-period comparisons. |
| `presentation.py` | Collects and validates user input, formats results, and creates and displays the plot. |
| `app.py` | Coordinates the application workflow and connects the other modules. |
| `evacodev2.py` | Compatibility entry point that launches `app.main()`. |

### Run the automated tests

The tests use Python's standard `unittest` library. From the repository root:

```bash
cd Week-5
python -m unittest -v
```

### Architecture documentation

The module dependency diagram, interfaces, architectural rationale, and architectural decision records are documented in [Week-5/ARCHITECTURE.md](Week-5/ARCHITECTURE.md). It contains **ADR-001** for the modular structure and **ADR-002** for the period-comparison feature, along with test evidence and a maintainability evaluation.

### Repository layout

- `Week-1/` and `Week-2/` contain earlier course work.
- `Week-5/` contains the modular EVA analysis application, its source data, tests, and architecture documentation.
