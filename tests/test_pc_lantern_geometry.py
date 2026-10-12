"""Presentation geometry for the three PC lantern cut-chain edges."""

import unittest
from xml.etree import ElementTree

from surface_diagrams.pc_lantern_lab import (
    ARC_COLORS, STYLE, SURFACE, PCLanternLab, _PCCutDiagram,
    _shape_pc_arc, chain_arcs, cut_system_svg,
)
from surface_diagrams.visuals import ColoredCurve


def _oval(svg):
    root = ElementTree.fromstring(svg)
    return next(item for item in root if item.attrib.get('class') == 'outer-boundary')


def _end_tangent(commands):
    last = commands[-1]
    if last[0] == 'C':
        return (last[-2] - last[-4], last[-1] - last[-3])
    previous = commands[-2]
    return (last[-2] - previous[-2], last[-1] - previous[-1])


class PCLanternGeometryTests(unittest.TestCase):
    def test_disk_and_support_outlines_are_oval(self):
        lab = PCLanternLab()
        cut = _oval(cut_system_svg(()))
        self.assertGreater(float(cut.attrib['rx']) / float(cut.attrib['ry']), 1.7)
        for factor in lab.state()['factors']:
            support = _oval(factor['svg'])
            self.assertGreater(float(support.attrib['rx']) / float(support.attrib['ry']), 1.5)
            self.assertTrue(factor['svg_unmirrored'])

    def test_every_prefix_has_perpendicular_rim_stem_and_opposite_mark_ends(self):
        lab = PCLanternLab()
        for step in lab.state()['cut_steps']:
            arcs = chain_arcs(step['word'])
            diagram = _PCCutDiagram(SURFACE, tuple(
                ColoredCurve(str(index), arc, ARC_COLORS[index])
                for index, arc in enumerate(arcs)))
            paths = [p for p in diagram.drawing(STYLE).paths if p.role == 'arc']
            self.assertEqual(len(paths), 3)
            rim = paths[0].commands
            self.assertEqual(rim[0][1:], (-SURFACE.width / 2, 0))
            self.assertEqual(rim[1][0], 'L')
            self.assertGreater(rim[1][1], rim[0][1])
            self.assertEqual(rim[1][2], rim[0][2])
            for arc, path in zip(arcs, paths):
                commands = path.commands
                first = commands[0]
                next_command = commands[1]
                dx = next_command[1] - first[1]
                dy = next_command[2] - first[2]
                self.assertGreater(dx, 0)
                self.assertAlmostEqual(dy, 0)
                dx, dy = _end_tangent(commands)
                self.assertGreater(dx, 0)
                self.assertAlmostEqual(dy, 0)

    def test_reversed_straight_edge_has_opposite_incident_tangents(self):
        commands = _shape_pc_arc((('M', 10., 0.), ('L', -10., 0.)))
        self.assertEqual([command[0] for command in commands], ['M', 'C', 'L', 'C'])
        self.assertGreater(commands[1][1], commands[0][1])
        dx, dy = _end_tangent(commands)
        self.assertGreater(dx, 0)
        self.assertEqual(dy, 0)


if __name__ == '__main__':
    unittest.main()
