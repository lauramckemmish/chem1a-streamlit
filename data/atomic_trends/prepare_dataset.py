"""Create the checked local Periodic trends teaching-data snapshot.

This is a preparation tool, not part of the Streamlit runtime. It combines the
PubChem PUG periodic-table response with the reputable `mendeleev` scientific
data package's explicit Cordero covalent-radius and Clementi--Raimondi
screening-constant fields. Run with a locally saved PubChem response to make
the source snapshot used for a release inspectable.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.request import urlopen

from mendeleev import element


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "elements.csv"
OUTPUT_PATH = ROOT / "elements.csv"
PUBCHEM_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/JSON"
EV_TO_KJ_MOL = 96.4853321233
FIELDS = (
    "atomic_number", "symbol", "element_name", "period", "group",
    "covalent_atomic_radius_pm", "first_ionisation_energy_kj_mol",
    "electron_affinity_kj_mol", "electronegativity_pauling",
    "effective_nuclear_charge", "effective_nuclear_charge_orbital",
)
MAIN_GROUPS = {1, 2, 13, 14, 15, 16, 17, 18}


def pubchem_rows(snapshot: Path | None) -> dict[int, dict[str, str]]:
    """Read PubChem's published periodic-table snapshot by atomic number."""
    if snapshot:
        payload = snapshot.read_bytes()
    else:
        with urlopen(PUBCHEM_URL) as response:  # nosec B310: preparation only
            payload = response.read()
    table = json.loads(payload)["Table"]
    columns = table["Columns"]["Column"]
    return {
        int(values[0]): dict(zip(columns, values, strict=True))
        for row in table["Row"]
        for values in [row["Cell"]]
    }


def number(value: str | None) -> float | None:
    return float(value) if value else None


def selected_zeff(atomic_number: int, period: int, group: int | None) -> tuple[float | None, str | None]:
    """Select a documented outer-orbital Clementi--Raimondi value, Z - sigma."""
    if atomic_number == 1:
        target = (1, "s")
    elif atomic_number == 2:
        target = (1, "s")
    elif group in {1, 2}:
        target = (period, "s")
    elif group in MAIN_GROUPS:
        target = (period, "p")
    else:
        return None, None
    for constant in element(atomic_number).screening_constants:
        if (constant.n, constant.s) == target:
            return atomic_number - float(constant.screening), f"{target[0]}{target[1]}"
    return None, None


def curate(snapshot: Path | None) -> list[dict[str, object]]:
    """Apply explicit source selections and transformations to stable metadata."""
    pubchem = pubchem_rows(snapshot)
    with INPUT_PATH.open(newline="", encoding="utf-8") as handle:
        metadata = list(csv.DictReader(handle))
    curated: list[dict[str, object]] = []
    for row in metadata:
        atomic_number = int(row["atomic_number"])
        source = pubchem[atomic_number]
        period = int(row["period"])
        group = int(row["group"]) if row["group"].isdigit() else None
        source_element = element(atomic_number)
        zeff, orbital = selected_zeff(atomic_number, period, group)
        # PubChem reports IE and EA in eV. EA is positive binding energy;
        # CHEM1011 uses negative delta-H for favourable electron attachment.
        curated.append({
            "atomic_number": atomic_number,
            "symbol": row["symbol"],
            "element_name": row["element_name"],
            "period": period,
            "group": group if group is not None else "",
            "covalent_atomic_radius_pm": source_element.covalent_radius_cordero,
            "first_ionisation_energy_kj_mol": (
                number(source.get("IonizationEnergy")) * EV_TO_KJ_MOL
                if number(source.get("IonizationEnergy")) is not None else None
            ),
            "electron_affinity_kj_mol": (
                -number(source.get("ElectronAffinity")) * EV_TO_KJ_MOL
                if number(source.get("ElectronAffinity")) is not None else None
            ),
            "electronegativity_pauling": number(source.get("Electronegativity")),
            "effective_nuclear_charge": zeff,
            "effective_nuclear_charge_orbital": orbital,
        })
    return curated


def write(rows: list[dict[str, object]], output: Path) -> None:
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            rendered = {key: "" if value is None else value for key, value in row.items()}
            for key, digits in {
                "covalent_atomic_radius_pm": 1,
                "first_ionisation_energy_kj_mol": 3,
                "electron_affinity_kj_mol": 3,
                "effective_nuclear_charge": 4,
            }.items():
                if rendered[key] != "":
                    rendered[key] = f"{float(rendered[key]):.{digits}f}"
            writer.writerow(rendered)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pubchem-json", type=Path, help="Saved PubChem PUG periodic-table JSON response")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    arguments = parser.parse_args()
    write(curate(arguments.pubchem_json), arguments.output)


if __name__ == "__main__":
    main()
