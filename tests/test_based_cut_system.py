import unittest

from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.based_cut_system import (based_arc_from_meridian,based_arc_ray_word,
                                          based_cut_system_drawing,based_arc_drawing)
from surface_diagrams.factorization_explorer import initial_factors,product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.visuals import RAINBOW


class BasedCutSystemTests(unittest.TestCase):
    def test_recovered_early_prefix_arcs_encode_complete_based_images(self):
        factors=initial_factors()
        for prefix in range(9):
            for image in exact_action(product(factors[:prefix])):
                arc=based_arc_from_meridian(image)
                self.assertEqual(arc.start,0)
                path=based_arc_ray_word(arc)
                self.assertEqual(reduce_word(path+(arc.end,)+inverse_word(path)),image)

    def test_six_arcs_route_together_until_stated_limit(self):
        factors=initial_factors()
        for prefix in (0,2,5):
            svg=based_cut_system_drawing(exact_action(product(factors[:prefix])))
            self.assertIn('svg',svg)
            self.assertIn('#d73027',svg)
            self.assertIn('#5254c8',svg)
        with self.assertRaisesRegex(ValueError,'limit|1024'):
            based_cut_system_drawing(exact_action(product(factors[:13])))

    def test_late_individual_arc_routes_without_claiming_joint_cut_system(self):
        images=exact_action(product(initial_factors()[:8]))
        svg=based_arc_drawing(images[1],index=1)
        self.assertIn('svg',svg)
        self.assertIn('#e08214',svg)
        arc=based_arc_from_meridian(images[1])
        path=based_arc_ray_word(arc)
        self.assertEqual(reduce_word(path+(arc.end,)+inverse_word(path)),images[1])
        with self.assertRaises(ValueError): based_arc_drawing(images[1],index=6)

    def test_eighth_prefix_routes_all_six_exact_arcs_together(self):
        images=exact_action(product(initial_factors()[:8]))
        self.assertGreater(sum(len(based_arc_from_meridian(image).cuts)+2 for image in images),1024)
        svg=based_cut_system_drawing(images)
        self.assertIn('<svg',svg)
        for color in RAINBOW[:6]:
            self.assertIn(color,svg)

    def test_non_meridians_and_wrong_endpoints_are_rejected(self):
        with self.assertRaises(ValueError): based_arc_from_meridian((1,2))
        with self.assertRaises(ValueError): based_arc_from_meridian((-1,))
        with self.assertRaises(ValueError): based_cut_system_drawing(((1,),))
