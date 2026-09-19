import unittest
from decimal import Decimal

from chem1a_ui import UNSW_COLOURS
from experiences.w01_spectroscopy import data
from experiences.w01_spectroscopy import hydrogen
from experiences.w01_spectroscopy import read_spectrum
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

    def test_visual_and_quantitative_renderers_share_features_and_coordinates(self) -> None:
        species = ["H", "Na"]
        selected_features = spectrum.features_for_species(species)
        visual = spectrum.render_visual_comparison_svg(species)
        quantitative = spectrum.render_comparison_svg(species)
        self.assertTrue(
            all(feature in data.stage_1_comparison_features() for row in selected_features.values() for feature in row)
        )
        for feature in selected_features["Na"]:
            x = spectrum.wavelength_x(float(feature["wavelength_nm"]))
            self.assertIn(f'x1="{x:.2f}"', visual)
            self.assertIn(f'x1="{x:.2f}"', quantitative)
        self.assertNotIn("tick-label", visual)
        self.assertIn("tick-label", quantitative)

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

    def test_hydrogen_detail_is_the_established_six_balmer_features(self) -> None:
        features = hydrogen.balmer_detail_features()
        self.assertEqual(6, len(features))
        self.assertEqual(["3→2", "4→2", "5→2", "6→2", "7→2", "8→2"], [hydrogen.transition_label(feature) for feature in features])
        self.assertEqual(features, data.hydrogen_detail_features())

    def test_read_spectrum_reuses_balmer_features_and_shared_coordinates(self) -> None:
        features = read_spectrum.balmer_features()
        self.assertEqual(features, hydrogen.balmer_detail_features())
        self.assertEqual(6, len(features))
        self.assertEqual(["Line A", "Line B", "Line C", "Line D", "Line E", "Line F"], read_spectrum.feature_options())
        labelled_features = read_spectrum.labelled_features()
        self.assertEqual(
            sorted(float(feature["wavelength_nm"]) for feature in features),
            [float(labelled_features[label]["wavelength_nm"]) for label in read_spectrum.feature_options()],
        )
        line_svg = read_spectrum.render_line_spectrum_svg("Line A")
        graph_svg = read_spectrum.render_intensity_graph_svg("Line A")
        for feature in features:
            x = spectrum.wavelength_x(float(feature["wavelength_nm"]))
            self.assertIn(f'x1="{x:.2f}"', line_svg)
            self.assertIn(f'L {x:.2f} ', graph_svg)
        self.assertIn("Wavelength / nm", line_svg)
        self.assertIn("Intensity", graph_svg)
        self.assertIn("Peak height is not measured intensity", graph_svg)
        for rendered in (line_svg, graph_svg):
            self.assertIn("Example line", rendered)
            self.assertIn("Your trace", rendered)
            self.assertNotIn("3→2", rendered)
            self.assertNotIn("4→2", rendered)
            self.assertNotIn("656.285", rendered)
            self.assertNotIn("486.136", rendered)

    def test_read_spectrum_offsets_coincident_example_and_trace_labels(self) -> None:
        for rendered in (
            read_spectrum.render_line_spectrum_svg(read_spectrum.EXAMPLE_FEATURE_LABEL),
            read_spectrum.render_intensity_graph_svg(read_spectrum.EXAMPLE_FEATURE_LABEL),
        ):
            self.assertIn('text-anchor="end" class="guide-label">Example line', rendered)
            self.assertIn('text-anchor="start" class="guide-label">Your trace', rendered)
            self.assertIn(f'viewBox="0 0 1200 {read_spectrum.SVG_HEIGHT}"', rendered)

    def test_read_spectrum_peak_height_is_equal_and_illustrative(self) -> None:
        rendered = read_spectrum.render_intensity_graph_svg("Line B")
        self.assertEqual(6, rendered.count('class="illustrative-peak"'))
        self.assertEqual(88.0, read_spectrum.ILLUSTRATIVE_PEAK_HEIGHT)
        self.assertNotIn("relative_intensity", rendered)

    def test_hydrogen_transition_lookup_uses_existing_stored_features(self) -> None:
        target = hydrogen.observed_feature_for_transition(3, 2)
        self.assertIsNotNone(target)
        self.assertEqual("656.28518", target["wavelength_nm"])
        self.assertIsNone(hydrogen.observed_feature_for_transition(9, 2))
        self.assertIsNone(hydrogen.observed_feature_for_transition(2, 3))

    def test_hydrogen_adaptive_comparison_window_is_local_and_padded(self) -> None:
        target = hydrogen.observed_feature_for_transition(3, 2)
        observed_nm = float(target["wavelength_nm"])
        minimum, maximum = hydrogen.adaptive_comparison_window(650.0, observed_nm)
        self.assertGreaterEqual(maximum - minimum, hydrogen.MINIMUM_COMPARISON_WINDOW_NM)
        self.assertLess(minimum, 650.0)
        self.assertGreater(maximum, observed_nm)
        wide_minimum, wide_maximum = hydrogen.adaptive_comparison_window(486.0, observed_nm)
        self.assertGreater(wide_maximum - wide_minimum, maximum - minimum)
        self.assertAlmostEqual(5.0, 486.0 - wide_minimum)
        self.assertAlmostEqual(5.0, wide_maximum - observed_nm)

    def test_hydrogen_local_comparison_preserves_full_precision_and_displays_nearest_nm(self) -> None:
        target = hydrogen.observed_feature_for_transition(3, 2)
        prediction_nm = 650.123
        rendered = hydrogen.render_local_comparison_svg(prediction_nm=prediction_nm, observed_feature=target)
        minimum, maximum = hydrogen.adaptive_comparison_window(prediction_nm, float(target["wavelength_nm"]))
        self.assertIn("Your prediction · 650 nm", rendered)
        self.assertIn("Observed 3→2 · 656 nm", rendered)
        self.assertIn(f'x1="{hydrogen._x(prediction_nm, minimum, maximum):.2f}"', rendered)
        self.assertIn(f'x1="{hydrogen._x(float(target["wavelength_nm"]), minimum, maximum):.2f}"', rendered)
        self.assertNotIn("656.28518 nm", rendered)

    def test_hydrogen_prediction_classification_uses_only_stored_features(self) -> None:
        target = hydrogen.observed_feature_for_transition(3, 2)
        self.assertEqual(("target", None), hydrogen.prediction_match(target, 656.0))
        kind, other = hydrogen.prediction_match(target, 486.136)
        self.assertEqual("other_line", kind)
        self.assertEqual("4→2", hydrogen.transition_label(other))
        self.assertEqual(("mismatch", None), hydrogen.prediction_match(target, 650.0))
        self.assertTrue(hydrogen.prediction_is_plausible_for_comparison(656.0))
        self.assertFalse(hydrogen.prediction_is_plausible_for_comparison(65.6))
        self.assertFalse(hydrogen.prediction_is_plausible_for_comparison(6560.0))

    def test_hydrogen_barcode_is_non_numerical_and_transition_labels_remain_optional(self) -> None:
        barcode = hydrogen.render_balmer_barcode_svg()
        self.assertIn("hydrogen-barcode-svg", barcode)
        self.assertNotIn("tick-label", barcode)
        self.assertNotIn("3→2", barcode)

    def test_transition_label_reveal_uses_authoritative_metadata(self) -> None:
        target = hydrogen.observed_feature_for_transition(3, 2)
        rendered = hydrogen.render_local_comparison_svg(
            prediction_nm=650.0,
            observed_feature=target,
            show_transition_labels=True,
        )
        for feature in hydrogen.balmer_detail_features():
            if 640 <= float(feature["wavelength_nm"]) <= 670:
                self.assertIn(hydrogen.transition_label(feature), rendered)

    def test_series_reference_views_are_loaded_from_existing_data(self) -> None:
        self.assertEqual((90.0, 1900.0), hydrogen.series_overview_bounds())
        for series, region in hydrogen.SERIES_REGIONS.items():
            features = hydrogen.series_features(series)
            self.assertTrue(features)
            self.assertTrue(all(feature["series"] == series for feature in features))
            self.assertTrue(all(float(feature["wavelength_nm"]) > 0 for feature in features))
            self.assertIn(region, {"UV", "visible", "IR"})


if __name__ == "__main__":
    unittest.main()
