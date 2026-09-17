import unittest
from decimal import Decimal

from experiences.w01_spectroscopy import data


class SpectroscopyDataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source_rows = data.source_lines()
        self.features = data.display_features()

    def test_stage_1_features_are_visible_and_neutral(self) -> None:
        features = data.stage_1_comparison_features()
        self.assertEqual({feature["species"] for feature in features}, data.STAGE_1_SPECIES)
        self.assertTrue(all(feature["ionization_stage"] == "I" for feature in features))
        self.assertTrue(all(380 <= float(feature["wavelength_nm"]) <= 780 for feature in features))

    def test_hydrogen_stage_selections_are_deliberate(self) -> None:
        comparison = [f for f in data.stage_1_comparison_features() if f["species"] == "H"]
        detail = data.hydrogen_detail_features()
        self.assertEqual(4, len(comparison))
        self.assertEqual(6, len(detail))
        self.assertEqual({"3", "4", "5", "6", "7", "8"}, {f["upper_n"] for f in detail})
        self.assertTrue({f["feature_id"] for f in comparison} <= {f["feature_id"] for f in detail})

    def test_sodium_d_doublet_remains_distinct(self) -> None:
        sodium = [f for f in data.stage_1_comparison_features() if f["species"] == "Na"]
        self.assertEqual(["NA_I_D2", "NA_I_D1"], [f["feature_id"] for f in sodium])
        self.assertEqual(2, len({f["wavelength_nm"] for f in sodium}))

    def test_no_learner_physical_intensity_field_exists(self) -> None:
        forbidden = {"relative_intensity", "intensity", "physical_intensity"}
        self.assertFalse(forbidden & set(self.features[0]))
        self.assertNotIn("relative_intensity", set(self.source_rows[0]))
        self.assertIn("source_reported_intensity", set(self.source_rows[0]))

    def test_display_features_retain_existing_source_references(self) -> None:
        source_ids = {row["source_id"] for row in self.source_rows}
        for feature in self.features:
            self.assertTrue(feature["source_ids"])
            self.assertTrue(set(feature["source_ids"].split("|")) <= source_ids)

    def test_series_reference_data_is_well_formed(self) -> None:
        series_rows = data.hydrogen_series_features()
        self.assertEqual({"Lyman", "Balmer", "Paschen"}, {row["series"] for row in series_rows})
        self.assertTrue(all(float(row["wavelength_nm"]) > 0 for row in series_rows))
        self.assertTrue(all(int(row["lower_n"]) < int(row["upper_n"]) for row in series_rows))
        self.assertTrue(all(row["source_url"] for row in series_rows))

    def test_angstrom_conversion_is_exact(self) -> None:
        self.assertEqual(Decimal("656.28518"), data.angstrom_to_nm("6562.8518"))


if __name__ == "__main__":
    unittest.main()
