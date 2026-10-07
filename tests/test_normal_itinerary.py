import unittest
from collections import Counter

from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.curves import Arc
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.normal_gluing import TerminalVisit
from surface_diagrams.normal_itinerary import arc_local_connections
from surface_diagrams.normal_strands import (
    LabeledCutVisit, LabeledRayVisit, StrandVisit, arc_gap_triangle_counts,
    arc_side_ray_visits,
)


class NormalItineraryTests(unittest.TestCase):
    def assert_exact_local_connections(self, arc, owner, *, points=6):
        connections = arc_local_connections(arc, points=points, owner=owner)
        self.assertTrue(connections)

        def terminal(role, point):
            boundary = point in (0, points + 1)
            key = (owner, role)
            return TerminalVisit(owner, key, key,
                                 f'{"b" if boundary else "p"}{point}',
                                 'boundary' if boundary else 'puncture')

        by_segment = {segment: [] for segment in range(len(arc.cuts) + 1)}
        for side in ('upper', 'lower'):
            for ray in arc_side_ray_visits(arc, side=side, points=points):
                by_segment[ray.segment].append(StrandVisit(
                    owner, LabeledRayVisit(owner, ray)))
        expected_events = [terminal('start', arc.start)]
        for segment in range(len(arc.cuts) + 1):
            expected_events.extend(by_segment[segment])
            if segment < len(arc.cuts):
                expected_events.append(StrandVisit(owner, LabeledCutVisit(
                    owner, segment + 1, arc.cuts[segment])))
        expected_events.append(terminal('end', arc.end))

        self.assertEqual(connections[0].first, expected_events[0])
        self.assertEqual(tuple(connection.second for connection in connections),
                         tuple(expected_events[1:]))
        self.assertTrue(all(left.second == right.first
                            for left, right in zip(connections, connections[1:])))

        incidence = Counter(event for connection in connections
                            for event in (connection.first, connection.second))
        self.assertEqual(set(incidence), set(expected_events))
        for event in expected_events:
            self.assertEqual(incidence[event],
                             1 if isinstance(event, TerminalVisit) else 2)

        possible_triangles = {(side, gap) for side in ('upper', 'lower')
                              for gap in range(points + 1)}
        for connection in connections:
            self.assertEqual(connection.owner, owner)
            self.assertIn(connection.triangle_id, possible_triangles)
            self.assertIn(connection.first_side, (0, 1, 2))
            self.assertIn(connection.second_side, (0, 1, 2))
            self.assertNotEqual(connection.first_side, connection.second_side)
            self.assertEqual((connection.first.owner, connection.second.owner),
                             (owner, owner))

        for side in ('upper', 'lower'):
            for gap in arc_gap_triangle_counts(
                    arc, points=points, side=side, include_outer=True):
                actual = Counter(tuple(sorted((connection.first_side,
                                               connection.second_side)))
                                 for connection in connections
                                 if connection.triangle_id == (side, gap.gap))
                left_cut, cut_right, right_left = gap.formal_pair_counts()
                if side == 'lower':
                    # Lower triangles run right ray, cut, left ray.
                    left_cut, cut_right = cut_right, left_cut
                self.assertEqual(
                    (actual[0, 1], actual[1, 2], actual[0, 2]),
                    (left_cut, cut_right, right_left),
                    (owner, side, gap.gap))
        return connections

    def test_boundary_to_puncture_arc_uses_outer_cap_and_labeled_ray(self):
        connections = self.assert_exact_local_connections(
            Arc(0, 2, direction='up'), 7)
        self.assertEqual(tuple(connection.triangle_id for connection in connections),
                         (('upper', 0), ('upper', 1)))
        self.assertEqual(connections[0].first.kind, 'boundary')
        self.assertEqual(connections[-1].second.kind, 'puncture')
        self.assertEqual(connections[0].second.crossing,
                         LabeledRayVisit(7, arc_side_ray_visits(
                             Arc(0, 2, direction='up'))[0]))

    def test_both_f1_winding_arcs_retain_all_local_connections(self):
        arcs = chain_arcs(exact_action(product(initial_factors()[:1])))
        for owner in (3, 6):
            with self.subTest(owner=owner):
                connections = self.assert_exact_local_connections(
                    arcs[owner - 1], owner)
                self.assertEqual(len(connections), 15)
                self.assertEqual(len({event.crossing for connection in connections
                                      for event in (connection.first,
                                                    connection.second)
                                      if not isinstance(event, TerminalVisit)}), 14)

    def test_f11_six_arcs_preserve_labeled_local_connections(self):
        arcs = chain_arcs(exact_action(product(initial_factors()[:11])))
        for owner, arc in enumerate(arcs, 1):
            with self.subTest(owner=owner):
                self.assert_exact_local_connections(arc, owner)


if __name__ == '__main__':
    unittest.main()
