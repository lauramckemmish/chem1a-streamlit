import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class StageOneAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = AppTest.from_file(str(APP_PATH)).run()
        if "hydrogen" in self._testMethodName:
            self.app.segmented_control[0].set_value("Hydrogen").run()

    def checkbox(self, label: str):
        return next(control for control in self.app.checkbox if control.label == label)

    def button(self, label: str):
        return next(control for control in self.app.button if control.label == label)

    def explore_control(self, label: str):
        return next(control for control in self.app.segmented_control if control.label == label)

    def test_tabs_replace_surface_configuration_and_default_to_all_five_atoms(self) -> None:
        self.assertEqual(
            ["Spectroscopy", "Periodic trends"],
            [tab.label for tab in self.app.tabs],
        )
        self.assertEqual(
            ["Explore spectra", "Hydrogen"],
            list(self.app.segmented_control[0].options),
        )
        self.assertEqual(0, len(self.app.radio))
        self.assertTrue(all(self.checkbox(name).value for name in ("Hydrogen", "Helium", "Sodium", "Neon", "Mercury")))
        self.assertEqual([], [heading.value for heading in self.app.title])
        self.assertEqual([], [heading.value for heading in self.app.subheader])
        self.assertFalse(any("CHEM 1A · Week 01 · Spectroscopy" in block.value for block in self.app.markdown))
        self.assertEqual(
            ["Explore atomic spectra", "Periodic trends"],
            [heading.value for heading in self.app.header],
        )

    def test_explore_has_no_combined_spectrum_controls_or_display(self) -> None:
        labels = [control.label for control in self.app.checkbox]
        self.assertNotIn("Combined spectrum", labels)
        self.assertNotIn("Separate spectra", labels)
        self.assertFalse(any("Combined selected lines" in block.value for block in self.app.markdown))
        rendered = [block.value for block in self.app.markdown]
        self.assertTrue(any("Atoms in view" in block for block in rendered))
        self.assertTrue(any("Representations" in block for block in rendered))
        self.assertFalse(any("Focus the comparison" in block for block in rendered))

    def test_default_explore_is_a_visual_barcode_without_wavelength_axis(self) -> None:
        rendered = next(block.value for block in self.app.markdown if "Selected atomic visual emission spectra" in block.value)
        self.assertIn("visual-field", rendered)
        for species in ("Hydrogen", "Helium", "Sodium", "Neon", "Mercury"):
            self.assertIn(species, rendered)
        self.assertNotIn("tick-label", rendered)
        self.assertTrue(self.checkbox("Emission").value)
        self.assertFalse(self.checkbox("Absorption").value)
        self.assertTrue(self.checkbox("Visual spectrum").value)
        self.assertFalse(self.checkbox("Wavelength spectrum").value)
        self.assertFalse(self.checkbox("Intensity vs wavelength").value)
        page_copy = [block.value for block in self.app.markdown]
        self.assertFalse(any("Compare" in block for block in page_copy))
        self.assertFalse(
            any("What changes? What stays the same?" in block for block in page_copy)
        )
        self.assertFalse(any("Compare the patterns in these atomic spectra." in block for block in page_copy))
        self.assertNotIn(
            "Colour is a wavelength cue. The pattern of line positions is what to compare.",
            [caption.value for caption in self.app.caption],
        )
        self.assertTrue(any("Atoms in view" in block for block in page_copy))
        self.assertEqual("Representation", self.explore_control("Arrange by").value)
        self.assertNotIn("Show wavelength scale", [control.label for control in self.app.button])
        self.assertNotIn("Reveal absorption spectra", [control.label for control in self.app.button])

    def test_focus_controls_remove_only_the_unchecked_visual_spectrum(self) -> None:
        self.checkbox("Helium").set_value(False).run()
        rendered = next(block.value for block in self.app.markdown if "Selected atomic visual emission spectra" in block.value)
        self.assertIn("Hydrogen", rendered)
        self.assertNotIn("Helium", rendered)
        self.assertIn("656.285", rendered)
        self.assertIn("588.995", rendered)

    def test_wavelength_representation_is_immediate_and_monochrome(self) -> None:
        self.checkbox("Wavelength spectrum").set_value(True).run()
        rendered = next(block.value for block in self.app.markdown if "Selected atomic line positions" in block.value)
        self.assertIn("380 to 780 nanometre scale", rendered)
        self.assertIn("tick-label", rendered)
        self.assertIn('stroke="#334155"', rendered)
        self.assertNotIn('stroke="rgb(', rendered)
        self.assertNotIn("selected features", rendered)
        self.assertTrue(any("Selected atomic visual emission spectra" in block.value for block in self.app.markdown))
        self.checkbox("Absorption").set_value(True).run()
        self.assertEqual(
            1,
            len([block for block in self.app.markdown if "Selected atomic line positions" in block.value]),
        )
        captions = [caption.value for caption in self.app.caption]
        self.assertNotIn("Horizontal position gives the wavelength.", captions)
        self.assertFalse(any("Sodium’s two selected lines" in caption for caption in captions))

    def test_absorption_visual_and_wavelength_representations_are_reversible(self) -> None:
        self.checkbox("Emission").set_value(False).run()
        self.checkbox("Absorption").set_value(True).run()
        visual = next(block.value for block in self.app.markdown if "Selected atomic visual absorption spectra" in block.value)
        self.assertIn("visible-spectrum-band", visual)
        self.assertNotIn("tick-label", visual)
        self.checkbox("Wavelength spectrum").set_value(True).run()
        quantitative = next(block.value for block in self.app.markdown if "Selected atomic line positions" in block.value)
        self.assertIn("tick-label", quantitative)
        self.assertIn('stroke="#334155"', quantitative)
        self.checkbox("Emission").set_value(True).run()
        self.checkbox("Absorption").set_value(False).run()
        self.checkbox("Wavelength spectrum").set_value(False).run()
        self.assertTrue(any("Selected atomic visual emission spectra" in block.value for block in self.app.markdown))

    def test_species_controls_apply_to_reversible_explore_representations(self) -> None:
        self.checkbox("Wavelength spectrum").set_value(True).run()
        self.checkbox("Neon").set_value(False).run()
        rendered = next(block.value for block in self.app.markdown if "Selected atomic line positions" in block.value)
        self.assertNotIn("Neon", rendered)
        self.checkbox("Emission").set_value(False).run()
        self.checkbox("Absorption").set_value(True).run()
        rendered = next(block.value for block in self.app.markdown if "Selected atomic line positions" in block.value)
        self.assertNotIn("Neon", rendered)

    def test_intensity_representation_is_available_for_emission_and_absorption(self) -> None:
        self.checkbox("Intensity vs wavelength").set_value(True).run()
        qualification = "Intensity curves are illustrative; line positions come from the reference data."
        self.assertEqual([qualification], [caption.value for caption in self.app.caption])
        self.checkbox("Absorption").set_value(True).run()
        self.assertEqual([qualification], [caption.value for caption in self.app.caption])
        self.assertFalse(any("The line and peak are centred" in caption.value for caption in self.app.caption))
        self.assertFalse(any("The line and dip are centred" in caption.value for caption in self.app.caption))

    def test_arrangement_changes_only_evidence_grouping(self) -> None:
        self.checkbox("Wavelength spectrum").set_value(True).run()
        self.checkbox("Absorption").set_value(True).run()
        self.explore_control("Arrange by").set_value("Atom").run()
        self.assertTrue(all(self.checkbox(name).value for name in ("Emission", "Absorption", "Visual spectrum", "Wavelength spectrum")))
        self.assertTrue(any("Hydrogen" in heading.value for heading in self.app.markdown))
        self.assertEqual(15, len([block for block in self.app.markdown if "Selected atomic" in block.value]))

    def test_atom_arrangement_uses_the_outer_atom_heading_as_the_visual_identity(self) -> None:
        for label in ("Helium", "Sodium", "Neon", "Mercury"):
            self.checkbox(label).set_value(False).run()
        self.explore_control("Arrange by").set_value("Atom").run()
        visual = next(block.value for block in self.app.markdown if "Selected atomic visual emission spectra" in block.value)
        self.assertNotIn(">Hydrogen</text>", visual)
        self.assertTrue(any("#### Hydrogen" in block.value for block in self.app.markdown))

    def test_no_selected_atom_has_a_neutral_prompt(self) -> None:
        for label in ("Hydrogen", "Helium", "Sodium", "Neon", "Mercury"):
            self.checkbox(label).set_value(False).run()
        self.assertEqual(["Choose at least one spectrum to keep in view."], [notice.value for notice in self.app.info])

    def test_no_selected_representation_has_a_neutral_prompt(self) -> None:
        self.checkbox("Visual spectrum").set_value(False).run()
        self.assertEqual(["Choose at least one representation to display."], [notice.value for notice in self.app.info])

    def test_no_selected_spectrum_type_has_a_neutral_prompt(self) -> None:
        self.checkbox("Emission").set_value(False).run()
        self.assertEqual(["Choose at least one spectrum type to display."], [notice.value for notice in self.app.info])

    def hydrogen_input(self, label: str):
        return next(control for control in self.app.number_input if control.label == label)

    def test_hydrogen_starts_with_a_barcode_and_transition_inputs(self) -> None:
        self.assertTrue(
            all(
                label in [control.label for control in self.app.number_input]
                for label in ("From level n", "To level n", "Your predicted wavelength (nm)")
            )
        )
        self.assertEqual(5, self.hydrogen_input("From level n").value)
        self.assertEqual(2, self.hydrogen_input("To level n").value)
        self.assertEqual("e.g. 123", self.hydrogen_input("Your predicted wavelength (nm)").proto.placeholder)
        initial = [block.value for block in self.app.markdown]
        self.assertTrue(any("You have a predicted wavelength. Now test the model against the hydrogen spectrum." in block for block in initial))
        self.assertTrue(any("hydrogen-barcode-svg" in block for block in initial))
        self.assertFalse(any("hydrogen-local-svg" in block for block in initial))
        self.assertIn("Nearest nm is accurate enough for this comparison.", [caption.value for caption in self.app.caption])
        self.assertNotIn("Show transition labels", [control.label for control in self.app.checkbox])

    def test_hydrogen_valid_prediction_reveals_local_evidence_and_persists(self) -> None:
        self.hydrogen_input("Your predicted wavelength (nm)").set_value(434.0).run()
        self.button("Plot my prediction").click().run()
        rendered = next(block.value for block in self.app.markdown if "hydrogen-local-svg" in block.value)
        self.assertIn("Your prediction · 434 nm", rendered)
        self.assertIn("Observed 5→2 · 434 nm", rendered)
        self.assertIn("Show transition labels", [control.label for control in self.app.checkbox])
        self.assertTrue(any("This is the test: does your prediction match an observed line?" in block.value for block in self.app.markdown))
        self.assertIn(
            "Line height is simplified here. Compare wavelength position, not relative line strength.",
            [caption.value for caption in self.app.caption],
        )
        self.assertIn("See more of hydrogen", [section.label for section in self.app.expander])
        self.assertTrue(any("Visible Balmer lines are only part of the hydrogen spectrum." in block.value for block in self.app.markdown))
        self.assertTrue(any("Where the series appear" in block.value for block in self.app.markdown))
        self.assertFalse(any("The overview locates the series. Use the local views below to inspect selected reference lines." in block.value for block in self.app.markdown))
        self.assertTrue(all(label in [control.label for control in self.app.checkbox] for label in ("Lyman · UV", "Balmer · visible", "Paschen · IR")))
        self.app.run()
        self.assertTrue(any("hydrogen-local-svg" in block.value for block in self.app.markdown))

    def test_hydrogen_rejects_invalid_and_unsupported_transitions_without_revealing_evidence(self) -> None:
        self.hydrogen_input("From level n").set_value(2).run()
        self.hydrogen_input("To level n").set_value(3).run()
        self.hydrogen_input("Your predicted wavelength (nm)").set_value(656.0).run()
        self.button("Plot my prediction").click().run()
        self.assertIn("For emission, the starting level n must be greater than the ending level.", [notice.value for notice in self.app.info])
        self.assertFalse(any("hydrogen-local-svg" in block.value for block in self.app.markdown))
        self.hydrogen_input("From level n").set_value(9).run()
        self.hydrogen_input("To level n").set_value(2).run()
        self.button("Plot my prediction").click().run()
        self.assertIn(
            "This comparison currently uses the selected Balmer transitions available in the app.",
            [notice.value for notice in self.app.info],
        )

    def test_hydrogen_unit_range_guidance_does_not_reveal_evidence(self) -> None:
        self.hydrogen_input("Your predicted wavelength (nm)").set_value(6560.0).run()
        self.button("Plot my prediction").click().run()
        self.assertIn(
            "This value is well outside the wavelength range expected for this comparison. Check that your final wavelength is in nm.",
            [notice.value for notice in self.app.info],
        )
        self.assertFalse(any("hydrogen-local-svg" in block.value for block in self.app.markdown))

    def test_hydrogen_prediction_messages_are_concise_and_neutral(self) -> None:
        self.button("Plot my prediction").click().run()
        self.assertIn("Enter your predicted wavelength in nm first.", [notice.value for notice in self.app.info])
        self.hydrogen_input("Your predicted wavelength (nm)").set_value(-1.0).run()
        self.button("Plot my prediction").click().run()
        self.assertIn("Enter a positive wavelength in nm.", [notice.value for notice in self.app.info])

    def test_hydrogen_mismatch_diagnostics_use_stored_lines_and_replace_submissions(self) -> None:
        self.hydrogen_input("Your predicted wavelength (nm)").set_value(486.0).run()
        self.button("Plot my prediction").click().run()
        self.assertTrue(any("4→2 at 486 nm" in notice.value for notice in self.app.info))
        self.hydrogen_input("Your predicted wavelength (nm)").set_value(650.0).run()
        self.button("Plot my prediction").click().run()
        self.assertTrue(any("Check ΔE, your units, and the wavelength conversion." in notice.value for notice in self.app.info))
        self.hydrogen_input("From level n").set_value(4).run()
        self.hydrogen_input("To level n").set_value(2).run()
        self.hydrogen_input("Your predicted wavelength (nm)").set_value(486.0).run()
        self.button("Plot my prediction").click().run()
        rendered = next(block.value for block in self.app.markdown if "hydrogen-local-svg" in block.value)
        self.assertIn("Observed 4→2 · 486 nm", rendered)

    def test_no_learner_sidebar_is_rendered(self) -> None:
        self.assertEqual([], list(self.app.sidebar.markdown))
        self.assertEqual([], list(self.app.sidebar.caption))


if __name__ == "__main__":
    unittest.main()
