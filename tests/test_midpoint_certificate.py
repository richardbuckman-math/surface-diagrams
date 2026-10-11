import unittest

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import initial_factors, move_factor, product
from surface_diagrams.midpoint_certificate import (
    six_seven_midpoint_certificate, sphere_split_certificate)
from surface_diagrams.sphere_actions import sphere_reduce


class MidpointCertificateTests(unittest.TestCase):
    def test_seven_six_split_has_exact_sphere_but_not_disk_equality(self):
        factors = initial_factors()
        certificate = six_seven_midpoint_certificate()
        self.assertEqual(certificate.forward_factor_ids,
                         tuple(f'F{i}' for i in range(1, 8)))
        self.assertEqual(certificate.backward_inverse_factor_ids,
                         tuple(f'F{i}' for i in range(13, 7, -1)))
        self.assertEqual(certificate.forward_braid, product(factors[:7]))
        self.assertEqual(certificate.backward_inverse_braid,
                         inverse_word(product(factors[7:])))
        self.assertTrue(certificate.sphere_equal)
        self.assertFalse(certificate.disk_equal)

        # Independently reconstruct all six quotient images and the common
        # basepoint change from the retained exact disk witnesses.
        whisker = certificate.common_whisker
        for actual_disk, backward_disk, actual_sphere, expected in zip(
                certificate.forward_disk_images,
                certificate.backward_disk_images,
                certificate.forward_sphere_images,
                certificate.expected_sphere_images):
            self.assertEqual(actual_sphere, sphere_reduce(actual_disk))
            self.assertEqual(expected, reduce_word(
                whisker + sphere_reduce(backward_disk) + inverse_word(whisker)))
            self.assertEqual(actual_sphere, expected)
        self.assertEqual(len(certificate.common_whisker), 58)

    def test_five_sphere_chain_arc_chart_sizes_and_exponent_obstruction(self):
        certificate = six_seven_midpoint_certificate()
        self.assertEqual(certificate.forward_pairwise_chart_cut_counts,
                         (147, 220, 40, 275, 68))
        self.assertEqual(certificate.backward_pairwise_chart_cut_counts,
                         (166, 435, 82, 485, 125))
        self.assertEqual(certificate.forward_sphere_meridian_lengths,
                         (61, 115, 117, 131, 113, 81))
        self.assertEqual(certificate.backward_sphere_meridian_lengths,
                         (55, 99, 101, 115, 77, 45))
        self.assertEqual(sum(1 if x > 0 else -1 for x in certificate.forward_braid), 40)
        self.assertEqual(sum(1 if x > 0 else -1 for x in certificate.backward_inverse_braid), -50)

    def test_general_split_works_after_hurwitz_move(self):
        moved = move_factor(initial_factors(), 1, 2)
        certificate = sphere_split_certificate(moved, 11)
        self.assertEqual(certificate.split_index, 11)
        self.assertEqual(certificate.forward_factor_ids, tuple(f.id for f in moved[:11]))
        self.assertEqual(certificate.backward_inverse_factor_ids,
                         tuple(f.id for f in reversed(moved[11:])))
        self.assertTrue(certificate.sphere_equal)
        self.assertFalse(certificate.disk_equal)
        self.assertEqual(len(certificate.forward_pairwise_chart_cut_counts), 5)
        self.assertEqual(len(certificate.backward_pairwise_chart_cut_counts), 5)

    def test_unverified_full_product_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Full product has no certified sphere identity'):
            sphere_split_certificate(initial_factors()[:-1], 7)
        with self.assertRaisesRegex(ValueError, 'Split index'):
            sphere_split_certificate(initial_factors(), 13)


if __name__ == '__main__':
    unittest.main()
