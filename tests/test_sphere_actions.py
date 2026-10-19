import unittest
from unittest.mock import patch

from surface_diagrams.factorization_explorer import initial_factors,move_factor,product
from surface_diagrams.braid_actions import free_homotopy_key,inverse_word,reduce_word
from surface_diagrams.mapping_classes import ConjugatedTwist,VerificationLimitError,exact_action,supported_class
from surface_diagrams.sphere_actions import sphere_curve_action,sphere_inner_certificate,sphere_reduce,sphere_chain_certificate,sphere_supported_class


class SphereActionTests(unittest.TestCase):
    def test_supported_sphere_classes_agree_with_disk_reduction_including_infinity(self):
        for g in ((), (5,), (3, -5, 2, 1)):
            for first, points in ((1, 2), (5, 2), (2, 3)):
                twist = ConjugatedTwist(g, first, points)
                expected = free_homotopy_key(sphere_reduce(supported_class(twist)))
                self.assertEqual(sphere_supported_class(twist), expected)
                self.assertEqual(sphere_supported_class(ConjugatedTwist(g, first, points, 2)), expected)
        with self.assertRaises(ValueError): sphere_supported_class(None)
        with self.assertRaises(ValueError): sphere_supported_class(ConjugatedTwist((), 6, 2))
        with self.assertRaises(VerificationLimitError):
            sphere_supported_class(ConjugatedTwist((2,), 1, 2), max_letters=2)

    def test_supported_sphere_class_discards_peripheral_whiskers_during_transport(self):
        peripheral = (1, 2, 3, 4, 5, 5, 4, 3, 2, 1)
        self.assertTrue(sphere_chain_certificate(peripheral)['certified'])
        twist = ConjugatedTwist(peripheral * 20 + (3, -5, 2, 1), 5, 2)
        expected = sphere_supported_class(ConjugatedTwist((3, -5, 2, 1), 5, 2))
        self.assertEqual(sphere_supported_class(twist), expected)

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

    def test_five_sphere_chain_arcs_certify_the_whole_mapping_class(self):
        for braid in ((), tuple(range(1, 6)) * 6, tuple(range(2, 6)) * 5,
                      product(initial_factors())):
            result = sphere_chain_certificate(braid)
            self.assertTrue(result['certified'])
            self.assertTrue(result['endpoints_fixed'])
            self.assertEqual(result['reference_classes'], result['image_classes'])
            self.assertTrue(sphere_inner_certificate(braid)['certified'])
        # T34 fixes the first arc but moves later ones. A single-arc or pure
        # permutation test would incorrectly accept this nonidentity.
        result = sphere_chain_certificate((3, 3))
        self.assertTrue(result['endpoints_fixed'])
        self.assertEqual(result['reference_classes'][0], result['image_classes'][0])
        self.assertNotEqual(result['reference_classes'], result['image_classes'])
        self.assertFalse(result['certified'])
        # A separating genus-two twist has homology I but nontrivial sphere action.
        self.assertFalse(sphere_chain_certificate((1, 2) * 6)['certified'])
        self.assertFalse(sphere_chain_certificate((1,))['endpoints_fixed'])
        def only_generator_actions(word, *args, **kwargs):
            self.assertEqual(len(word), 1, 'The arc certificate must not expand the full disk action')
            return exact_action(word, *args, **kwargs)
        with patch('surface_diagrams.sphere_actions.exact_action', side_effect=only_generator_actions):
            self.assertTrue(sphere_chain_certificate(product(initial_factors()))['certified'])
        with self.assertRaises(VerificationLimitError):
            sphere_chain_certificate((2,), max_letters=2)
