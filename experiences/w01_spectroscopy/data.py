"""Read-only access to the bounded CHEM 1A spectroscopy source layer."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path


DATA_DIRECTORY = Path(__file__).resolve().parents[2] / "data" / "spectroscopy"
STAGE_1_SPECIES = frozenset({"H", "He", "Na", "Ne", "Hg"})


def _read_csv(filename: str) -> list[dict[str, str]]:
    with (DATA_DIRECTORY / filename).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def source_lines() -> list[dict[str, str]]:
    """Return bounded NIST source/reference rows without pedagogical filtering."""
    return _read_csv("source_lines.csv")


def display_features() -> list[dict[str, str]]:
    """Return curated teaching features with their source-row identifiers."""
    return _read_csv("display_features.csv")


def stage_1_comparison_features() -> list[dict[str, str]]:
    """Return selected visible comparison features for the approved neutral species."""
    return [
        feature
        for feature in display_features()
        if feature["show_compare_atoms"] == "true"
    ]


def hydrogen_detail_features() -> list[dict[str, str]]:
    """Return the richer six-feature hydrogen Balmer selection for Stage 2."""
    return [
        feature
        for feature in display_features()
        if feature["show_hydrogen_detail"] == "true"
    ]


def hydrogen_series_features() -> list[dict[str, str]]:
    """Return bounded NIST main-series references for later Stage 4 use."""
    return _read_csv("hydrogen_series.csv")


def angstrom_to_nm(wavelength_angstrom: str | float | Decimal) -> Decimal:
    """Convert an Angstrom value to nm using the exact 0.1 factor."""
    return Decimal(str(wavelength_angstrom)) * Decimal("0.1")
