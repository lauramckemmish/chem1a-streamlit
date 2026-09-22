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
        self.assertEqual(
            ["Spectroscopy", "Explore spectra", "Hydrogen", "Read the spectrum", "Atomic trends"],
            [tab.label for tab in self.app.tabs],
        )
        self.assertEqual(0, len(self.app.radio))
        self.assertTrue(all(self.checkbox(name).value for name in ("Hydrogen", "Helium", "Sodium", "Neon", "Mercury")))
        self.assertEqual([], [heading.value for heading in self.app.title])
        self.assertEqual([], [heading.value for heading in self.app.subheader])
        self.assertTrue(
            any("CHEM 1A · Week 01 · Spectroscopy" in block.value for block in self.app.markdown)
        )
        self.assertEqual(
            ["Explore atomic spectra", "Hydrogen", "Read the spectrum", "Explore periodic trends"],
            [heading.value for heading in self.app.header],
        )

    def test_explore_has_no_combined_spectrum_controls_or_display(self) -> None:
        labels = [control.label for control in self.app.checkbox]
        self.assertNotIn("Combined spectrum", labels)
        self.assertNotIn("Separate spectra", labels)
        self.assertFalse(any("Combined selected lines" in block.value for block in self.app.markdown))
        rendered = [block.value for block in self.app.markdown]
        self.assertTrue(any("Spectra in view" in block for block in rendered))
        self.assertFalse(any("Focus the comparison" in block for block in rendered))

    def test_default_explore_is_a_visual_barcode_without_wavelength_axis(self) -> None:
        rendered = next(block.value for block in self.app.markdown if "Selected atomic visual emission spectra" in block.value)
        self.assertIn("visual-field", rendered)
        for species in ("Hydrogen", "Helium", "Sodium", "Neon", "Mercury"):
            self.assertIn(species, rendered)
        self.assertNotIn("tick-label", rendered)
        self.assertIn("Show wavelength scale", [control.label for control in self.app.button])
        page_copy = [block.value for block in self.app.markdown]
        self.assertFalse(any("Compare the patterns in these atomic spectra." in block for block in page_copy))
        self.assertIn(
            "Colour is a wavelength cue. The pattern of line positions is what to compare.",
            [caption.value for caption in self.app.caption],
        )
        self.assertTrue(any("What changes? What stays the same?" in block for block in page_copy))
        self.assertTrue(any("Spectra in view" in block for block in page_copy))
        self.assertTrue(any("Now add a wavelength scale to the same patterns." in block for block in page_copy))

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
        page_copy = [block.value for block in self.app.markdown]
        self.assertIn(
            "Horizontal position gives the wavelength. Colour is a visual cue.",
            [caption.value for caption in self.app.caption],
        )
        self.assertIn(
            "Sodium’s two selected lines are at 588.995 and 589.592 nm. They almost overlap on this scale.",
            [caption.value for caption in self.app.caption],
        )
        self.assertTrue(any("Now compare the same atoms in absorption." in block for block in page_copy))
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
        self.assertTrue(any('class="chem1a-pair-atom">Hydrogen' in block for block in rendered))
        self.assertTrue(any('class="chem1a-pair-atom">Sodium' in block for block in rendered))
        self.assertGreaterEqual(sum('chem1a-pair-label">Emission' in block for block in rendered), 5)
        self.assertGreaterEqual(sum('chem1a-pair-label">Absorption' in block for block in rendered), 5)
        sodium_absorption = [block for block in rendered if "Sodium absorption" in block]
        self.assertEqual(1, len(sodium_absorption))
        self.assertIn("588.995", sodium_absorption[0])
        self.assertIn("589.592", sodium_absorption[0])
        self.assertFalse(any("What do you notice about where the absorption and emission lines appear?" in block for block in rendered))
        self.assertTrue(any("Emission and absorption lines occur at the same wavelengths. Why?" in block for block in rendered))

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
        self.assertEqual(["Choose at least one spectrum to keep in view."], [notice.value for notice in self.app.info])

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

    def test_read_spectrum_has_aligned_representations_and_native_trace_control(self) -> None:
        self.assertIn("Choose a line to trace", [control.label for control in self.app.selectbox])
        self.assertEqual(
            ["Line A", "Line B", "Line C", "Line D", "Line E", "Line F"],
            list(next(control for control in self.app.selectbox if control.label == "Choose a line to trace").options),
        )
        rendered = [block.value for block in self.app.markdown]
        self.assertTrue(any("The same hydrogen spectrum can be shown in two different ways." in block for block in rendered))
        self.assertTrue(any("**Line spectrum**" in block for block in rendered))
        self.assertTrue(any("**Intensity vs wavelength**" in block for block in rendered))
        self.assertTrue(any("Hydrogen line spectrum" in block for block in rendered))
        self.assertTrue(any("Hydrogen intensity versus wavelength" in block for block in rendered))
        self.assertIn(
            "The line and peak are at the same wavelength. Peak height is simplified here so you can focus on position.",
            [caption.value for caption in self.app.caption],
        )
        self.assertTrue(any("Find another line and its matching peak. What stays the same? What has been added?" in block for block in rendered))
        self.assertIn("What about peak height?", [section.label for section in self.app.expander])
        self.assertTrue(
            any(
                "Real spectra can have unequal peak heights. Intensity depends on the physical conditions and on how the spectrum is produced and measured. Here, peak height is held constant so you can focus on the wavelength mapping."
                in block
                for block in rendered
            )
        )
        next(control for control in self.app.selectbox if control.label == "Choose a line to trace").set_value("Line D").run()
        updated = [block.value for block in self.app.markdown]
        read_rendered = [block for block in updated if "read-line-svg" in block or "intensity-graph-svg" in block]
        self.assertEqual(2, len(read_rendered))
        self.assertTrue(all("Your trace" in block for block in read_rendered))
        self.assertTrue(all("3→2" not in block and "656.285" not in block for block in read_rendered))

    def test_sidebar_contains_only_chem1a_identity_and_verified_source_context(self) -> None:
        sidebar_text = " ".join(block.value for block in self.app.sidebar.markdown)
        sidebar_captions = [caption.value for caption in self.app.sidebar.caption]
        self.assertIn("CHEM 1A", sidebar_text)
        self.assertIn("Week 01 · Spectroscopy", sidebar_captions)
        self.assertIn("Scientific source", sidebar_text)
        self.assertIn("Bounded NIST atomic-spectroscopy references", sidebar_captions)
        self.assertIn("Selected teaching features; provenance is recorded in this repository.", sidebar_captions)
        self.assertNotIn("CURIOUS", sidebar_text)
        self.assertNotIn("NESA", sidebar_text)
        self.assertNotIn("Data to Discovery", sidebar_text)


if __name__ == "__main__":
    unittest.main()
