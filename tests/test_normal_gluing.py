import unittest

from surface_diagrams.normal_gluing import (
    ExpectedArc, NormalTriangle, TerminalVisit, TriangleSide, glue_triangles,
    inner_arc_triangles,
)
from surface_diagrams.normal_strands import (
    ArcRayVisit, LabeledCutVisit, LabeledRayVisit, NormalTriangleError,
    StrandVisit, joint_arc_cut_orders, joint_arc_ray_orders,
)
from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.curves import route
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.model import PlanarSurface, Style


def two_upper_gaps():
    """The two upper triangles crossed by the direct Arc(1, 3)."""
    start = TerminalVisit(0, -1, 'start', 'p1')
    end = TerminalVisit(0, -2, 'end', 'p3')
    crossing = StrandVisit(0, 1)
    first = NormalTriangle('upper-1', ('north', 'p1', 'p2'), (
        TriangleSide('ray-1', (start,)),
        TriangleSide('chain-1'),
        TriangleSide('ray-2', (crossing,)),
    ))
    second = NormalTriangle('upper-2', ('north', 'p2', 'p3'), (
        TriangleSide('ray-2', (crossing,)),
        TriangleSide('chain-2'),
        TriangleSide('ray-3', (end,)),
    ))
    return (first, second), ExpectedArc(0, start, end), crossing


