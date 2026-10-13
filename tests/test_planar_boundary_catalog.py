"""Checks for the framed-boundary incidence candidate catalog."""

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import unittest

from surface_diagrams.planar_boundary_catalog import (
    _isomorphic, incidence, lines, structural_types,
)


DATA = Path(__file__).resolve().parents[1] / 'docs' / 'boundary-factorizations' / 'data'
COUNTS = {1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 6: 10, 7: 24, 8: 69, 9: 384, 10: 5250}


class PlanarBoundaryCatalogTests(unittest.TestCase):
    def test_every_saved_pattern_has_target_pair_and_boundary_counts(self):
        for n, count in COUNTS.items():
            with self.subTest(n=n):
                saved = json.loads((DATA / f'{n}.json').read_text(encoding='utf-8'))
                self.assertEqual(saved['n'], n)
                self.assertEqual(len(saved['types']), count)
                for raw_large in saved['types']:
                    blocks, singletons = incidence(n, raw_large)
                    pairs = Counter(p for block in blocks for p in combinations(block, 2))
                    self.assertEqual(set(pairs), set(combinations(range(1, n+1), 2)))
                    self.assertTrue(all(value == 1 for value in pairs.values()))
                    for point in range(1, n+1):
                        self.assertEqual(sum(point in block for block in blocks)
                                         + singletons[point-1], 1)

    def test_small_structural_counts_and_nonisomorphic_representatives(self):
        for n in range(1, 9):
            with self.subTest(n=n):
                types = structural_types(n)
                self.assertEqual(len(types), COUNTS[n])
                self.assertTrue(all(not _isomorphic(n, left, right)
                                    for left, right in combinations(types, 2)))

    def test_single_boundary_power_and_invalid_overlap(self):
        blocks, singleton = incidence(3)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(singleton, (-1, -1, -1))
        self.assertEqual(incidence(3, ((1, 2, 3),), inner_power=2)[1], (2, 2, 2))
        with self.assertRaises(ValueError):
            lines(4, ((1, 2, 3), (1, 2, 4)))


if __name__ == '__main__':
    unittest.main()
