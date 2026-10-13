import unittest
from collections import Counter
import re
from types import SimpleNamespace
from unittest.mock import patch
from xml.etree import ElementTree as ET

from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.curves import Arc
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.normal_cut_engine import calculate_cut_system
from surface_diagrams.normal_cut_preview import (
    _FanLayout, _StripLayout, _chain_endpoint_directions, render_normal_cut_preview,
)
from surface_diagrams.normal_gluing import TerminalVisit
from surface_diagrams.visuals import RAINBOW


class NormalCutPreviewTests(unittest.TestCase):
    def test_smooth_chain_endpoints_remain_opposite_after_permutation(self):
        # Both other endpoints lie to the right of point 1, so choosing
        # tangents from screen x alone would make these arcs leave together.
        chain = SimpleNamespace(arcs=(Arc(3, 1), Arc(1, 2)), owners=(1, 2))
        directions = _chain_endpoint_directions(chain)
        self.assertEqual(directions[1][1], directions[2][0])
        self.assertEqual(directions[1], (1.0, 1.0))

    @staticmethod
    def _certificate(prefix, *, owners=None):
        images = exact_action(product(initial_factors()[:prefix]))
        return calculate_cut_system(chain_arcs(images), owners=owners)

    def _assert_svg_matches_certificate(self, certificate, *, projection='strip'):
        with patch('surface_diagrams.curves.route', side_effect=AssertionError('old route called')):
            svg = render_normal_cut_preview(certificate, projection=projection)
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
        boundary = root.find("{http://www.w3.org/2000/svg}*[@class='outer-boundary']")
        self.assertIsNotNone(boundary)
        self.assertEqual(boundary.tag.split('}')[-1],
                         'rect' if projection == 'strip' else 'ellipse')
        if projection == 'strip':
            self.assertGreater(float(boundary.attrib['rx']), 0)
            self.assertEqual(float(boundary.attrib['x']), 13.0)
        self.assertEqual(len(root.findall('{http://www.w3.org/2000/svg}circle')),
                         certificate.points)
        labels = root.findall("{http://www.w3.org/2000/svg}text[@class='marked-point-label']")
        self.assertEqual(tuple(label.text for label in labels),
                         tuple(str(point) for point in range(1, certificate.points + 1)))
        paths = root.findall("{http://www.w3.org/2000/svg}path[@class='arc']")
        self.assertEqual(len(paths), len(certificate.owners))
        connections = Counter(connection.owner for connection in certificate.connections)
        for path in paths:
            owner = int(path.attrib['data-owner'])
            self.assertIn(owner, certificate.owners)
            self.assertEqual(path.attrib['stroke'], RAINBOW[owner - 1])
            commands = path.attrib['d'].split()
            self.assertEqual(commands[0], 'M')
            self.assertEqual(commands.count('M'), 1)
            self.assertEqual(commands.count('L') + commands.count('Q'),
                             connections[owner])
            self.assertNotIn('nan', path.attrib['d'].lower())
            self.assertNotIn('inf', path.attrib['d'].lower())
        layout = (_StripLayout(certificate) if projection == 'strip'
                  else _FanLayout(certificate))
        self.assertEqual(len(layout.crossings),
                         sum(map(len, certificate.ray_orders.values())) +
                         sum(map(len, certificate.cut_orders.values())))
        return svg

    def test_small_prefixes_draw_six_route_free_colored_paths(self):
        for prefix in (1, 2):
            with self.subTest(prefix=prefix):
                certificate = self._certificate(prefix)
                self.assertEqual(len(certificate.triangles), 14)
                svg = self._assert_svg_matches_certificate(certificate)
                # Standard chain edges and puncture terminal strands leave
                # triangle edges through shallow interior bends.
                self.assertIn(' Q ', svg)

    def test_reversed_owner_input_keeps_each_f2_path_geometry(self):
        forward = self._certificate(2)
        reverse = self._certificate(2, owners=(6, 5, 4, 3, 2, 1))
        def paths(certificate):
            root = ET.fromstring(render_normal_cut_preview(certificate))
            return {path.attrib['data-owner']: path.attrib['d']
                    for path in root.findall("{http://www.w3.org/2000/svg}path[@class='arc']")}
        self.assertEqual(paths(forward), paths(reverse))

    def test_f11_full_certificate_has_six_complete_preview_paths(self):
        certificate = self._certificate(11)
        self.assertEqual(len(certificate.triangles), 14)
        self._assert_svg_matches_certificate(certificate)

    def test_strip_cells_preserve_all_side_orders_and_stay_inside_disk(self):
        for prefix in (1, 11):
            with self.subTest(prefix=prefix):
                certificate = self._certificate(prefix)
                layout = _StripLayout(certificate)
                for triangle in certificate.triangles:
                    side, gap = triangle.triangle_id
                    corners = layout._cell_vertices(triangle)
                    self.assertEqual(len(corners), 4)
                    self.assertEqual(corners[0][1], corners[3][1])
                    self.assertEqual(corners[1][1], corners[2][1])
                    self.assertEqual(corners[0][0], corners[1][0])
                    self.assertEqual(corners[2][0], corners[3][0])
                    self.assertEqual(corners[1][1], 0)
                    self.assertEqual(corners[0][1] > 0, side == 'upper')
                    self.assertEqual(abs(corners[0][0] - corners[2][0]),
                                     layout.spacing)
                    for side_index, edge in enumerate(triangle.sides):
                        start, end = corners[side_index:side_index + 2]
                        physical = [visit for visit in edge.visits
                                    if not isinstance(visit, TerminalVisit)]
                        for position, visit in enumerate(physical, 1):
                            coordinate = layout.coordinate(visit)
                            fraction = position / (len(physical) + 1)
                            self.assertAlmostEqual(coordinate[0],
                                start[0] + fraction * (end[0] - start[0]))
                            self.assertAlmostEqual(coordinate[1],
                                start[1] + fraction * (end[1] - start[1]))
                for crossing in layout.crossings.values():
                    self.assertLess(abs(crossing[0]), layout.width / 2)
                    self.assertLess(abs(crossing[1]), layout.height / 2)
                triangles = {triangle.triangle_id: triangle
                             for triangle in certificate.triangles}
                for connection in certificate.connections:
                    side, gap = connection.triangle_id
                    corners = layout._cell_vertices(triangles[side, gap])
                    left, right = sorted((corners[0][0], corners[2][0]))
                    low, high = sorted((corners[0][1], corners[1][1]))
                    for point in (layout.coordinate(connection.first),
                                  layout.coordinate(connection.second)):
                        self.assertLessEqual(left, point[0])
                        self.assertLessEqual(point[0], right)
                        self.assertLessEqual(low, point[1])
                        self.assertLessEqual(point[1], high)
                    command = layout.chord(connection)
                    if command[0] == 'Q':
                        self.assertLess(left, command[1])
                        self.assertLess(command[1], right)
                        self.assertLess(low, command[2])
                        self.assertLess(command[2], high)

    def test_legacy_fan_projection_remains_available(self):
        certificate = self._certificate(1)
        self._assert_svg_matches_certificate(certificate, projection='fan')
        self.assertEqual(render_normal_cut_preview(certificate),
                         render_normal_cut_preview(certificate, projection='strip'))
        with self.assertRaisesRegex(ValueError, 'projection'):
            render_normal_cut_preview(certificate, projection='unknown')

    def test_smooth_view_keeps_certified_crossings_and_opposite_point_tangents(self):
        certificate = self._certificate(1)
        layout = _StripLayout(certificate)
        root = ET.fromstring(render_normal_cut_preview(certificate, projection='smooth'))
        self.assertEqual(len(root.findall(".//{http://www.w3.org/2000/svg}path[@class='vertical-ray']")), 6)
        paths = root.findall("{http://www.w3.org/2000/svg}path[@class='arc']")
        self.assertEqual(len(paths), 6)
        height = float(root.attrib['viewBox'].split()[3])
        width = float(root.attrib['viewBox'].split()[2])
        for path in paths:
            tokens = path.attrib['d'].split()
            self.assertEqual(tokens[0], 'M')
            self.assertTrue(tokens.count('C'))
            self.assertNotIn('L', tokens)
            self.assertNotIn('Q', tokens)
            first = tokens.index('C')
            last = len(tokens) - 7
            self.assertEqual(tokens[last], 'C')
            self.assertAlmostEqual(float(tokens[2]), float(tokens[first + 2]))
            self.assertAlmostEqual(float(tokens[last + 4]), float(tokens[last + 6]))
            owner = int(path.attrib['data-owner'])
            coordinates = {(float(tokens[index + 5]), float(tokens[index + 6]))
                           for index, token in enumerate(tokens) if token == 'C'}
            for visit, coordinate in layout.crossings.items():
                if visit.owner != owner:
                    continue
                expected = (round(width / 2 + coordinate[0], 6),
                            round(height / 2 - coordinate[1], 6))
                self.assertIn(expected, coordinates)

    def test_vertical_mirror_changes_only_display_coordinates(self):
        certificate = self._certificate(1)
        standard = ET.fromstring(render_normal_cut_preview(certificate))
        mirrored = ET.fromstring(render_normal_cut_preview(certificate, mirror_vertical=True))
        view_height = float(standard.attrib['viewBox'].split()[3])
        tag = "{http://www.w3.org/2000/svg}path[@class='arc']"
        regular_paths = standard.findall(tag)
        mirror_paths = mirrored.findall(tag)
        self.assertEqual(len(regular_paths), len(mirror_paths))
        for regular, flipped in zip(regular_paths, mirror_paths):
            self.assertEqual(regular.attrib['data-owner'], flipped.attrib['data-owner'])
            self.assertEqual(regular.attrib['stroke'], flipped.attrib['stroke'])
            a = [float(value) for value in re.findall(r'-?\d+(?:\.\d+)?', regular.attrib['d'])]
            b = [float(value) for value in re.findall(r'-?\d+(?:\.\d+)?', flipped.attrib['d'])]
            self.assertEqual(len(a), len(b))
            for index, (x, y) in enumerate(zip(a, b)):
                if index % 2 == 0:
                    self.assertAlmostEqual(x, y)
                else:
                    self.assertAlmostEqual(x + y, view_height)
        self.assertEqual([circle.attrib for circle in
                          standard.findall('{http://www.w3.org/2000/svg}circle')],
                         [circle.attrib for circle in
                          mirrored.findall('{http://www.w3.org/2000/svg}circle')])
        with self.assertRaisesRegex(TypeError, 'boolean'):
            render_normal_cut_preview(certificate, mirror_vertical='yes')


if __name__ == '__main__':
    unittest.main()
