import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class StageOneAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = AppTest.from_file(str(APP_PATH)).run()

    def checkbox(self, label: str):
        return next(control for control in self.app.checkbox if control.label == label)

    def button(self, label: str):
        return next(control for control in self.app.button if control.label == label)

    def test_tabs_replace_surface_configuration_and_default_to_all_five_atoms(self) -> None:
        self.assertEqual(["Explore spectra", "Hydrogen"], [tab.label for tab in self.app.tabs])
        self.assertEqual(0, len(self.app.radio))
        self.assertTrue(all(self.checkbox(name).value for name in ("Hydrogen", "Helium", "Sodium", "Neon", "Mercury")))

    def test_explore_has_no_combined_spectrum_controls_or_display(self) -> None:
        labels = [control.label for control in self.app.checkbox]
        self.assertNotIn("Combined spectrum", labels)
        self.assertNotIn("Separate spectra", labels)
        self.assertFalse(any("Combined selected lines" in block.value for block in self.app.markdown))

    def test_default_explore_is_a_visual_barcode_without_wavelength_axis(self) -> None:
        rendered = next(block.value for block in self.app.markdown if "Selected atomic visual emission spectra" in block.value)
        self.assertIn("visual-field", rendered)
        for species in ("Hydrogen", "Helium", "Sodium", "Neon", "Mercury"):
            self.assertIn(species, rendered)
        self.assertNotIn("tick-label", rendered)
        self.assertIn("Show wavelength scale", [control.label for control in self.app.button])

    def test_focus_controls_remove_only_the_unchecked_visual_spectrum(self) -> None:
        self.checkbox("Helium").set_value(False).run()
        rendered = next(block.value for block in self.app.markdown if "Selected atomic visual emission spectra" in block.value)
        self.assertIn("Hydrogen", rendered)
        self.assertNotIn("Helium", rendered)
        self.assertIn("656.285", rendered)
        self.assertIn("588.995", rendered)

    def test_wavelength_reveal_transforms_to_quantitative_spectrum_and_persists(self) -> None:
        self.button("Show wavelength scale").click().run()
        rendered = next(block.value for block in self.app.markdown if "Selected atomic emission-line positions" in block.value)
        self.assertIn("380 to 780 nanometre scale", rendered)
        self.assertIn("tick-label", rendered)
        self.assertFalse(any("Selected atomic visual emission spectra" in block.value for block in self.app.markdown))
        self.assertIn("Reveal absorption spectra", [control.label for control in self.app.button])
        self.app.run()
        self.assertTrue(any("Selected atomic emission-line positions" in block.value for block in self.app.markdown))

    def test_absorption_is_not_available_until_wavelength_reveal_then_persists(self) -> None:
        self.assertFalse(any("Selected atomic absorption-line positions" in block.value for block in self.app.markdown))
        self.assertNotIn("Reveal absorption spectra", [control.label for control in self.app.button])
        self.button("Show wavelength scale").click().run()
        self.button("Reveal absorption spectra").click().run()
        rendered = [block.value for block in self.app.markdown if "Selected atomic absorption-line positions" in block.value]
        self.assertEqual(5, len(rendered))
        self.assertTrue(any("Hydrogen absorption" in block for block in rendered))
        self.app.run()
        self.assertTrue(any("Selected atomic absorption-line positions" in block.value for block in self.app.markdown))

    def test_absorption_pairs_each_selected_atom_with_its_own_emission(self) -> None:
        self.button("Show wavelength scale").click().run()
        self.button("Reveal absorption spectra").click().run()
        rendered = [block.value for block in self.app.markdown]
        self.assertTrue(any("Hydrogen — emission" in block for block in rendered))
        self.assertTrue(any("Hydrogen — absorption" in block for block in rendered))
        self.assertTrue(any("Sodium — emission" in block for block in rendered))
        self.assertTrue(any("Sodium — absorption" in block for block in rendered))
        sodium_absorption = [block for block in rendered if "Sodium absorption" in block]
        self.assertEqual(1, len(sodium_absorption))
        self.assertIn("588.995", sodium_absorption[0])
        self.assertIn("589.592", sodium_absorption[0])

    def test_added_atoms_use_the_current_quantitative_absorption_state(self) -> None:
        self.checkbox("Sodium").set_value(False).run()
        self.button("Show wavelength scale").click().run()
        self.button("Reveal absorption spectra").click().run()
        self.checkbox("Sodium").set_value(True).run()
        rendered = [block.value for block in self.app.markdown]
        self.assertTrue(any("Sodium: 588.995, 589.592 nm" in block for block in rendered))
        self.assertTrue(any("Sodium absorption" in block for block in rendered))

    def test_focus_controls_do_not_reset_the_wavelength_reveal(self) -> None:
        self.button("Show wavelength scale").click().run()
        self.checkbox("Neon").set_value(False).run()
        self.assertTrue(any("Selected atomic emission-line positions" in block.value for block in self.app.markdown))
        self.assertNotIn("Neon", next(block.value for block in self.app.markdown if "Selected atomic emission-line positions" in block.value))

    def test_focus_controls_do_not_reset_the_absorption_reveal(self) -> None:
        self.button("Show wavelength scale").click().run()
        self.button("Reveal absorption spectra").click().run()
        self.checkbox("Mercury").set_value(False).run()
        self.assertTrue(any("Selected atomic absorption-line positions" in block.value for block in self.app.markdown))
        self.assertFalse(any("Mercury absorption" in block.value for block in self.app.markdown))

    def test_no_selected_atom_has_a_neutral_prompt(self) -> None:
        for label in ("Hydrogen", "Helium", "Sodium", "Neon", "Mercury"):
            self.checkbox(label).set_value(False).run()
        self.assertEqual(["Choose an atom to keep a spectrum in view."], [notice.value for notice in self.app.info])

    def test_hydrogen_surface_stays_available_without_calculating_the_prediction(self) -> None:
        self.assertEqual(["Your predicted wavelength (nm)"], [control.label for control in self.app.number_input])
        self.app.number_input[0].set_value(650.123).run()
        self.button("Plot my prediction").click().run()
        rendered = next(block.value for block in self.app.markdown if "Your prediction: 650.123 nm" in block.value)
        self.assertIn("Your prediction: 650.123 nm", rendered)
        self.assertEqual(["See more of hydrogen"], [section.label for section in self.app.expander])

    def test_sidebar_contains_only_chem1a_identity_and_verified_source_context(self) -> None:
        sidebar_text = " ".join(block.value for block in self.app.sidebar.markdown)
        self.assertIn("CHEM 1A", sidebar_text)
        self.assertIn("Scientific source", sidebar_text)
        self.assertNotIn("CURIOUS", sidebar_text)
        self.assertNotIn("NESA", sidebar_text)
        self.assertNotIn("Data to Discovery", sidebar_text)


if __name__ == "__main__":
    unittest.main()
