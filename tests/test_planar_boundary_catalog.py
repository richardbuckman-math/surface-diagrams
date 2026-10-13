"""Checks for the framed-boundary incidence candidate catalog."""

from collections import Counter
from itertools import combinations, combinations_with_replacement
from fractions import Fraction
import json
from pathlib import Path
import unittest

from surface_diagrams.planar_boundary_catalog import (
    _isomorphic, incidence, lines, pattern_sort_key, structural_types,
)
from surface_diagrams.line_arrangement_relations import arrangement_intersections


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

    def test_saved_types_follow_largest_support_profile(self):
        for n in range(3, 11):
            types = json.loads((DATA / f'{n}.json').read_text(encoding='utf-8'))['types']
            keys = [pattern_sort_key(n, raw) for raw in types]
            self.assertEqual(keys, sorted(keys))

    def test_every_saved_line_certificate_is_exact(self):
        for n in range(3, 11):
            types = json.loads((DATA / f'{n}.json').read_text(encoding='utf-8'))['types']
            path = DATA / f'{n}-relations.json'
            if not path.exists():
                continue
            certificates = json.loads(path.read_text(encoding='utf-8'))
            for key, certificate in certificates.items():
                with self.subTest(n=n, pattern=key):
                    index = int(key)
                    self.assertLess(index, len(types))
                    slopes = tuple(map(Fraction, certificate['slopes']))
                    intercepts = tuple(map(Fraction, certificate['intercepts']))
                    intersections = arrangement_intersections(slopes, intercepts)
                    self.assertIsNotNone(intersections)
                    factors = tuple(block for _, _, block in intersections)
                    target = lines(n, types[index])
                    self.assertEqual(tuple(sorted(factors, key=lambda b: (-len(b), b))), target)
                    self.assertEqual([list(block) for block in factors],
                                     certificate['ordered_factors'])
                    self.assertEqual([str(x) for x, _, _ in intersections],
                                     certificate['x_values'])
                    self.assertTrue(all(x < y for (x, _, _), (y, _, _)
                                        in zip(intersections, intersections[1:])))
                    # Multiplying two such relations gives a certified
                    # double-outer relation with nonnegative inner powers.
                    degrees = [sum(point in block for block in factors)
                               for point in range(1, n+1)]
                    self.assertTrue(all(degree >= 1 for degree in degrees))

    def test_double_outer_compositions_have_pair_multiplicity_two(self):
        for n in (3, 4, 5):
            certificates = json.loads((DATA / f'{n}-relations.json').read_text(encoding='utf-8'))
            for left, right in combinations_with_replacement(tuple(certificates.values()), 2):
                factors = left['ordered_factors'] + right['ordered_factors']
                pair_counts = Counter(pair for block in factors
                                      for pair in combinations(block, 2))
                self.assertTrue(all(pair_counts[pair] == 2
                                    for pair in combinations(range(1, n+1), 2)))
                powers = [sum(point in block for block in factors) - 2
                          for point in range(1, n+1)]
                self.assertTrue(all(power >= 0 for power in powers))


if __name__ == '__main__':
    unittest.main()
