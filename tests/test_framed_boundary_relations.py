"""Full braid and framing checks for non-composite boundary relations."""

import json
from pathlib import Path
import unittest

from surface_diagrams.double_boundary_catalog import canonical_blocks
from surface_diagrams.framed_boundary_relations import (
    enclosed_boundaries, five_boundary_lifts, four_triple_relations,
    framed_outer_certificate,
)
from surface_diagrams.mapping_classes import ConjugatedTwist, exact_action
from surface_diagrams.projected_relations import pc_daisy_terms, pc_rose_terms


DATA = Path(__file__).resolve().parents[1] / 'docs' / 'boundary-factorizations' / 'data'


class FramedBoundaryRelationTests(unittest.TestCase):
    def test_lantern_and_daisy_calibrate_framing_convention(self):
        outer3 = ConjugatedTwist((), 1, 3)
        outer4 = ConjugatedTwist((), 1, 4)
        self.assertEqual(framed_outer_certificate(3, pc_rose_terms(outer3), 1),
                         (1, 1, 1))
        self.assertEqual(framed_outer_certificate(4, pc_daisy_terms(outer4), 1),
                         (1, 1, 1, 2))

    def test_seed_and_lantern_expansions_cover_all_three_open_n4_types(self):
        patterns = json.loads((DATA / '4-double.json').read_text(encoding='utf-8'))['patterns']
        actual = []
        for relation in four_triple_relations():
            factors = relation['factors']
            supports = tuple(enclosed_boundaries(factor, 4) for factor in factors)
            kind = canonical_blocks(4, supports)
            index = next(index for index, pattern in enumerate(patterns)
                         if kind == tuple(tuple(block) for block in pattern['blocks']))
            actual.append(index)
            self.assertEqual(tuple(relation['inner_powers']),
                             framed_outer_certificate(4, factors, 2))
        self.assertEqual(actual, [3, 4, 6])
        self.assertEqual([len(relation['factors']) for relation in four_triple_relations()],
                         [4, 6, 8])

    def test_published_direct_rows_replay_and_have_exact_support_images(self):
        root = DATA.parent
        patterns = json.loads((DATA / '4-double.json').read_text(encoding='utf-8'))['patterns']
        self.assertEqual([index for index, row in enumerate(patterns) if row.get('direct')],
                         [3, 4, 6])
        for row in patterns:
            direct = row.get('direct')
            if direct is None:
                continue
            factors = tuple(ConjugatedTwist(tuple(factor['conjugator']),
                                             factor['first'], factor['points'])
                            for factor in direct['factors'])
            self.assertEqual(list(framed_outer_certificate(4, factors, 2)),
                             direct['inner_powers'])
            self.assertEqual(canonical_blocks(4, [enclosed_boundaries(factor, 4)
                                                  for factor in factors]),
                             tuple(tuple(block) for block in row['blocks']))
            for factor, saved in zip(factors, direct['factors']):
                self.assertEqual(list(enclosed_boundaries(factor, 4)), saved['support'])
                picture = root / saved['svg']
                self.assertTrue(picture.is_file())
                self.assertIn('<svg ', picture.read_text(encoding='utf-8'))

    def test_every_local_lantern_expansion_preserves_exact_disk_braid(self):
        seed = four_triple_relations()[0]['factors']
        for factor in seed[2:]:
            replacement = pc_rose_terms(factor)
            word = tuple(letter for term in replacement for letter in term.word)
            self.assertEqual(exact_action(word, 4), exact_action(factor.word, 4))

    def test_five_boundary_daisy_lifts_certify_three_new_types(self):
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        outer5 = ConjugatedTwist((), 1, 5)
        prefix, *petals = pc_daisy_terms(outer5)
        petal_word = tuple(letter for factor in petals for letter in factor.word)
        self.assertEqual(framed_outer_certificate(5, (prefix, *petals), 1),
                         (1, 1, 1, 1, 3))
        self.assertEqual(exact_action(prefix.word + petal_word, 5),
                         exact_action(petal_word + prefix.word, 5))
        actual = []
        for relation in five_boundary_lifts():
            factors = relation['factors']
            core_length = relation['core_factor_count']
            self.assertEqual(tuple(factors[core_length:]), tuple(petals) * 2)
            self.assertEqual(tuple(relation['inner_powers']),
                             framed_outer_certificate(5, factors, 2))
            kind = canonical_blocks(5, [enclosed_boundaries(factor, 5)
                                        for factor in factors])
            index = next(index for index, pattern in enumerate(patterns)
                         if kind == tuple(tuple(block) for block in pattern['blocks']))
            self.assertIsNone(patterns[index]['composition'])
            actual.append(index)
        self.assertEqual(actual, [24, 29, 33])

    def test_published_five_boundary_lifts_replay_and_have_exact_images(self):
        root = DATA.parent
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        self.assertEqual([i for i, row in enumerate(patterns) if row.get('direct')],
                         [24, 29, 33])
        for index in (24, 29, 33):
            direct = patterns[index]['direct']
            factors = tuple(ConjugatedTwist(tuple(row['conjugator']),
                                             row['first'], row['points'])
                            for row in direct['factors'])
            self.assertEqual(list(framed_outer_certificate(5, factors, 2)),
                             direct['inner_powers'])
            self.assertEqual(len(factors), direct['core_factor_count'] + 8)
            for factor, row in zip(factors, direct['factors']):
                self.assertEqual(list(enclosed_boundaries(factor, 5)), row['support'])
                self.assertTrue((root / row['svg']).is_file())

    def test_wrong_factor_order_or_target_power_is_rejected(self):
        factors = four_triple_relations()[0]['factors']
        with self.assertRaisesRegex(ValueError, 'action'):
            framed_outer_certificate(4, (factors[1], factors[0], *factors[2:]), 2)
        with self.assertRaisesRegex(ValueError, 'Pair winding'):
            framed_outer_certificate(4, factors, 1)


if __name__ == '__main__':
    unittest.main()
