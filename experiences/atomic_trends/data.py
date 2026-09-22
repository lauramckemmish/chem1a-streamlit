"""Loading and filtering for the local atomic-trends reference data."""

from __future__ import annotations

import csv
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "atomic_trends" / "elements.csv"

PROPERTY_METADATA = {
    "First ionisation energy": ("first_ionisation_energy_kj_mol", "First ionisation energy", "kJ mol⁻¹"),
    "Atomic radius": ("atomic_radius_pm", "Atomic radius", "pm"),
    "Electronegativity": ("electronegativity_pauling", "Electronegativity", "Pauling scale"),
}


def elements() -> list[dict[str, object]]:
    """Return local reference rows, retaining absent reference values as None."""
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    parsed: list[dict[str, object]] = []
    for row in rows:
        parsed.append(
            {
                "atomic_number": int(row["atomic_number"]),
                "symbol": row["symbol"],
                "element_name": row["element_name"],
                "period": int(row["period"]),
                "group": int(row["group"]) if row["group"].isdigit() else None,
                "atomic_radius_pm": float(row["atomic_radius_pm"]) if row["atomic_radius_pm"] else None,
                "first_ionisation_energy_kj_mol": float(row["first_ionisation_energy_kj_mol"])
                if row["first_ionisation_energy_kj_mol"]
                else None,
                "electronegativity_pauling": float(row["electronegativity_pauling"])
                if row["electronegativity_pauling"]
                else None,
            }
        )
    return parsed


def selected_elements(mode: str, selections: list[int]) -> list[dict[str, object]]:
    """Filter a complete local table without inventing values or ordering."""
    rows = elements()
    if mode == "Periods":
        return [row for row in rows if row["period"] in selections]
    if mode == "Groups":
        return [row for row in rows if row["group"] in selections]
    return rows


def series_for_selection(mode: str, selections: list[int], property_key: str) -> list[dict[str, object]]:
    """Return only available property values, grouped into natural-order series."""
    rows = selected_elements(mode, selections)
    available = [row for row in rows if row[property_key] is not None]
    if mode == "All elements":
        return [{**row, "series": "All elements"} for row in available]
    series_key = "period" if mode == "Periods" else "group"
    return [{**row, "series": f"{series_key.title()} {row[series_key]}"} for row in available]
