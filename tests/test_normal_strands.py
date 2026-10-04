import unittest

from surface_diagrams.normal_strands import (
    NormalTriangleError, StrandVisit, arc_gap_triangle_counts,
    arc_side_ray_counts, arc_side_ray_word,
    pair_triangle_sides, triangle_pair_counts,
)
from surface_diagrams.braid_actions import arc_ray_word
from surface_diagrams.based_cut_system import based_arc_ray_word
from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.curves import Arc
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action


class NormalTriangleTests(unittest.TestCase):
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
                for side in ('upper', 'lower'):
                    for gap in arc_gap_triangle_counts(arc, side=side):
                        with self.subTest(prefix=prefix, edge=edge,
                                          side=side, gap=gap.gap):
                            gap.formal_pair_counts()

    def test_auxiliary_rays_retain_both_sides_and_outer_endpoint(self):
        arc = Arc(1, 4, (3, 0, 5), direction='up')
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
