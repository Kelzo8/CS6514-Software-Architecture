from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_DATA_PATH = Path(__file__).with_name("eva-data.json")


def load_eva_data(path: str | Path = DEFAULT_DATA_PATH) -> list[dict[str, Any]]:
    """Load and return EVA dictionaries from a JSON file."""
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)
