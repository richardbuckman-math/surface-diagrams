import unittest

from surface_diagrams.factorization_explorer import initial_factors,move_factor,product
from surface_diagrams.sphere_actions import sphere_inner_certificate,sphere_reduce


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
