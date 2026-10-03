import unittest

from surface_diagrams.normal_strands import (
    NormalTriangleError, StrandVisit, pair_triangle_sides, triangle_pair_counts,
)


class NormalTriangleTests(unittest.TestCase):
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
