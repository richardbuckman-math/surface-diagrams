import unittest
from dataclasses import replace
from math import sqrt

from surface_diagrams.normal_strands import (
    ArcRayVisit, NormalTriangleError, StrandVisit, _reduce_ray_visits,
    arc_gap_triangle_counts, arc_side_ray_counts, arc_side_ray_visits,
    arc_side_ray_word,
    pair_triangle_sides, single_arc_ray_orders, triangle_pair_counts,
)
from surface_diagrams.braid_actions import arc_ray_word
from surface_diagrams.based_cut_system import based_arc_ray_word
from surface_diagrams.chain_cut_system import chain_arc, chain_arcs
from surface_diagrams.curves import Arc, route
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.model import PlanarSurface, Style


class NormalTriangleTests(unittest.TestCase):
    @staticmethod
    def _single_arc_layout(arc, *, spacing=36, height=80, margin=30):
        surface = PlanarSurface.row('PPPPPP', spacing=spacing,
                                    height=height, margin=margin)
        pieces = route(surface.with_curves(arc), Style())
        xs = (-surface.width / 2,) + tuple(point.x for point in surface.objects) + (surface.width / 2,)
        return pieces, xs

    def test_single_arc_layout_orders_surviving_visits_by_analytic_height(self):
        arc = Arc(1, 4, (3, 0, 5), direction='up')
        pieces, xs = self._single_arc_layout(arc)
        orders = single_arc_ray_orders(arc, pieces, xs)
        self.assertEqual(tuple(visit.crossing_id for visit in orders['upper', 2]),
                         ((0, 2), (2, 2)))
        self.assertEqual(tuple(visit.crossing_id for visit in orders['upper', 3]),
                         ((0, 3), (2, 3)))
        self.assertEqual(orders['lower', 4], ())
        for side in ('upper', 'lower'):
            self.assertEqual({visit.crossing_id for point in range(1, 7)
                              for visit in orders[side, point]},
                             {visit.crossing_id for visit in
                              arc_side_ray_visits(arc, side)})

    def test_single_arc_layout_rejects_tied_heights_and_wrong_itinerary(self):
        arc = Arc(1, 4, (3, 0, 5), direction='up')
        pieces, xs = self._single_arc_layout(arc)
        x = xs[2]
        def unscaled_height(piece):
            radius = abs(piece.end - piece.start) / 2
            return radius * sqrt(1 - ((x - (piece.start + piece.end) / 2) / radius) ** 2)
        tied_aspect = (pieces[0].aspect * unscaled_height(pieces[0])
                       / unscaled_height(pieces[2]))
        tied = pieces[:2] + (replace(pieces[2], aspect=tied_aspect),) + pieces[3:]
        with self.assertRaisesRegex(NormalTriangleError, 'indistinguishable heights'):
            single_arc_ray_orders(arc, tied, xs)
        wrong_side = pieces[:2] + (replace(pieces[2], up=False),) + pieces[3:]
        with self.assertRaisesRegex(NormalTriangleError, 'disagrees'):
            single_arc_ray_orders(arc, wrong_side, xs)
        with self.assertRaisesRegex(NormalTriangleError, 'outside its gap'):
            single_arc_ray_orders(arc, pieces,
                                  xs[:5] + (pieces[-1].start + 1,) + xs[6:])

    def test_one_f11_arc_layout_has_individual_ray_orders(self):
        images = exact_action(product(initial_factors()[:11]))
        arc = chain_arc(images, 3)
        pieces, xs = self._single_arc_layout(arc, spacing=500,
                                             height=2200, margin=550)
        orders = single_arc_ray_orders(arc, pieces, xs)
        self.assertEqual(sum(len(visits) for visits in orders.values()),
                         sum(len(arc_side_ray_visits(arc, side))
                             for side in ('upper', 'lower')))
        self.assertGreater(max(map(len, orders.values())), 1)

    def test_puncture_terminals_are_separate_vertex_slots(self):
        arc = Arc(1, 3, direction='up')
        upper = arc_gap_triangle_counts(arc, side='upper')
        lower = arc_gap_triangle_counts(arc, side='lower')
        with self.assertRaises(NormalTriangleError):
            triangle_pair_counts(upper[0].left_ray, upper[0].chain_cut,
                                 upper[0].right_ray)
        self.assertEqual((upper[0].left_ray, upper[0].chain_cut,
                          upper[0].right_ray, upper[0].left_terminal,
                          upper[0].right_terminal), (0, 0, 1, 1, 0))
        self.assertEqual(upper[0].formal_pair_counts(), (0, 0, 1))
        self.assertEqual(upper[1].formal_pair_counts(), (0, 0, 1))
        self.assertTrue(all(gap.formal_pair_counts() == (0, 0, 0)
                            for gap in lower))
        straight = arc_gap_triangle_counts(Arc(1, 2))
        self.assertEqual((straight[0].left_terminal,
                          straight[0].right_terminal), (1, 1))
        self.assertEqual(straight[0].formal_pair_counts(), (0, 0, 1))

    def test_moderate_itinerary_has_admissible_terminal_aware_counts(self):
        arc = Arc(1, 4, (3, 0, 5), direction='up')
        upper = arc_gap_triangle_counts(arc, side='upper')
        lower = arc_gap_triangle_counts(arc, side='lower')
        self.assertEqual((upper[0].left_ray, upper[0].chain_cut,
                          upper[0].right_ray, upper[0].left_terminal),
                         (1, 0, 2, 1))
        self.assertEqual((lower[3].left_ray, lower[3].chain_cut,
                          lower[3].right_ray, lower[3].left_terminal),
                         (0, 0, 1, 1))
        for gap in upper + lower:
            with self.subTest(side=gap.side, gap=gap.gap):
                gap.formal_pair_counts()

    def test_original_chain_prefixes_have_admissible_inner_triangles(self):
        factors = initial_factors()
        for prefix in range(13):
            arcs = chain_arcs(exact_action(product(factors[:prefix])))
            for edge, arc in enumerate(arcs, 1):
                all_ids = []
                for side in ('upper', 'lower'):
                    visits = arc_side_ray_visits(arc, side=side)
                    all_ids.extend(visit.crossing_id for visit in visits)
                    with self.subTest(prefix=prefix, edge=edge, side=side):
                        self.assertEqual(tuple(visit.letter for visit in visits),
                                         arc_side_ray_word(arc, side=side))
                        self.assertTrue(all(visit.side == side and
                                            visit.crossing_id == (visit.segment, visit.point)
                                            and visit.sign in (-1, 1)
                                            for visit in visits))
                        if side == 'upper':
                            expected = (based_arc_ray_word(arc) if arc.start == 0 else
                                        arc_ray_word(6, arc))
                            self.assertEqual(tuple(visit.letter for visit in visits),
                                             expected)
                    for gap in arc_gap_triangle_counts(arc, side=side):
                        with self.subTest(prefix=prefix, edge=edge,
                                          side=side, gap=gap.gap):
                            gap.formal_pair_counts()
                self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_ray_visit_reduction_retains_survivor_ids_across_segments(self):
        # A minimal Arc cannot repeat consecutive cuts, so build the event
        # stream directly to exercise cancellation across different segments.
        visits = (ArcRayVisit('upper', 0, 2, 1),
                  ArcRayVisit('upper', 0, 3, 1),
                  ArcRayVisit('upper', 2, 3, -1),
                  ArcRayVisit('upper', 2, 4, 1))
        reduced = _reduce_ray_visits(visits)
        self.assertEqual(reduced, (visits[0], visits[3]))
        self.assertEqual(tuple(visit.crossing_id for visit in reduced),
                         ((0, 2), (2, 4)))
        with self.assertRaises((AttributeError, TypeError)):
            reduced[0].point = 5

    def test_auxiliary_rays_retain_both_sides_and_outer_endpoint(self):
        arc = Arc(1, 4, (3, 0, 5), direction='up')
        self.assertEqual(tuple((visit.segment, visit.letter)
                               for visit in arc_side_ray_visits(arc, 'upper')),
                         ((0, 2), (0, 3), (2, 1), (2, 2), (2, 3),
                          (2, 4), (2, 5)))
        self.assertEqual(tuple((visit.segment, visit.letter)
                               for visit in arc_side_ray_visits(arc, 'lower')),
                         ((1, -3), (1, -2), (1, -1), (3, -5)))
        self.assertEqual(arc_side_ray_word(arc, side='upper'),
                         (2, 3, 1, 2, 3, 4, 5))
        self.assertEqual(arc_side_ray_word(arc, side='lower'),
                         (-3, -2, -1, -5))
        self.assertEqual(arc_side_ray_counts(arc, side='lower'),
                         (1, 1, 1, 0, 1, 0))
        based = Arc(0, 4, (3, 0), direction='down')
        self.assertEqual(arc_side_ray_word(based), based_arc_ray_word(based))
        self.assertEqual(arc_side_ray_word(arc), arc_ray_word(6, arc))

    def test_three_colored_corners_preserve_arc_owners(self):
        sides = (
            (StrandVisit(2, 0), StrandVisit(0, 1)),
            (StrandVisit(0, 2), StrandVisit(1, 3)),
            (StrandVisit(1, 4), StrandVisit(2, 5)),
        )
        strands = pair_triangle_sides(sides)
        self.assertEqual({strand.owner for strand in strands}, {0, 1, 2})
        used = {(side, slot) for strand in strands for side, slot in (
            (strand.first_side, strand.first_slot),
            (strand.second_side, strand.second_slot))}
        self.assertEqual(used, {(side, slot) for side in range(3) for slot in range(2)})

    def test_invalid_counts_and_owner_switch_are_rejected(self):
        for counts in ((1, 1, 1), (1, 1, 4), (-1, 2, 1)):
            with self.subTest(counts=counts), self.assertRaises(NormalTriangleError):
                triangle_pair_counts(*counts)
        with self.assertRaisesRegex(NormalTriangleError, 'different arcs'):
            pair_triangle_sides(((StrandVisit(0, 0),), (StrandVisit(1, 1),), ()))

    def test_dense_local_pairing_has_no_search_limit(self):
        count = 1600
        sides = tuple(tuple(StrandVisit(0, side * count + slot)
                            for slot in range(count)) for side in range(3))
        strands = pair_triangle_sides(sides)
        self.assertEqual(len(strands), 3 * count // 2)
        self.assertEqual(len({(strand.first_side, strand.first_slot)
                              for strand in strands}
                             | {(strand.second_side, strand.second_slot)
                                for strand in strands}), 3 * count)

    def test_small_admissible_patterns_have_no_interleaving_chords(self):
        for a in range(6):
            for b in range(6):
                for c in range(6):
                    try:
                        triangle_pair_counts(a, b, c)
                    except NormalTriangleError:
                        continue
                    counts = (a, b, c)
                    sides = tuple(tuple(StrandVisit(0, (side, slot))
                                        for slot in range(count))
                                  for side, count in enumerate(counts))
                    strands = pair_triangle_sides(sides)
                    offsets = (0, a, a + b)
                    chords = [tuple(sorted((offsets[s.first_side] + s.first_slot,
                                             offsets[s.second_side] + s.second_slot)))
                              for s in strands]
                    for i, (left, right) in enumerate(chords):
                        for other_left, other_right in chords[i + 1:]:
                            self.assertFalse(left < other_left < right < other_right
                                             or other_left < left < other_right < right,
                                             counts)


if __name__ == '__main__':
    unittest.main()
