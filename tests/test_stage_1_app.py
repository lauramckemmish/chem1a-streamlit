import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class StageOneAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = AppTest.from_file(str(APP_PATH)).run()

    def checkbox(self, label: str):
        return next(control for control in self.app.checkbox if control.label == label)

    def test_default_is_hydrogen_combined_view(self) -> None:
        self.assertEqual(("Explore spectra", "Hydrogen"), tuple(self.app.radio[0].options))
        self.assertEqual("Explore spectra", self.app.radio[0].value)
        self.assertTrue(self.checkbox("Hydrogen").value)
        self.assertFalse(self.checkbox("Helium").value)
        self.assertFalse(self.checkbox("Sodium").value)
        self.assertFalse(self.checkbox("Neon").value)
        self.assertFalse(self.checkbox("Mercury").value)
        self.assertTrue(self.checkbox("Combined spectrum").value)
        self.assertFalse(self.checkbox("Separate spectra").value)
        self.assertEqual(["Explore absorption spectra"], [section.label for section in self.app.expander])

    def test_combined_view_adds_selected_species_without_changing_the_shared_scale(self) -> None:
        self.checkbox("Sodium").set_value(True).run()
        self.checkbox("Neon").set_value(True).run()
        combined_svg = next(block.value for block in self.app.markdown if "Combined selected lines" in block.value)
        self.assertIn("380 to 780 nanometre scale", combined_svg)
        self.assertIn("588.995", combined_svg)
        self.assertIn("585.249", combined_svg)

    def test_separate_view_adds_component_rows_below_the_combined_row(self) -> None:
        self.checkbox("Sodium").set_value(True).run()
        self.checkbox("Separate spectra").set_value(True).run()
        spectra = [block.value for block in self.app.markdown if "<svg" in block.value]
        self.assertGreaterEqual(len(spectra), 2)
        self.assertIn("Combined selected lines", spectra[0])
        self.assertIn("Sodium", spectra[1])

    def test_no_selected_atom_has_a_neutral_prompt(self) -> None:
        self.checkbox("Hydrogen").set_value(False).run()
        self.assertEqual(["Select an atom to begin."], [notice.value for notice in self.app.info])

    def test_absorption_reveal_reuses_current_combined_selection(self) -> None:
        self.checkbox("Sodium").set_value(True).run()
        absorption_svg = next(
            block.value for block in self.app.markdown if "Selected atomic absorption-line positions" in block.value
        )
        self.assertIn("588.995", absorption_svg)
        self.assertIn("589.592", absorption_svg)
        self.assertTrue(self.checkbox("Hydrogen").value)
        self.assertTrue(self.checkbox("Sodium").value)

    def test_hydrogen_surface_places_the_learner_prediction_without_calculating_it(self) -> None:
        self.app.radio[0].set_value("Hydrogen").run()
        self.assertEqual(["Your predicted wavelength (nm)"], [control.label for control in self.app.number_input])
        self.app.number_input[0].set_value(650.123).run()
        self.app.button[0].click().run()
        rendered = next(block.value for block in self.app.markdown if "Your prediction: 650.123 nm" in block.value)
        self.assertIn("Your prediction: 650.123 nm", rendered)
        self.assertEqual(["See more of hydrogen"], [section.label for section in self.app.expander])

    def test_switching_surfaces_preserves_explore_state_and_adds_no_ion_surface(self) -> None:
        self.checkbox("Sodium").set_value(True).run()
        self.app.radio[0].set_value("Hydrogen").run()
        self.app.radio[0].set_value("Explore spectra").run()
        self.assertTrue(self.checkbox("Hydrogen").value)
        self.assertTrue(self.checkbox("Sodium").value)
        self.assertEqual(("Explore spectra", "Hydrogen"), tuple(self.app.radio[0].options))


if __name__ == "__main__":
    unittest.main()
