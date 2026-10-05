import unittest

from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.normal_strands import (
    ArcRayVisit, LabeledRayVisit, NormalTriangleError,
    arc_side_ray_visits, resolve_ray_order,
)


class RayOrderConstraintTests(unittest.TestCase):
    def test_documented_f1_upper_ray_three_order(self):
        arcs = chain_arcs(exact_action(product(initial_factors()[:1])))
        visits = tuple(LabeledRayVisit(owner, visit)
                       for owner, arc in enumerate(arcs, 1)
                       for visit in arc_side_ray_visits(arc, 'upper')
                       if visit.point == 3)
        by_id = {(visit.owner, visit.visit.segment): visit for visit in visits}
        self.assertEqual(set(by_id), {(3, 0), (3, 2), (6, 0), (6, 2)})

        # Supplied local precedence facts from HANDOFF, north toward point 3.
        # This test checks resolution; it does not derive the facts from F1.
        expected_ids = ((3, 0), (6, 2), (3, 2), (6, 0))
        precedences = tuple((by_id[first], by_id[second])
                            for first, second in zip(expected_ids, expected_ids[1:]))
        ordered = resolve_ray_order(tuple(reversed(visits)), precedences)
        self.assertEqual(tuple((visit.owner, visit.visit.segment)
                               for visit in ordered), expected_ids)

    def test_transitive_constraints_give_one_order(self):
        a, b, c = (LabeledRayVisit(owner, ArcRayVisit('upper', 0, 2, 1))
                   for owner in (4, 2, 5))
        self.assertEqual(resolve_ray_order((c, a, b),
                                           ((a, b), (b, c), (a, c), (a, b))),
                         (a, b, c))

    def test_missing_cross_arc_order_is_reported(self):
        a = LabeledRayVisit(3, ArcRayVisit('upper', 0, 3, 1))
        b = LabeledRayVisit(3, ArcRayVisit('upper', 2, 3, 1))
        c = LabeledRayVisit(6, ArcRayVisit('upper', 0, 3, -1))
        d = LabeledRayVisit(6, ArcRayVisit('upper', 2, 3, -1))
        with self.assertRaisesRegex(NormalTriangleError, 'unresolved ties'):
            resolve_ray_order((a, b, c, d), ((a, b), (d, c)))

    def test_cycle_and_invalid_events_are_rejected(self):
        a = LabeledRayVisit(3, ArcRayVisit('upper', 0, 3, 1))
        b = LabeledRayVisit(6, ArcRayVisit('upper', 2, 3, -1))
        with self.assertRaisesRegex(NormalTriangleError, 'cycle'):
            resolve_ray_order((a, b), ((a, b), (b, a)))
        with self.assertRaisesRegex(NormalTriangleError, 'unknown visit'):
            resolve_ray_order((a,), ((a, b),))
        with self.assertRaisesRegex(NormalTriangleError, 'different rays'):
            resolve_ray_order((a, LabeledRayVisit(6, ArcRayVisit('lower', 2, 3, -1))), ())
        with self.assertRaisesRegex(NormalTriangleError, 'repeats a visit'):
            resolve_ray_order((a, a), ())
        opposite_sign = LabeledRayVisit(3, ArcRayVisit('upper', 0, 3, -1))
        with self.assertRaisesRegex(NormalTriangleError, 'repeats a crossing ID'):
            resolve_ray_order((a, opposite_sign), ())


if __name__ == '__main__':
    unittest.main()
