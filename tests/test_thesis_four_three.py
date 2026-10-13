"""Exact disk checks for the first thesis columns and squared-boundary stage."""

import unittest

from examples.build_four_three_thesis_first_stage import OUTPUT, build_html
from examples.build_four_three_thesis_squared_stage import (
    OUTPUT as SQUARED_OUTPUT, build_html as build_squared_html,
)
from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.mapping_classes import ConjugatedTwist, exact_action
from surface_diagrams.marked_disk_chain import marked_disk_chain
from surface_diagrams.thesis_four_three import (
    CHART_BRAID, CONCATENATED_ROWS, CYCLIC_ROWS, FIRST_ROWS, OUTER_WORD,
    REARRANGED_ROWS, ROTATED_ROWS, SQUARED_ROWS, check_stage,
    chronological_word,
)


class ThesisFourThreeTests(unittest.TestCase):
    def test_five_point_disk_chain_detects_outer_twist(self):
        reference = marked_disk_chain(exact_action((), 5))
        outer = marked_disk_chain(exact_action(OUTER_WORD, 5))
        self.assertEqual(len(reference), 5)
        self.assertEqual(tuple(arc.cuts for arc in reference), ((),) * 5)
        self.assertNotEqual(reference[0], outer[0])
        self.assertEqual(reference[1:], outer[1:])

    def test_first_column_and_cyclic_rotation_are_exact_disk_relations(self):
        target = exact_action(OUTER_WORD, 5)
        for rows in (FIRST_ROWS, CYCLIC_ROWS, REARRANGED_ROWS):
            with self.subTest(rows=rows):
                self.assertEqual(exact_action(chronological_word(rows), 5), target)
                certificates = check_stage(rows)
                self.assertEqual(len(certificates), 5)
                self.assertTrue(all(len(c.paths) == 5 for c in certificates))
                self.assertEqual(certificates[0].arcs[1:], certificates[-1].arcs[1:])
                self.assertNotEqual(certificates[0].arcs[0], certificates[-1].arcs[0])

    def test_green_factor_is_an_inverse_square(self):
        green = FIRST_ROWS[0][1]
        self.assertEqual(green.word, inverse_word(ConjugatedTwist((), 4, 2).word) * 2)
        self.assertEqual(FIRST_ROWS[2][0].twist.conjugator, (-2,))
        self.assertEqual(FIRST_ROWS[3][0].twist.conjugator, (-1, -2))

    def test_third_column_is_a_checked_chart_conjugation(self):
        # The source's point rearrangement is global, so every changed
        # factor agrees with beta f beta^-1 as a based disk action.
        for original, changed in zip(FIRST_ROWS, REARRANGED_ROWS):
            for old, new in zip(original, changed):
                expected = CHART_BRAID + old.word + inverse_word(CHART_BRAID)
                self.assertEqual(exact_action(new.word, 5), exact_action(expected, 5))
        self.assertEqual(REARRANGED_ROWS[-1][0].word, FIRST_ROWS[1][0].word)

    def test_published_visual_is_current_and_contains_all_cut_rows(self):
        page = build_html()
        self.assertEqual(OUTPUT.read_text(encoding='utf-8'), page)
        self.assertEqual(page.count('class="factor-row"'), 12)
        self.assertEqual(page.count('data-projection="smooth"'), 12)
        self.assertIn('The cyclic arrow is checked by exact disk action', page)
        self.assertIn('chart β', page)

    def test_squared_boundary_stage_has_explicit_cyclic_and_combine_steps(self):
        target = exact_action(OUTER_WORD * 2, 5)
        for rows in (CONCATENATED_ROWS, ROTATED_ROWS, SQUARED_ROWS):
            with self.subTest(rows=len(rows)):
                self.assertEqual(exact_action(chronological_word(rows), 5), target)
                self.assertEqual(len(check_stage(rows, outer_power=2)), len(rows) + 1)
        self.assertEqual(ROTATED_ROWS[1:], CONCATENATED_ROWS[:-1])
        self.assertEqual(exact_action(chronological_word(ROTATED_ROWS[:2]), 5),
                         exact_action(chronological_word(SQUARED_ROWS[:1]), 5))
        self.assertEqual(SQUARED_ROWS[0][0].exponent, 2)
        self.assertEqual(SQUARED_ROWS[0][1].exponent, -4)

    def test_published_squared_stage_contains_every_certified_cut_row(self):
        page = build_squared_html()
        self.assertEqual(SQUARED_OUTPUT.read_text(encoding='utf-8'), page)
        self.assertEqual(page.count('class="factor-row"'), 23)
        self.assertEqual(page.count('data-projection="smooth"'), 23)
        self.assertIn('The inserted middle column exposes the cyclic step', page)


if __name__ == '__main__':
    unittest.main()
