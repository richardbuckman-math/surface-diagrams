import unittest

from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.curves import route
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.model import PlanarSurface, Style
from surface_diagrams.normal_certificate import certify_arc_orders
from surface_diagrams.normal_gluing import arc_triangles, glue_triangles
from surface_diagrams.normal_order import resolve_arc_orders
from surface_diagrams.normal_strands import (
    NormalTriangleError, joint_arc_cut_orders, joint_arc_ray_orders,
)


class NormalCertificateTests(unittest.TestCase):
    def test_route_free_f1_orders_certify_both_winding_arcs(self):
        arcs = chain_arcs(exact_action(product(initial_factors()[:1])))
        rays, cuts = resolve_arc_orders(arcs, owners=(3, 6))
        paths = certify_arc_orders(arcs, rays, cuts, owners=(3, 6))
        self.assertEqual(tuple(path.owner for path in paths), (3, 6))
        self.assertEqual(tuple(len(path.crossings) for path in paths), (14, 14))

        wrong = dict(rays)
        visits = list(wrong['upper', 3])
        visits[0], visits[1] = visits[1], visits[0]
        wrong['upper', 3] = tuple(visits)
        with self.assertRaises(NormalTriangleError):
            certify_arc_orders(arcs, wrong, cuts, owners=(3, 6))

    def test_rejects_wrong_itinerary_even_when_gluing_accepts(self):
        arc = chain_arcs(exact_action(product(initial_factors()[:1])))[2]
        surface = PlanarSurface.row('PPPPPP', spacing=50, height=220, margin=55)
        pieces = route(surface.with_curves(arc), Style())
        xs = ((-surface.width / 2,) +
              tuple(point.x for point in surface.objects) +
              (surface.width / 2,))
        rays = joint_arc_ray_orders((arc,), pieces, xs)
        cuts = joint_arc_cut_orders((arc,), pieces, xs)
        wrong = dict(rays)
        visits = list(wrong['upper', 3])
        visits[0], visits[1] = visits[1], visits[0]
        wrong['upper', 3] = tuple(visits)

        # Owner and endpoint checks alone miss this valid-looking placement.
        triangles, expected = arc_triangles((arc,), wrong, cuts, owners=(1,))
        path, = glue_triangles(triangles, expected)
        self.assertEqual((path.start.vertex, path.end.vertex), ('p2', 'p3'))
        with self.assertRaisesRegex(NormalTriangleError, 'itinerary mismatch'):
            certify_arc_orders((arc,), wrong, cuts)


if __name__ == '__main__':
    unittest.main()
