import unittest

from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.hyperelliptic_homology import (
    IDENTITY, braid_permutation, branch_point_orbits, half_twist_class,
    homology_action, homology_quotient,
)
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.sphere_actions import sphere_inner_certificate


class HyperellipticHomologyTests(unittest.TestCase):
    def test_chain_braid_relations_and_central_words(self):
        self.assertEqual(homology_action((1, 2, 1)),
                         homology_action((2, 1, 2)))
        self.assertEqual(homology_action((1, 3)),
                         homology_action((3, 1)))
        self.assertEqual(homology_action((2, -2)), IDENTITY)
        self.assertEqual(homology_action((1, 2, 3, 4, 5) * 6), IDENTITY)
        minus_identity = tuple(tuple(-entry for entry in row)
                               for row in IDENTITY)
        self.assertEqual(homology_action((1, 2, 3, 4, 5, 5, 4, 3, 2, 1)),
                         minus_identity)

    def test_six_seven_homology_and_branch_orbits(self):
        factors = initial_factors()
        self.assertTrue(sphere_inner_certificate(product(factors))['certified'])
        self.assertEqual(homology_action(product(factors)), IDENTITY)
        for factor in factors:
            if not factor.half:
                self.assertEqual(factor.points, 3)
                self.assertEqual(homology_action(factor.word), IDENTITY)
        halves = tuple(factor for factor in factors if factor.half)
        classes = tuple(half_twist_class(factor.conjugator, factor.first)
                        for factor in halves)
        self.assertEqual(classes, ((3, 2, 0, 1), (0, -1, 1, 0),
                                   (3, 5, -3, 1), (3, 4, -2, 1),
                                   (-6, -7, 3, -2), (3, 3, -1, 1)))
        self.assertEqual(homology_quotient(classes),
                         {'lattice_rank': 2, 'free_rank': 2, 'torsion': ()})
        def intersection(left, right):
            return (left[0] * right[2] + left[1] * right[3]
                    - left[2] * right[0] - left[3] * right[1])
        self.assertTrue(all(intersection(classes[i], classes[j]) % 4 == 0
                            for i in range(len(classes))
                            for j in range(i + 1, len(classes))))
        self.assertEqual(branch_point_orbits(factor.word for factor in factors),
                         ((1, 4), (2, 5), (3, 6)))
        pairs = tuple(tuple(i + 1 for i, label in enumerate(braid_permutation(factor.word))
                            if label != i + 1) for factor in halves)
        self.assertEqual(pairs, ((3, 6), (1, 4), (2, 5),
                                 (3, 6), (1, 4), (2, 5)))

    def test_quotient_torsion_and_validation(self):
        self.assertEqual(homology_quotient(((2, 0, 0, 0), (0, 4, 0, 0))),
                         {'lattice_rank': 2, 'free_rank': 2,
                          'torsion': (2, 4)})
        self.assertEqual(homology_quotient(()),
                         {'lattice_rank': 0, 'free_rank': 4, 'torsion': ()})
        with self.assertRaises(ValueError):
            homology_action((6,))
        with self.assertRaises(ValueError):
            braid_permutation((0,))
        with self.assertRaises(ValueError):
            half_twist_class((), 6)
        with self.assertRaises(ValueError):
            homology_quotient(((1, 2, 3),))

    def test_fixed_external_point_does_not_close(self):
        word = product(initial_factors())
        full_twist = (1, 2, 3, 4, 5) * 6
        # The braid exponent sum forces power three if it is central.
        self.assertEqual(sum(1 if letter > 0 else -1 for letter in word),
                         3 * len(full_twist))
        self.assertNotEqual(exact_action(word), exact_action(full_twist * 3))


if __name__ == '__main__':
    unittest.main()
