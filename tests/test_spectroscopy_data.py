import unittest
from decimal import Decimal

from chem1a_ui import UNSW_COLOURS
from experiences.w01_spectroscopy import data
from experiences.w01_spectroscopy import spectrum


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

    def test_stage_1_renderer_uses_only_approved_data(self) -> None:
        selected = spectrum.features_for_species(["H", "Na", "Ne"])
        self.assertEqual(["H", "Na", "Ne"], list(selected))
        self.assertTrue(
            all(feature in data.stage_1_comparison_features() for features in selected.values() for feature in features)
        )
        self.assertTrue(
            all(380 <= float(feature["wavelength_nm"]) <= 780 for features in selected.values() for feature in features)
        )

    def test_stage_1_renderer_keeps_coordinates_shared(self) -> None:
        self.assertEqual(spectrum.wavelength_x(589.0), spectrum.wavelength_x(589.0))
        self.assertLess(spectrum.wavelength_x(588.9950), spectrum.wavelength_x(589.5924))
        self.assertEqual(spectrum.PLOT_LEFT, spectrum.wavelength_x(380.0))
        self.assertEqual(spectrum.PLOT_RIGHT, spectrum.wavelength_x(780.0))

    def test_stage_1_renderer_rejects_unapproved_species(self) -> None:
        with self.assertRaises(ValueError):
            spectrum.features_for_species(["He+"])

    def test_stage_1_default_starts_with_hydrogen_only(self) -> None:
        self.assertEqual(("H",), spectrum.DEFAULT_SELECTED_SPECIES)
        self.assertTrue(set(spectrum.DEFAULT_SELECTED_SPECIES) <= set(spectrum.SPECIES_ORDER))

    def test_shared_visual_system_uses_the_unified_unsw_theme_colours(self) -> None:
        self.assertEqual("#FFDC00", UNSW_COLOURS["yellow"])
        self.assertEqual("#3F61C4", UNSW_COLOURS["indigo"])

    def test_combined_features_are_the_unique_union_of_selected_features(self) -> None:
        selected = spectrum.features_for_species(["H", "Na"])
        combined = spectrum.combined_features_for_species(["H", "Na"])
        self.assertEqual(6, len(combined))
        self.assertEqual(len(combined), len({feature["wavelength_nm"] for feature in combined}))
        self.assertEqual(
            {feature["feature_id"] for feature in combined},
            {feature["feature_id"] for features in selected.values() for feature in features},
        )
        self.assertTrue(all(380 <= float(feature["wavelength_nm"]) <= 780 for feature in combined))

    def test_absorption_uses_the_same_selected_positions_as_emission(self) -> None:
        species = ["H", "Na", "Ne"]
        self.assertEqual(spectrum.features_for_species(species), spectrum.absorption_features_for_species(species))
        self.assertEqual(
            spectrum.combined_features_for_species(species),
            spectrum.combined_absorption_features_for_species(species),
        )
        absorption = spectrum.render_combined_absorption_svg(species)
        self.assertIn("continuous illustrative visible-spectrum band", absorption)
        self.assertNotIn("relative_intensity", absorption)
        self.assertTrue(
            all(380 <= float(feature["wavelength_nm"]) <= 780 for feature in spectrum.combined_absorption_features_for_species(species))
        )


if __name__ == "__main__":
    unittest.main()
