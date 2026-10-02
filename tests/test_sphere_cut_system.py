import unittest

from surface_diagrams.factorization_explorer import initial_factors,product
from surface_diagrams.sphere_cut_system import sphere_chart_drawing


class SphereCutSystemTests(unittest.TestCase):
    def test_full_product_recovers_standard_five_arc_chart(self):
        svg,whisker=sphere_chart_drawing(product(initial_factors()))
        self.assertEqual(len(whisker),58)
        self.assertIn('<svg',svg)
        self.assertIn('#d73027',svg)
        self.assertIn('#23964f',svg)
        self.assertEqual(sphere_chart_drawing(())[1],())

    def test_nontrivial_outer_action_has_no_identity_chart(self):
        with self.assertRaisesRegex(ValueError,'no identity certificate'):
            sphere_chart_drawing((1,))
