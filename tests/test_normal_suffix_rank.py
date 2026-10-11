import unittest

from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.curves import Arc, route
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.model import PlanarSurface, Style
from surface_diagrams.normal_certificate import certify_arc_orders
from surface_diagrams.normal_gluing import TerminalVisit
from surface_diagrams.normal_itinerary import (
    LocalTriangleConnection, arc_local_connections,
)
from surface_diagrams.normal_order import resolve_arc_orders as compare_arc_orders
from surface_diagrams.normal_strands import (
    ArcRayVisit, LabeledCutVisit, LabeledRayVisit, NormalTriangleError,
    StrandVisit,
    joint_arc_cut_orders, joint_arc_ray_orders,
)
from surface_diagrams.normal_suffix_rank import (
    resolve_arc_orders, resolve_connection_orders,
)


class NormalSuffixRankTests(unittest.TestCase):
    @staticmethod
    def _chain(count):
        return chain_arcs(exact_action(product(initial_factors()[:count])))

    def test_f1_f2_match_comparison_resolver_and_accepted_route(self):
        surface = PlanarSurface.row('PPPPPP', spacing=50, height=220, margin=55)
        xs = ((-surface.width / 2,)
              + tuple(point.x for point in surface.objects)
              + (surface.width / 2,))
        for count, owners in ((1, (3, 6)), (2, (3, 4, 5, 6))):
            with self.subTest(factor_count=count):
                arcs = self._chain(count)
                inferred = resolve_arc_orders(arcs, owners=owners)
                self.assertEqual(inferred,
                                 compare_arc_orders(arcs, owners=owners))
                self.assertEqual(inferred,
                                 resolve_arc_orders(arcs,
                                                    owners=tuple(reversed(owners))))
                connections = tuple(connection for owner in owners
                                    for connection in arc_local_connections(
                                        arcs[owner - 1], owner=owner))
                self.assertEqual(inferred,
                                 resolve_connection_orders(reversed(connections)))
                self.assertEqual(len(certify_arc_orders(
                    arcs, *inferred, owners=owners)), len(owners))

                pieces = route(surface.with_curves(*arcs), Style())
                self.assertEqual(inferred[0],
                                 joint_arc_ray_orders(arcs, pieces, xs))
                self.assertEqual(inferred[1],
                                 joint_arc_cut_orders(arcs, pieces, xs))

    def test_f11_full_orders_have_exact_event_certificate(self):
        arcs = self._chain(11)
        rays, cuts = resolve_arc_orders(arcs)
        self.assertEqual(sum(map(len, rays.values())), 10745)
        self.assertEqual(sum(map(len, cuts.values())), 4683)
        paths = certify_arc_orders(arcs, rays, cuts)
        self.assertEqual(tuple(path.owner for path in paths),
                         (1, 2, 3, 4, 5, 6))
        self.assertEqual(tuple(len(path.crossings) for path in paths),
                         (3439, 709, 5207, 291, 4392, 1390))

    def test_unanchored_suffixes_and_same_vertex_terminals_stay_ambiguous(self):
        with self.assertRaisesRegex(NormalTriangleError,
                                    'unresolved comparison'):
            resolve_arc_orders((Arc(1, 3, direction='up'),) * 2)
        with self.assertRaisesRegex(NormalTriangleError,
                                    'terminal order is unresolved'):
            resolve_arc_orders((Arc(1, 2, direction='up'),) * 2)

    def test_opposing_incident_rank_orders_conflict(self):
        a = StrandVisit(1, LabeledRayVisit(
            1, ArcRayVisit('upper', 0, 2, 1)))
        b = StrandVisit(2, LabeledRayVisit(
            2, ArcRayVisit('upper', 0, 2, 1)))

        def terminal(owner, label, vertex):
            identifier = (owner, label)
            return TerminalVisit(owner, identifier, identifier, vertex)

        connections = (
            LocalTriangleConnection(1, ('upper', 1), 2, a, 0,
                                    terminal(1, 'left', 'p1')),
            LocalTriangleConnection(2, ('upper', 1), 2, b, 1,
                                    terminal(2, 'left', 'p2')),
            LocalTriangleConnection(1, ('upper', 2), 0, a, 1,
                                    terminal(1, 'right', 'p2')),
            LocalTriangleConnection(2, ('upper', 2), 0, b, 2,
                                    terminal(2, 'right', 'p3')),
        )
        with self.assertRaisesRegex(NormalTriangleError, 'conflict'):
            resolve_connection_orders(connections)

    def test_closed_strand_component_cannot_have_finite_suffix_rank(self):
        upper = StrandVisit(1, LabeledRayVisit(
            1, ArcRayVisit('upper', 0, 2, 1)))
        lower = StrandVisit(1, LabeledRayVisit(
            1, ArcRayVisit('lower', 1, 2, -1)))
        left = StrandVisit(1, LabeledCutVisit(1, 1, 1))
        right = StrandVisit(1, LabeledCutVisit(1, 2, 2))
        loop = (
            LocalTriangleConnection(1, ('upper', 1), 1, left, 2, upper),
            LocalTriangleConnection(1, ('lower', 1), 1, left, 0, lower),
            LocalTriangleConnection(1, ('lower', 2), 2, lower, 1, right),
            LocalTriangleConnection(1, ('upper', 2), 1, right, 0, upper),
        )
        with self.assertRaisesRegex(NormalTriangleError,
                                    'directed strand suffix does not terminate'):
            resolve_connection_orders(loop)


if __name__ == '__main__':
    unittest.main()
