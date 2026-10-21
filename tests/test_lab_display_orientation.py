"""A drawing mirror must never change the encoded mapping class or braid."""

import re
import unittest
from xml.etree import ElementTree as ET

from surface_diagrams import Arc, PlanarSurface, Style, render_svg
from surface_diagrams.based_cut_system import based_arc_drawing
from surface_diagrams.boundary_playground_geometry import support_svg as boundary_support_svg
from surface_diagrams.boundary_playground import new_project
from surface_diagrams.chain_cut_system import chain_arc_drawing, chain_cut_system_drawing
from surface_diagrams.factorization_explorer import Factor, initial_factors, product
from surface_diagrams.factorization_geometry import support_svg as six_support_svg
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.sphere_cut_system import sphere_chart_drawing
from surface_diagrams.visuals import ColoredCurve, PlanarDiagram


SVG = '{http://www.w3.org/2000/svg}'


class LabDisplayOrientationTests(unittest.TestCase):
    def _route(self, svg, role):
        root = ET.fromstring(svg)
        # Frame-free support thumbnails normalize their trimmed viewport with
        # an enclosing translation. The routed path and mirror stay intact.
        route = root.find(f".//{SVG}path[@class='{role}']")
        self.assertIsNotNone(route)
        return root, route

    def test_mirror_axis_follows_marked_points_even_when_legend_adds_height(self):
        surface = PlanarSurface.row('PPP', spacing=82, height=260, margin=80)
        diagram = PlanarDiagram(surface, (ColoredCurve('e1', Arc(0, 1, (2,),
                                                               direction='up'), '#c02648'),),
                                show_legend=True)
        style = Style(curve_width=2.4)
        old, original = self._route(render_svg(diagram, style=style), 'arc')
        mirrored, route = self._route(render_svg(
            diagram, style=style, mirror_curve_paths_vertical=True), 'arc')
        marks = mirrored.findall(f"{SVG}circle[@class='marked-point']")
        self.assertEqual(len(marks), 3)
        mark_y = float(marks[0].attrib['cy'])
        shift = float(re.search(r'translate\(0 ([^)]*)\)', route.attrib['transform']).group(1))
        self.assertAlmostEqual(shift, 2 * mark_y)
        self.assertEqual(route.attrib['d'], original.attrib['d'])
        self.assertEqual([mark.attrib for mark in marks],
                         [mark.attrib for mark in old.findall(
                             f"{SVG}circle[@class='marked-point']")])
        self.assertIsNone(mirrored.find(f"{SVG}path[@class='curve-legend']").get('transform'))

    def test_pairwise_arc_and_boundary_loop_use_same_display_mirror(self):
        project = new_project(3)
        factors = (project.split(0, 'lantern').factors[1], project.factors[0],
                   Factor('a', (2,), 1, 2, half=True))
        for factor in factors:
            role = 'arc' if factor.half else 'closed-curve'
            with self.subTest(factor=factor.id):
                original, path = self._route(boundary_support_svg(factor, 3), role)
                reflected, mirrored_path = self._route(boundary_support_svg(
                    factor, 3, mirror_vertical=True), role)
                self.assertEqual(mirrored_path.attrib['d'], path.attrib['d'])
                self.assertIn('scale(1 -1)', mirrored_path.attrib['transform'])
                self.assertEqual([dot.attrib for dot in original.findall(f'{SVG}circle')],
                                 [dot.attrib for dot in reflected.findall(f'{SVG}circle')])

    def test_six_point_support_and_transported_chain_arc_can_flip_independently(self):
        factor = initial_factors()[8]
        _, regular = self._route(six_support_svg(factor), 'arc')
        _, mirror = self._route(six_support_svg(factor, mirror_vertical=True), 'arc')
        self.assertEqual(regular.attrib['d'], mirror.attrib['d'])
        self.assertIn('scale(1 -1)', mirror.attrib['transform'])

        images = exact_action(product(initial_factors()[:1]))
        normal = ET.fromstring(chain_cut_system_drawing(images))
        flipped = ET.fromstring(chain_cut_system_drawing(images, mirror_vertical=True))
        regular_arcs = normal.findall(f"{SVG}path[@class='arc']")
        mirror_arcs = flipped.findall(f"{SVG}path[@class='arc']")
        self.assertEqual(len(regular_arcs), 6)
        self.assertEqual([path.attrib['d'] for path in regular_arcs],
                         [path.attrib['d'] for path in mirror_arcs])
        self.assertTrue(all('scale(1 -1)' in path.attrib['transform']
                            for path in mirror_arcs))
        one = ET.fromstring(chain_arc_drawing(images, index=2, mirror_vertical=True))
        self.assertEqual(len(one.findall(f"{SVG}path[@class='arc']")), 1)

    def test_mirror_option_requires_a_boolean(self):
        with self.assertRaises(TypeError):
            render_svg(PlanarSurface.row('PPP'), mirror_curve_paths_vertical='yes')

    def test_based_arc_and_five_point_sphere_chart_use_the_same_mirror(self):
        based = ET.fromstring(based_arc_drawing((1,), mirror_vertical=True))
        self.assertIn('scale(1 -1)', based.find(f"{SVG}path[@class='arc']").attrib['transform'])
        sphere, whisker = sphere_chart_drawing((), mirror_vertical=True)
        self.assertEqual(whisker, ())
        chart = ET.fromstring(sphere)
        self.assertEqual(len(chart.findall(f"{SVG}path[@class='arc']")), 5)
        self.assertTrue(all('scale(1 -1)' in path.attrib['transform']
                            for path in chart.findall(f"{SVG}path[@class='arc']")))


if __name__ == '__main__':
    unittest.main()
