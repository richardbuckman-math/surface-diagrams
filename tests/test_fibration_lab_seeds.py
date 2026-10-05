"""Check source transcriptions and the closed genus-two lab seed."""

import unittest

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import product
from surface_diagrams.fibration_lab_seeds import (
    HYPERELLIPTIC_INVOLUTION_BRAID,
    MATSUMOTO_SIX_TWO,
    NAKAMURA_TEN_TEN,
    XIAO_FOUR_THREE,
    seed_for,
)
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.sphere_actions import sphere_inner_certificate


class FibrationLabSeedTests(unittest.TestCase):
    def test_xiao_paper_words_match_its_conjugator_formulas(self):
        # Akhmedov, arXiv:2609.17634, Section 8 and Appendix B. These are
        # exact equalities in the ordinary disk braid group, checked by its
        # faithful Artin action rather than by typography of braid strings.
        factors = XIAO_FOUR_THREE.factors
        omega = (1, 2) * 3 + (4, 5) * 3
        k1 = factors[1].conjugator
        expected = (
            factors[0].word,
            k1 + omega + inverse_word(k1),
            factors[2].word,
            factors[3].word,
            factors[4].word,
            factors[5].word,
            omega,
        )
        self.assertEqual(len(XIAO_FOUR_THREE.raw_disk_words), 7)
        for printed, decomposition in zip(XIAO_FOUR_THREE.raw_disk_words, expected):
            self.assertEqual(exact_action(printed), exact_action(decomposition))

    def test_xiao_involution_correction_and_positive_factors(self):
        negative_identity = tuple(tuple(-entry for entry in row) for row in IDENTITY)
        raw = XIAO_FOUR_THREE.raw_disk_words
        factors = XIAO_FOUR_THREE.factors
        self.assertEqual(XIAO_FOUR_THREE.involution_corrections, (1, 6))
        self.assertEqual(homology_action(HYPERELLIPTIC_INVOLUTION_BRAID), negative_identity)
        self.assertEqual(tuple(homology_action(raw[i]) for i in (1, 4, 6)),
                         (negative_identity, IDENTITY, negative_identity))
        self.assertEqual(sum(f.half for f in factors), 4)
        self.assertEqual(sum(f.points == 3 and f.power == 2 for f in factors), 3)
        for index in (1, 4, 6):
            self.assertEqual(homology_action(factors[index].word), IDENTITY)
        for index in XIAO_FOUR_THREE.involution_corrections:
            relative = (HYPERELLIPTIC_INVOLUTION_BRAID + raw[index]
                        + inverse_word(factors[index].word))
            self.assertTrue(sphere_inner_certificate(relative)['certified'])
            self.assertEqual(homology_action(relative), IDENTITY)

    def test_xiao_normalized_product_is_closed_genus_two_identity(self):
        word = product(XIAO_FOUR_THREE.factors)
        self.assertEqual(sum(1 if letter > 0 else -1 for letter in word), 40)
        self.assertTrue(sphere_inner_certificate(word)['certified'])
        self.assertEqual(homology_action(word), IDENTITY)
        # Birman-Hilden's kernel for closed genus two is {1, iota}; the
        # involution acts as -I, so sphere identity plus +I selects 1.

    def test_other_literature_entries_have_no_unverified_seed_words(self):
        self.assertIs(seed_for('4-3'), XIAO_FOUR_THREE)
        self.assertIs(seed_for('6-2'), MATSUMOTO_SIX_TWO)
        self.assertIs(seed_for('10-10'), NAKAMURA_TEN_TEN)
        for seed in (MATSUMOTO_SIX_TWO, NAKAMURA_TEN_TEN):
            self.assertFalse(seed.factors)
            self.assertFalse(seed.raw_disk_words)
        with self.assertRaises(KeyError):
            seed_for('unverified')


if __name__ == '__main__':
    unittest.main()
