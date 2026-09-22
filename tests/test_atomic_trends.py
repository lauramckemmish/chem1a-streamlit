import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from experiences.atomic_trends import data
from experiences.atomic_trends import view


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class AtomicTrendsDataTests(unittest.TestCase):
    def test_local_data_covers_the_full_periodic_table(self) -> None:
        rows = data.elements()
        self.assertEqual(118, len(rows))
        self.assertEqual(list(range(1, 119)), [row["atomic_number"] for row in rows])

    def test_reference_units_match_the_stored_ionisation_energy_values(self) -> None:
        hydrogen = data.elements()[0]
        self.assertAlmostEqual(1312.008, hydrogen["first_ionisation_energy_kj_mol"], places=3)
        self.assertEqual("kJ mol⁻¹", data.PROPERTY_METADATA["First ionisation energy"][2])

    def test_canonical_property_schema_and_representative_source_values(self) -> None:
        rows = {row["symbol"]: row for row in data.elements()}
        self.assertIn("Covalent atomic radius", data.PROPERTY_METADATA)
        self.assertAlmostEqual(128.0, rows["Li"]["covalent_atomic_radius_pm"])
        self.assertAlmostEqual(84.0, rows["B"]["covalent_atomic_radius_pm"])
        self.assertAlmostEqual(2.2, rows["H"]["electronegativity_pauling"])
        self.assertIsNone(rows["He"]["electronegativity_pauling"])

    def test_electron_affinity_uses_negative_chem1011_attachment_convention(self) -> None:
        rows = {row["symbol"]: row for row in data.elements()}
        self.assertAlmostEqual(-72.750, rows["H"]["electron_affinity_kj_mol"], places=3)
        self.assertLess(rows["F"]["electron_affinity_kj_mol"], -300)
        self.assertLess(rows["Cl"]["electron_affinity_kj_mol"], -300)
        self.assertIsNone(rows["He"]["electron_affinity_kj_mol"])

    def test_zeff_retains_the_selected_clementi_raimondi_orbital(self) -> None:
        rows = {row["symbol"]: row for row in data.elements()}
        for symbol, orbital in {
            "H": "1s", "He": "1s", "Li": "2s", "Be": "2s", "B": "2p",
            "Ne": "2p", "Na": "3s", "Mg": "3s", "Al": "3p", "Ar": "3p",
        }.items():
            self.assertEqual(orbital, rows[symbol]["effective_nuclear_charge_orbital"])
            self.assertIsNotNone(rows[symbol]["effective_nuclear_charge"])
        self.assertIsNone(rows["Fe"]["effective_nuclear_charge"])
        self.assertIsNone(rows["Fe"]["effective_nuclear_charge_orbital"])

    def test_period_and_group_filters_preserve_natural_atomic_order(self) -> None:
        period_two = data.selected_elements("Periods", [2])
        group_one = data.selected_elements("Groups", [1])
        self.assertEqual([3, 4, 5, 6, 7, 8, 9, 10], [row["atomic_number"] for row in period_two])
        self.assertEqual([1, 3, 11, 19, 37, 55, 87], [row["atomic_number"] for row in group_one])

    def test_multiple_selections_and_missing_values_are_truthful(self) -> None:
        selected = data.series_for_selection("Groups", [1, 17], "electronegativity_pauling")
        self.assertEqual([1, 3, 9, 11, 17, 19], [row["atomic_number"] for row in selected[:6]])
        self.assertTrue(all(row["electronegativity_pauling"] is not None for row in selected))
        all_rows = data.selected_elements("All elements", [])
        self.assertEqual(118, len(all_rows))
        self.assertTrue(any(row["electronegativity_pauling"] is None for row in all_rows))

    def test_plotly_figure_keeps_period_labels_and_constrained_interaction(self) -> None:
        rows = data.series_for_selection("Periods", [2, 3], "first_ionisation_energy_kj_mol")
        figure = view._figure(rows, "First ionisation energy", "kJ mol⁻¹", show_labels=True)
        self.assertEqual(2, len(figure.data))
        self.assertTrue(all(trace.mode == "lines+markers+text" for trace in figure.data))
        self.assertEqual("Group", figure.layout.xaxis.title.text)
        self.assertEqual([1, 2, 13, 14, 15, 16, 17, 18], list(figure.data[0].x))
        self.assertEqual(list(figure.data[0].x), list(figure.data[1].x))
        self.assertEqual("zoom", figure.layout.dragmode)
        self.assertTrue(figure.layout.showlegend)
        self.assertEqual(430, figure.layout.height)
        self.assertFalse(figure.layout.xaxis.showgrid)
        self.assertFalse(view.PLOTLY_CONFIG["scrollZoom"])
        self.assertFalse(view.PLOTLY_CONFIG["displaylogo"])
        self.assertIn("lasso2d", view.PLOTLY_CONFIG["modeBarButtonsToRemove"])

    def test_plotly_all_elements_avoids_persistent_symbol_labels(self) -> None:
        rows = data.series_for_selection("All elements", [], "covalent_atomic_radius_pm")
        figure = view._figure(rows, "Covalent atomic radius", "pm", show_labels=False)
        self.assertEqual("lines+markers", figure.data[0].mode)
        self.assertIsNone(figure.data[0].text)
        self.assertFalse(figure.layout.showlegend)

    def test_group_plot_uses_period_on_the_horizontal_axis(self) -> None:
        rows = data.series_for_selection("Groups", [1, 17], "first_ionisation_energy_kj_mol")
        figure = view._figure(rows, "First ionisation energy", "kJ mol⁻¹", show_labels=True, mode="Groups")
        self.assertEqual("Period", figure.layout.xaxis.title.text)
        self.assertEqual(tuple(range(1, 8)), figure.layout.xaxis.tickvals)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7], list(figure.data[0].x))
        self.assertTrue(figure.layout.showlegend)

    def test_period_checkboxes_are_visible_and_allow_an_empty_selection(self) -> None:
        app = AppTest.from_file(str(APP_PATH)).run()
        period_controls = [control for control in app.checkbox if control.label in {str(value) for value in range(1, 8)}]
        self.assertEqual([str(value) for value in range(1, 8)], [control.label for control in period_controls])
        self.assertTrue(next(control for control in period_controls if control.label == "2").value)
        next(control for control in period_controls if control.label == "2").set_value(False).run()
        self.assertIn(
            "Choose at least one period or group with available reference values.",
            [notice.value for notice in app.info],
        )

    def test_explore_mode_is_segmented_and_groups_are_main_group_only(self) -> None:
        app = AppTest.from_file(str(APP_PATH)).run()
        explore = next(control for control in app.segmented_control if control.label == "Explore")
        self.assertEqual(["Periods", "Groups", "All elements"], list(explore.options))
        self.assertEqual("Periods", explore.value)
        explore.set_value("Groups").run()
        group_controls = [control for control in app.checkbox if control.label in {str(value) for value in view.MAIN_GROUPS}]
        self.assertEqual([str(value) for value in view.MAIN_GROUPS], [control.label for control in group_controls])
        self.assertTrue(next(control for control in group_controls if control.label == "1").value)
        self.assertFalse(any(control.label == "3" for control in app.checkbox))

    def test_periodic_trends_has_no_learner_prompt(self) -> None:
        app = AppTest.from_file(str(APP_PATH)).run()
        self.assertFalse(any("What pattern do you see?" in block.value for block in app.markdown))

    def test_each_canonical_property_is_available_to_the_existing_surface(self) -> None:
        app = AppTest.from_file(str(APP_PATH)).run()
        property_control = next(control for control in app.selectbox if control.label == "Property")
        self.assertEqual(list(data.PROPERTY_METADATA), list(property_control.options))
        for property_label in data.PROPERTY_METADATA:
            property_control.set_value(property_label).run()
            self.assertFalse(app.exception)


if __name__ == "__main__":
    unittest.main()
