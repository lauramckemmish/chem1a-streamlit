"""Loading and filtering for the local atomic-trends reference data."""

from __future__ import annotations

import csv
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "atomic_trends" / "elements.csv"

PROPERTY_METADATA = {
    "First ionisation energy": ("first_ionisation_energy_kj_mol", "First ionisation energy", "kJ mol⁻¹"),
    "Covalent atomic radius": ("covalent_atomic_radius_pm", "Covalent atomic radius", "pm"),
    "Electron affinity": ("electron_affinity_kj_mol", "Electron affinity", "kJ mol⁻¹"),
    "Pauling electronegativity": ("electronegativity_pauling", "Pauling electronegativity", "Pauling scale"),
    "Effective nuclear charge": ("effective_nuclear_charge", "Effective nuclear charge", "elementary charge"),
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
                "covalent_atomic_radius_pm": float(row["covalent_atomic_radius_pm"])
                if row["covalent_atomic_radius_pm"]
                else None,
                "first_ionisation_energy_kj_mol": float(row["first_ionisation_energy_kj_mol"])
                if row["first_ionisation_energy_kj_mol"]
                else None,
                "electron_affinity_kj_mol": float(row["electron_affinity_kj_mol"])
                if row["electron_affinity_kj_mol"]
                else None,
                "electronegativity_pauling": float(row["electronegativity_pauling"])
                if row["electronegativity_pauling"]
                else None,
                "effective_nuclear_charge": float(row["effective_nuclear_charge"])
                if row["effective_nuclear_charge"]
                else None,
                "effective_nuclear_charge_orbital": row["effective_nuclear_charge_orbital"] or None,
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
    """Return complete selected series, retaining unavailable values as None."""
    rows = selected_elements(mode, selections)
    if mode == "All elements":
        return [{**row, "series": "All elements"} for row in rows]
    series_key = "period" if mode == "Periods" else "group"
    return [{**row, "series": f"{series_key.title()} {row[series_key]}"} for row in rows]
