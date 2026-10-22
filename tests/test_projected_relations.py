"""Exact disk checks for the puncture-capped daisy and rose derivations."""

import unittest
from dataclasses import replace

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import initial_factors
from surface_diagrams.mapping_classes import ConjugatedTwist, exact_action
from surface_diagrams.projected_relations import (
    pc_daisy_terms, pc_half_lantern_terms, pc_rose_terms, pc_lantern_petal_cycle_terms,
)


def product(terms):
    return tuple(letter for term in terms for letter in term.word)


class ProjectedRelationsTests(unittest.TestCase):
    def test_four_point_daisy_and_its_two_lantern_steps(self):
        twist = lambda first, points, g=(): ConjugatedTwist(g, first, points)
        outer, inner = twist(1, 4), twist(1, 2)
        t123, t34 = twist(1, 3), twist(3, 2)
        t124_under = twist(1, 3, (-3,))
        t24_under, t14_under = twist(2, 2, (-3,)), twist(1, 2, (-3, -2))

        # First PC lantern regards {1,2}, 3, and 4 as its three entries.
        self.assertEqual(exact_action(outer.word + inner.word, 4),
                         exact_action(product((t123, t34, t124_under)), 4))
        # Second PC lantern splits the under-going {1,2,4} curve.
        self.assertEqual(exact_action(t124_under.word, 4),
                         exact_action(product((t24_under, t14_under, inner)), 4))
        # The two copies of T12 are now at the right and cancel.
        expected = (t123, t34, t24_under, t14_under)
        self.assertEqual(pc_daisy_terms(outer), expected)
        self.assertEqual(exact_action(outer.word, 4), exact_action(product(expected), 4))
        self.assertEqual(t24_under.word, (-3, 2, 2, 3))
        self.assertEqual(t14_under.word, (-3, -2, 1, 1, 2, 3))

    def test_recursive_daisy_and_pairwise_rose(self):
        for count in range(3, 7):
            with self.subTest(points=count):
                outer = ConjugatedTwist((), 1, count)
                daisy = pc_daisy_terms(outer)
                rose = pc_rose_terms(outer)
                self.assertEqual(len(daisy), count)
                self.assertEqual(len(rose), count * (count - 1) // 2)
                self.assertTrue(all(term.points == 2 for term in rose))
                self.assertEqual(exact_action(product(daisy), count), exact_action(outer.word, count))
                self.assertEqual(exact_action(product(rose), count), exact_action(outer.word, count))

    def test_relation_transports_with_an_outer_conjugator(self):
        outer = ConjugatedTwist((4, -2), 2, 4)
        self.assertEqual(exact_action(product(pc_daisy_terms(outer))), exact_action(outer.word))
        self.assertEqual(exact_action(product(pc_rose_terms(outer))), exact_action(outer.word))

    def test_half_lantern_matches_checked_hurwitz_walk(self):
        for conjugator, first, strands in (((), 1, 3), ((2, -1), 2, 4)):
            with self.subTest(conjugator=conjugator):
                outer = ConjugatedTwist(conjugator, first, 3)
                halves = pc_half_lantern_terms(outer)
                self.assertEqual([(term.half, term.power) for term in halves],
                                 [(True, 1), (True, 1), (False, 2)])
                self.assertEqual(exact_action(product(halves), strands),
                                 exact_action(outer.word, strands))

    def test_petal_cycle_retains_three_actual_swaps_and_transports_with_the_root(self):
        for g, first, strands in (((), 1, 3), ((-4, -3), 1, 5), ((3, -1), 2, 5)):
            root = ConjugatedTwist(g, first, 3)
            before, after = pc_lantern_petal_cycle_terms(root)
            current = before
            for _ in range(3):
                a, b = current
                current = (b, replace(a, conjugator=inverse_word(b.word) + a.conjugator))
            self.assertEqual(exact_action(product(before), strands), exact_action(product(after), strands))
            for actual, expected in zip(current, after):
                self.assertEqual(exact_action(actual.word, strands), exact_action(expected.word, strands))
            self.assertTrue(all(not f.half and f.power == 1 and f.points == 2 for f in before + after))
        for bad in (ConjugatedTwist((), 1, 2), ConjugatedTwist((), 1, 3, power=2),
                    ConjugatedTwist((), 1, 2, half=True)):
            with self.assertRaises(ValueError):
                pc_lantern_petal_cycle_terms(bad)

    def test_six_seven_half_lantern_first_arc_pairing(self):
        factors = {factor.id: factor for factor in initial_factors()}
        self.assertEqual(
            [factor.id for factor in factors.values() if not factor.half],
            ['F1', 'F4', 'F5', 'F8', 'F10', 'F12', 'F13'],
        )
        standard_h34 = exact_action((3,))
        for factor_id in ('F1', 'F8', 'F13'):
            with self.subTest(factor=factor_id):
                unit = replace(factors[factor_id].mapping_class, power=1)
                terms = pc_half_lantern_terms(unit)
                self.assertEqual(exact_action(product(terms)), exact_action(unit.word))
                self.assertEqual(exact_action(terms[0].word), standard_h34)


if __name__ == '__main__':
    unittest.main()
