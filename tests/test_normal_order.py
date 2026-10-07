import unittest

from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.curves import Arc, route
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.model import PlanarSurface, Style
from surface_diagrams.normal_gluing import (
    TerminalVisit, glue_triangles, inner_arc_triangles,
)
from surface_diagrams.normal_itinerary import (
    LocalTriangleConnection, arc_local_connections,
)
from surface_diagrams.normal_order import (
    resolve_arc_orders, resolve_connection_orders,
)
from surface_diagrams.normal_strands import (
    ArcRayVisit, LabeledRayVisit, NormalTriangleError, StrandVisit,
    joint_arc_cut_orders, joint_arc_ray_orders,
)


class NormalOrderTests(unittest.TestCase):
    def test_f1_orders_come_from_itineraries_and_round_trip(self):
        arcs = chain_arcs(exact_action(product(initial_factors()[:1])))
        inferred_rays, inferred_cuts = resolve_arc_orders(arcs, owners=(3, 6))

        # Reordering the input chords or owners must not settle a geometric
        # tie. Both calls must still derive the same complete edge orders.
        connections = tuple(connection for owner in (6, 3)
                            for connection in arc_local_connections(
                                arcs[owner - 1], owner=owner))
        self.assertEqual(resolve_connection_orders(reversed(connections)),
                         (inferred_rays, inferred_cuts))
        self.assertEqual(resolve_arc_orders(arcs, owners=(6, 3)),
                         (inferred_rays, inferred_cuts))
        self.assertEqual(sum(map(len, inferred_rays.values())), 22)
        self.assertEqual(sum(map(len, inferred_cuts.values())), 6)

        triangles, expected = inner_arc_triangles(
            arcs, inferred_rays, inferred_cuts, owners=(3, 6))
        glued = glue_triangles(triangles, expected)
        self.assertEqual(tuple(path.owner for path in glued), (3, 6))
        for path in glued:
            source = arc_local_connections(arcs[path.owner - 1], owner=path.owner)
            self.assertEqual(path.start, source[0].first)
            self.assertEqual(path.end, source[-1].second)
            self.assertEqual(path.crossings,
                             tuple(StrandVisit(path.owner, connection.second.crossing)
                                   for connection in source[:-1]))

        # The accepted route is a benchmark only; it is not supplied to the
        # resolver or the gluing round trip above.
        surface = PlanarSurface.row('PPPPPP', spacing=50, height=220, margin=55)
        pieces = route(surface.with_curves(*arcs), Style())
        xs = ((-surface.width / 2,) +
              tuple(point.x for point in surface.objects) +
              (surface.width / 2,))
        self.assertEqual(inferred_rays, joint_arc_ray_orders(arcs, pieces, xs))
        self.assertEqual(inferred_cuts, joint_arc_cut_orders(arcs, pieces, xs))

    def test_unanchored_parallel_chords_report_ambiguity(self):
        parallel = Arc(1, 3, direction='up')
        with self.assertRaisesRegex(NormalTriangleError, 'unresolved comparison'):
            resolve_arc_orders((parallel, parallel))

    def test_opposing_local_blocks_report_conflict(self):
        a = StrandVisit(1, LabeledRayVisit(
            1, ArcRayVisit('upper', 0, 2, 1)))
        b = StrandVisit(2, LabeledRayVisit(
            2, ArcRayVisit('upper', 0, 2, 1)))

        def terminal(owner, label, vertex):
            identifier = (owner, label)
            return TerminalVisit(owner, identifier, identifier, vertex)

        # On the left, side 2's cut block puts b before a. On the right,
        # side 0's block puts a before b in physical ray order.
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

    def test_comparison_budget_is_enforced_before_quadratic_work(self):
        arcs = chain_arcs(exact_action(product(initial_factors()[:1])))
        with self.assertRaisesRegex(NormalTriangleError, 'exceed max_pairs'):
            resolve_arc_orders(arcs, owners=(3, 6), max_pairs=1)

        # F1 has 36 possible same-edge pairs, but comparison sorting and
        # propagation need fewer memoized states to recover its full orders.
        self.assertEqual(resolve_arc_orders(arcs, owners=(3, 6), max_pairs=35),
                         resolve_arc_orders(arcs, owners=(3, 6)))

    def test_duplicate_terminal_vertex_has_no_invented_order(self):
        arcs = chain_arcs(exact_action(product(initial_factors()[:2])))
        # Two F2 arcs terminate at p5 on the same side of upper gap 4. Their
        # itinerary labels cannot choose an order at that common vertex.
        with self.assertRaisesRegex(NormalTriangleError,
                                    'terminal order is unresolved'):
            resolve_arc_orders(arcs, owners=(3, 4, 5, 6))


if __name__ == '__main__':
    unittest.main()
