"""Exact small incidence counts for a doubled exterior twist."""

import json
from itertools import combinations_with_replacement
from pathlib import Path
import unittest

from surface_diagrams.double_boundary_catalog import (
    canonical_blocks, double_outer_types, inner_boundary_powers,
)


DATA = Path(__file__).resolve().parents[1] / 'docs' / 'boundary-factorizations' / 'data'


class DoubleBoundaryCatalogTests(unittest.TestCase):
    def test_all_small_pair_twice_types_and_nonnegative_powers(self):
        for n, expected in ((2, 1), (3, 3), (4, 9)):
            with self.subTest(n=n):
                types = double_outer_types(n)
                self.assertEqual(len(types), expected)
                self.assertEqual(len(set(types)), expected)
                for blocks in types:
                    self.assertTrue(all(power >= 0 for power in
                                        inner_boundary_powers(n, blocks)))

    def test_composition_coverage_and_three_new_four_boundary_candidates(self):
        for n, covered in ((3, 3), (4, 6)):
            saved = json.loads((DATA / f'{n}-relations.json').read_text(encoding='utf-8'))
            factors = [entry['ordered_factors'] for entry in saved.values()]
            compositions = {canonical_blocks(n, left + right)
                            for left, right in combinations_with_replacement(factors, 2)}
            types = set(double_outer_types(n))
            self.assertEqual(len(compositions), covered)
            self.assertTrue(compositions <= types)
            self.assertEqual(len(types - compositions), 0 if n == 3 else 3)

    def test_published_catalog_matches_computed_types(self):
        for n in (3, 4):
            saved = json.loads((DATA / f'{n}-double.json').read_text(encoding='utf-8'))
            self.assertEqual(saved['n'], n)
            computed = double_outer_types(n)
            self.assertEqual([tuple(tuple(block) for block in row['blocks'])
                              for row in saved['patterns']], list(computed))
            relations = json.loads((DATA / f'{n}-relations.json').read_text(encoding='utf-8'))
            for row, blocks in zip(saved['patterns'], computed):
                pair = row['composition']
                if pair is None:
                    continue
                left, right = (relations[str(index)]['ordered_factors'] for index in pair)
                self.assertEqual(canonical_blocks(n, left + right), blocks)

    def test_invalid_support_or_pair_count_rejected(self):
        with self.assertRaises(ValueError):
            canonical_blocks(4, ((1, 1, 2),))
        with self.assertRaises(ValueError):
            inner_boundary_powers(3, ((1, 2), (1, 3), (2, 3)))


if __name__ == '__main__':
    unittest.main()
