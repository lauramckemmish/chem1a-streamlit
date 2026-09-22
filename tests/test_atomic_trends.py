import unittest

from experiences.atomic_trends import data


class AtomicTrendsDataTests(unittest.TestCase):
    def test_local_data_covers_the_full_periodic_table(self) -> None:
        rows = data.elements()
        self.assertEqual(118, len(rows))
        self.assertEqual(list(range(1, 119)), [row["atomic_number"] for row in rows])

    def test_reference_units_match_the_stored_ionisation_energy_values(self) -> None:
        hydrogen = data.elements()[0]
        self.assertEqual(1312.0, hydrogen["first_ionisation_energy_kj_mol"])
        self.assertEqual("kJ mol⁻¹", data.PROPERTY_METADATA["First ionisation energy"][2])

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


if __name__ == "__main__":
    unittest.main()
