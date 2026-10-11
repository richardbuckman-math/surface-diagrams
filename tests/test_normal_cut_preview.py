import unittest
from collections import Counter
from unittest.mock import patch
from xml.etree import ElementTree as ET

from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.normal_cut_engine import calculate_cut_system
from surface_diagrams.normal_cut_preview import _FanLayout, render_normal_cut_preview
from surface_diagrams.visuals import RAINBOW


class NormalCutPreviewTests(unittest.TestCase):
    @staticmethod
    def _certificate(prefix, *, owners=None):
        images = exact_action(product(initial_factors()[:prefix]))
        return calculate_cut_system(chain_arcs(images), owners=owners)

    def _assert_svg_matches_certificate(self, certificate):
        with patch('surface_diagrams.curves.route', side_effect=AssertionError('old route called')):
            svg = render_normal_cut_preview(certificate)
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
        self.assertEqual(len(root.findall('{http://www.w3.org/2000/svg}ellipse')), 1)
        self.assertEqual(len(root.findall('{http://www.w3.org/2000/svg}circle')),
                         certificate.points)
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
        layout = _FanLayout(certificate)
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


if __name__ == '__main__':
    unittest.main()
