"""Sphere shortening must retain the lift, cap and explicit scope."""
from dataclasses import replace
import unittest

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import ConjugatedTwist
from surface_diagrams.sphere_actions import sphere_supported_class
from surface_diagrams.sphere_support_compact import (
    check_support_replacement, compact_sphere_support, reframe_factors)
from surface_diagrams.six_seven_structure import SignedResearchFactor


class SphereSupportCompactTests(unittest.TestCase):
    def test_complementary_triple_root_is_rejected_but_square_is_certified(self):
        source = ConjugatedTwist((), 1, 3)
        complement = replace(source, first=4)
        self.assertEqual(sphere_supported_class(source), sphere_supported_class(complement))
        with self.assertRaisesRegex(ValueError, 'genus-two lift'):
            check_support_replacement(source, complement)
        result = check_support_replacement(replace(source, power=2),
                                           replace(complement, power=2))
        self.assertEqual(result['kind'], 'sphere_rewrite')
        self.assertFalse(result['disk_equal'])
        self.assertTrue(result['sphere_certificate']['certified'])
        self.assertEqual(result['lift_homology'], IDENTITY)
        self.assertTrue(result['disk_discrepancy'])

    def test_point_push_clutter_is_removed_with_a_recorded_sphere_discrepancy(self):
        sphere_word = (1,2,3,4,5,5,4,3,2,1)
        source = ConjugatedTwist(sphere_word, 1, 3, power=2)
        result = compact_sphere_support(source, max_cuts=4)
        self.assertEqual(result['status'], 'certified')
        self.assertLessEqual(result['cuts'], 4)
        self.assertFalse(result['disk_equal'])
        candidate = ConjugatedTwist(**result['candidate'])
        discrepancy = reduce_word(source.word + inverse_word(candidate.word))
        self.assertEqual(discrepancy, result['disk_discrepancy'])
        self.assertEqual(homology_action(discrepancy), IDENTITY)

    def test_a_failed_work_or_drawing_budget_never_relaxes_the_cap(self):
        source = ConjugatedTwist((), 1, 3)
        result = compact_sphere_support(source, max_cuts=1, max_states=1)
        self.assertIsNone(result['candidate'])
        self.assertEqual(result['status'], 'bounded_failure')
        self.assertEqual(result['max_cuts'], 1)
        self.assertLessEqual(result['states'], 1)
        with self.assertRaisesRegex(ValueError, 'cut-visit cap'):
            check_support_replacement(source, source, max_cuts=1)

    def test_invalid_core_and_class_are_rejected(self):
        source = ConjugatedTwist((), 1, 2, half=True)
        with self.assertRaisesRegex(ValueError, 'core type'):
            check_support_replacement(source, replace(source, half=False))
        with self.assertRaisesRegex(ValueError, 'sphere support'):
            check_support_replacement(source, replace(source, first=3))

    def test_global_frame_telescopes_for_signed_factors_without_asserting_equality(self):
        factors = (Factor('a', (), 1, 2, half=True),
                   SignedResearchFactor('b', (3,-2), 2, 3, sign=-1))
        g = (2,-4,1)
        result = reframe_factors(factors, g)
        self.assertEqual(result['kind'], 'global_conjugation')
        self.assertEqual(reduce_word(product(result['factors'])),
                         reduce_word(g + product(factors) + inverse_word(g)))
        self.assertEqual(result['word_certificate']['discrepancy'], ())
        self.assertEqual(result['factors'][1].sign, -1)
        with self.assertRaisesRegex(ValueError, 'generators'):
            reframe_factors(factors, (6,))


if __name__ == '__main__':
    unittest.main()
