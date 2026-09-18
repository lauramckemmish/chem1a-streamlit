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
        self.assertTrue(self.checkbox("Hydrogen").value)
        self.assertFalse(self.checkbox("Helium").value)
        self.assertFalse(self.checkbox("Sodium").value)
        self.assertFalse(self.checkbox("Neon").value)
        self.assertFalse(self.checkbox("Mercury").value)
        self.assertTrue(self.checkbox("Combined spectrum").value)
        self.assertFalse(self.checkbox("Separate spectra").value)
        self.assertEqual(1, sum("<svg" in block.value for block in self.app.markdown))

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
        self.assertEqual(2, len(spectra))
        self.assertIn("Combined selected lines", spectra[0])
        self.assertIn("Sodium", spectra[1])

    def test_no_selected_atom_has_a_neutral_prompt(self) -> None:
        self.checkbox("Hydrogen").set_value(False).run()
        self.assertEqual(["Select an atom to begin."], [notice.value for notice in self.app.info])


if __name__ == "__main__":
    unittest.main()
