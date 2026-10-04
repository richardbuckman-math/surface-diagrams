import unittest

from surface_diagrams.normal_gluing import (
    ExpectedArc, NormalTriangle, TerminalVisit, TriangleSide, glue_triangles,
)
from surface_diagrams.normal_strands import NormalTriangleError, StrandVisit


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
