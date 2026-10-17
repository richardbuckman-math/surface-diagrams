import unittest

from surface_diagrams.factorization_explorer import initial_factors,move_factor,product
from surface_diagrams.braid_actions import free_homotopy_key,inverse_word,reduce_word
from surface_diagrams.mapping_classes import VerificationLimitError,exact_action
from surface_diagrams.sphere_actions import sphere_curve_action,sphere_inner_certificate,sphere_reduce


class SphereActionTests(unittest.TestCase):
    def test_boundary_relation_and_input_validation(self):
        self.assertEqual(sphere_reduce((1,2,3,4,5,6)),())
        self.assertEqual(sphere_reduce((6,)),(-5,-4,-3,-2,-1))
        with self.assertRaises(ValueError): sphere_reduce((7,))

    def test_six_seven_has_verified_common_inner_action(self):
        certificate=sphere_inner_certificate(product(initial_factors()))
        self.assertTrue(certificate['certified'])
        self.assertFalse(certificate['disk_identity'])
        self.assertEqual(len(certificate['conjugator']),58)
        self.assertEqual(certificate['images'],certificate['expected'])
        moved=move_factor(initial_factors(),1,2)
        after=sphere_inner_certificate(product(moved))
        self.assertTrue(after['certified'])
        self.assertEqual(after['images'],certificate['images'])

    def test_identity_central_twist_and_nonidentity(self):
        self.assertTrue(sphere_inner_certificate(())['certified'])
        central=sphere_inner_certificate(tuple(range(1,6))*6)
        self.assertTrue(central['certified'])
        self.assertFalse(central['disk_identity'])
        self.assertEqual(central['conjugator'],())
        self.assertFalse(sphere_inner_certificate((1,))['certified'])
        self.assertFalse(sphere_inner_certificate((1,1))['certified'])

    def test_curve_action_agrees_with_full_based_action_including_infinity(self):
        for braid in ((), (5,), (3, -5, 2, 1)):
            images = exact_action(braid)
            for path in ((1, 2), (5, 6), (2, 3, 4)):
                expected = free_homotopy_key(sphere_reduce(reduce_word(
                    letter for symbol in path for letter in images[symbol - 1])))
                self.assertEqual(sphere_curve_action(braid, path), expected)
                self.assertEqual(sphere_curve_action(braid, (3,) + path + (-3,)), expected)
                self.assertEqual(sphere_curve_action(braid, inverse_word(path)), expected)
        with self.assertRaises(VerificationLimitError):
            sphere_curve_action((2,), (1, 2), max_letters=2)
