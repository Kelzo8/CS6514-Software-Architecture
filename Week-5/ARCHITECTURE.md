# Activity 2: Proposed Structure and Architectural Decisions

## Modular structure

| Module | Responsibility | Interface |
|---|---|---|
| `data_loader.py` | Read and decode the EVA JSON source. | `load_eva_data(path) -> list[dict]` |
| `data_preparation.py` | Validate source values, parse dates and durations, and produce prepared records and diagnostics. | `prepare_records(raw_records) -> PreparedData` |
| `analysis.py` | Calculate existing categories, country totals and cumulative hours, plus the new period comparison. | `analyze(prepared_data, country_a, country_b) -> AnalysisResult`; `compare_countries_for_period(prepared_data, country_a, country_b, start_year, end_year) -> PeriodComparison` |
| `presentation.py` | Collect and validate user input; format summaries and show/save the cumulative plot. | `prompt_country(...)`, `prompt_year_range()`, `present(result)`, `present_period_comparison(result)` |
| `app.py` | Coordinate loading, preparation, prompts, analysis, and presentation. | `main() -> None` |
| `evacodev2.py` | Compatibility entry point for running the application. | `python evacodev2.py` |

### Dependencies and interfaces

```text
evacodev2.py (entry point)
└── app.py (workflow coordinator)
    ├── data_loader.py
    │   └── returns raw records to app.py
    ├── data_preparation.py
    │   └── receives raw records; returns PreparedData to app.py
    ├── analysis.py
    │   └── receives PreparedData and country/year selections;
    │       returns analysis results to app.py
    └── presentation.py
        ├── prompts app.py for country and year selections
        └── receives results from app.py for display and plotting
```

The modules communicate through function arguments and return values. `app.py` coordinates the workflow. Analysis consumes prepared records and returns result objects; it does not read files, prompt users, print reports, or draw charts. Presentation accepts and displays results without knowing how JSON is loaded.

## ADR-001: Separate EVA workflow responsibilities into cohesive modules

### Context

The inherited Week 5 application combined JSON reading, record validation, calculations, prompts, output, charting, and execution flow in a single source file. This tied analysis to the data format and display implementation, and made responsibilities difficult to change independently.

### Alternatives

1. Keep one file and organize it into sections.
2. Split into a few broad files, risking continued mixing of responsibilities.
3. Split by workflow responsibility into loading, preparation, analysis, presentation, and coordination modules with explicit interfaces.

### Decision

Choose alternative 3. Use the modules shown above, with `app.py` as the coordinator and `evacodev2.py` as the compatibility entry point.

### Rationale

The loader handles JSON, preparation parses and validates records, analysis does the calculations, presentation handles prompts and output, and the app runs the steps in order. A change to one of these jobs should usually stay in its module.

### Consequences

- **Benefits:** clearer responsibilities, changes limited to the relevant module, and analysis that can be called without loading files or displaying results.
- **Trade-offs:** more files and interfaces must be maintained, and data must be passed between modules.
- **Constraints:** preserve existing country aliases, duration categories, all-time totals and comparison, malformed-record handling, and cumulative plot behavior.

## ADR-002: Add period comparison through existing analysis and presentation modules

### Context

Researchers need to compare two countries' EVA count and duration over an inclusive year range. The application must handle equal totals, countries with no matching EVAs, invalid year ranges, and unknown countries without terminating. The feature should fit the existing architecture and reuse calculations where possible.

### Alternatives

1. Put filtering, calculations, prompts, and output in `app.py`, which would mix coordination with analysis and presentation.
2. Create a separate comparison module with its own aggregation logic, adding another module and risking duplicated calculations.
3. Add a period-comparison function to `analysis.py`, input and formatting functions to `presentation.py`, and connect them in `app.py`.

### Decision

Choose alternative 3. `compare_countries_for_period` accepts prepared data, country names, and start/end years; it returns a `PeriodComparison`. The end points are inclusive. Input validation and result formatting are handled by `presentation.py`; `app.py` coordinates the existing and new operations. Existing and period country totals share an aggregation helper.

### Rationale

The comparison is an analysis operation, while prompting and reporting belong to presentation. The existing prepared-record interface supplies the needed dates, countries, and durations, so the loader and preparation modules do not need changes. Direct function interfaces also make calculations independently testable.

### Consequences

- **Benefits:** inclusive period logic is isolated and testable; existing total aggregation is reused; invalid inputs can be reprompted at the UI boundary.
- **Limitations:** `analysis.py` now owns both all-time and period analysis, and the app presents both operations in sequence.
- **Trade-offs:** result dataclasses and year prompts add modest structure; no new framework or runtime dependency was added. Tests use Python's built-in `unittest`.

## Activity 5: Test evidence and maintainability evaluation

Run `python3 -m unittest -v` from `Week-5`: **5 tests passed**. Tests use known records and expected values to check the inclusive year range, counts, totals, averages, zero-match behavior, unavailable average, ties, an existing category and country-total operation, and reprompting for an unknown country and reversed range.

A smoke run of `evacodev2.py` with USA, Russia, and the years 2020 to 2021 retained the existing all-time categories, totals, comparison, and plot output, then displayed the new comparison. The dataset has no EVAs in those years, so both counts and totals were zero, averages were unavailable, and the comparison reported a tie. The noninteractive chart backend could not display a window, but the plot was saved.

Three production modules changed for the new requirement: `analysis.py`, `presentation.py`, and `app.py`. The loader and preparation modules remain unchanged. Tests call analysis directly with prepared records, without file reading or display. Responsibilities remain identifiable, duration aggregation is shared, and the added complexity is limited to the comparison result, calculation, and input handling needed by the requirement.