class NormalGluingTests(unittest.TestCase):
    def test_f1_inner_triangles_round_trip_both_winding_itineraries(self):
        arcs = chain_arcs(exact_action(product(initial_factors()[:1])))
        surface = PlanarSurface.row('PPPPPP', spacing=50, height=220, margin=55)
        pieces = route(surface.with_curves(*arcs), Style())
        xs = (-surface.width / 2,) + tuple(point.x for point in surface.objects) + (
            surface.width / 2,)
        rays = joint_arc_ray_orders(arcs, pieces, xs)
        cuts = joint_arc_cut_orders(arcs, pieces, xs)

        # The other four F1 chain arcs coincide with triangulation edges.
        self.assertEqual(tuple(owner for owner, arc in enumerate(arcs, 1)
                               if arc.is_straight(6)), (1, 2, 4, 5))
        triangles, expected = inner_arc_triangles(arcs, rays, cuts, owners=(3, 6))
        self.assertEqual(len(triangles), 10)
        self.assertEqual({triangle.triangle_id for triangle in triangles},
                         {(side, gap) for side in ('upper', 'lower')
                          for gap in range(1, 6)})
        self.assertEqual(tuple((arc.owner, arc.start.vertex, arc.end.vertex)
                               for arc in expected),
                         ((3, 'p2', 'p3'), (6, 'p5', 'p6')))

        glued = glue_triangles(triangles, expected)
        self.assertEqual(tuple(path.owner for path in glued), (3, 6))
        for path in glued:
            arc = arcs[path.owner - 1]
            locations = ((2 * arc.start,) + tuple(2 * gap + 1 for gap in arc.cuts)
                         + (2 * arc.end,))
            itinerary = []
            for segment, (start, end) in enumerate(zip(locations, locations[1:])):
                side = 'upper' if (segment % 2 == 0) == arc.initial_up else 'lower'
                points = [point for point in range(1, 7)
                          if min(start, end) < 2 * point < max(start, end)]
                sign = 1 if start < end else -1
                for point in (points if sign > 0 else reversed(points)):
                    itinerary.append(LabeledRayVisit(
                        path.owner, ArcRayVisit(side, segment, point, sign)))
                if segment < len(arc.cuts):
                    itinerary.append(LabeledCutVisit(
                        path.owner, segment + 1, arc.cuts[segment]))
            self.assertEqual(tuple(visit.crossing for visit in path.crossings),
                             tuple(itinerary))
            self.assertEqual(len(itinerary), 14)

        with self.assertRaisesRegex(NormalTriangleError, 'edge-parallel'):
            inner_arc_triangles(arcs, rays, cuts, owners=(3,))

        # A different shared-ray order may not be silently reconnected into
        # another owner's arc when the local normal pairings are glued.
        swapped_rays = dict(rays)
        upper_three = list(swapped_rays['upper', 3])
        upper_three[0], upper_three[1] = upper_three[1], upper_three[0]
        swapped_rays['upper', 3] = tuple(upper_three)
        bad_triangles, expected = inner_arc_triangles(
            arcs, swapped_rays, cuts, owners=(3, 6))
        with self.assertRaises(NormalTriangleError):
            glue_triangles(bad_triangles, expected)

    def test_two_upper_triangles_join_the_direct_arc(self):
        triangles, expected, crossing = two_upper_gaps()
        paths = glue_triangles(triangles, (expected,))
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0].crossings, (crossing,))
        self.assertEqual((paths[0].start, paths[0].end),
                         (expected.start, expected.end))

    def test_reversed_shared_edge_order_is_rejected(self):
        starts = (TerminalVisit(0, -1, 'a-start', 'p1'),
                  TerminalVisit(1, -1, 'b-start', 'p1'))
        ends = (TerminalVisit(0, -2, 'a-end', 'p3'),
                TerminalVisit(1, -2, 'b-end', 'p3'))
        a, b = StrandVisit(0, 1), StrandVisit(1, 1)
        first = NormalTriangle('upper-1', ('north', 'p1', 'p2'), (
            TriangleSide('ray-1', starts), TriangleSide('chain-1'),
            TriangleSide('ray-2', (b, a)),
        ))
        second = NormalTriangle('upper-2', ('north', 'p2', 'p3'), (
            TriangleSide('ray-2', (a, b)), TriangleSide('chain-2'),
            TriangleSide('ray-3', (ends[1], ends[0])),
        ))
        declared = (ExpectedArc(0, starts[0], ends[0]),
                    ExpectedArc(1, starts[1], ends[1]))
        self.assertEqual(len(glue_triangles((first, second), declared)), 2)
        reversed_second = NormalTriangle('upper-2', second.vertices, (
            TriangleSide('ray-2', (b, a)), TriangleSide('chain-2'),
            TriangleSide('ray-3', (ends[0], ends[1])),
        ))
        with self.assertRaisesRegex(NormalTriangleError, 'order'):
            glue_triangles((first, reversed_second), declared)

    def test_shared_edge_must_have_opposite_boundary_directions(self):
        triangles, expected, crossing = two_upper_gaps()
        same_direction = NormalTriangle('upper-2', ('p2', 'north', 'p3'), (
            TriangleSide('ray-2', (crossing,)),
            TriangleSide('new-edge'),
            TriangleSide('ray-3', (expected.end,)),
        ))
        with self.assertRaisesRegex(NormalTriangleError, 'orientations'):
            glue_triangles((triangles[0], same_direction), (expected,))

    def test_owner_swap_and_missing_terminal_are_rejected(self):
        triangles, expected, _ = two_upper_gaps()
        wrong_owner = NormalTriangle('upper-2', triangles[1].vertices, (
            TriangleSide('ray-2', (StrandVisit(1, 1),)),
            *triangles[1].sides[1:],
        ))
        with self.assertRaises(NormalTriangleError):
            glue_triangles((triangles[0], wrong_owner), (expected,))

        missing = ExpectedArc(0, expected.start,
                              TerminalVisit(0, -3, 'other-end', 'p3'))
        with self.assertRaisesRegex(NormalTriangleError, 'terminal'):
            glue_triangles(triangles, (missing,))

    def test_extra_closed_component_is_rejected(self):
        triangles, expected, _ = two_upper_gaps()
        ab, bc, ca = StrandVisit(0, 10), StrandVisit(0, 11), StrandVisit(0, 12)
        cycle = (
            NormalTriangle('a', ('q0', 'q1', 'q2'), (
                TriangleSide('outer-a'), TriangleSide('ab', (ab,)),
                TriangleSide('ca', (ca,)),
            )),
            NormalTriangle('b', ('q2', 'q1', 'q3'), (
                TriangleSide('ab', (ab,)), TriangleSide('outer-b'),
                TriangleSide('bc', (bc,)),
            )),
            NormalTriangle('c', ('q0', 'q2', 'q3'), (
                TriangleSide('ca', (ca,)), TriangleSide('bc', (bc,)),
                TriangleSide('outer-c'),
            )),
        )
        with self.assertRaisesRegex(NormalTriangleError, 'cycle'):
            glue_triangles(triangles + cycle, (expected,))


if __name__ == '__main__':
    unittest.main()
