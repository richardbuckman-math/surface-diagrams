import unittest
from dataclasses import replace
from xml.etree import ElementTree as ET

from surface_diagrams import (Arc, Loop, PlanarSurface, Style, ColoredCurve,
    PlanarDiagram, Figure, Panel, BraidDiagram, RAINBOW, RoutingError, render_svg, render_tikz)
from surface_diagrams.layout import layout


class VisualsTest(unittest.TestCase):
    def test_crossing_highlights_follow_word_positions_without_changing_braid(self):
        for direction in ('top-to-bottom','bottom-to-top'):
            for crossing_style in ('straight','smooth'):
                plain=BraidDiagram(3,(1,-2,-1),direction=direction,crossing_style=crossing_style)
                marked=replace(plain,highlight_crossings=(1,3))
                a,b=layout(plain,Style()),layout(marked,Style())
                self.assertEqual(a.paths,b.paths[2:])
                self.assertEqual(a.texts,b.texts)
                centers=[sum(c[2] for c in p.commands[:4])/4 for p in b.paths[:2]]
                self.assertEqual(centers[0]<centers[1],direction=='bottom-to-top')
                self.assertIn('braid-highlight',render_svg(marked))
                self.assertIn('braid-highlight',render_tikz(marked))
        for positions in ((0,),(4,),(True,),(1,1)):
            with self.assertRaises(ValueError):
                BraidDiagram(3,(1,-2,-1),highlight_crossings=positions)

    def setUp(self):
        self.surface = PlanarSurface.row('PPPP', spacing=60, height=210, margin=65)

    def test_intersections_are_opt_in_and_colors_follow_ids(self):
        curves = (ColoredCurve('a', Arc(1,3), RAINBOW[0]),
                  ColoredCurve('b', Arc(2,4), RAINBOW[4]))
        with self.assertRaises(RoutingError):
            layout(PlanarDiagram(self.surface, curves), Style())
        d = layout(PlanarDiagram(self.surface, curves, allow_intersections=True), Style())
        self.assertEqual([p.stroke for p in d.paths], [RAINBOW[0], RAINBOW[4]])
        # Two overlapping upper semicircles have an actual transverse crossing;
        # overlay mode must retain both complete curves, not reconnect their ends.
        self.assertEqual([p.commands[0][1] for p in d.paths], [-90, -30])
        self.assertEqual([p.commands[-1][-2] for p in d.paths], [30, 90])
        with self.assertRaises(RoutingError):
            render_svg(PlanarDiagram(self.surface, (ColoredCurve('bad', Arc(0,3), '#f00'),), True))

    def test_disjoint_mode_keeps_joint_routing_and_rejects_duplicate_ids(self):
        curves = (ColoredCurve('a', Arc(1,2), '#f00'), ColoredCurve('b', Arc(3,4), '#00f'))
        self.assertEqual(len(layout(PlanarDiagram(self.surface, curves), Style()).paths), 2)
        with self.assertRaises(ValueError):
            PlanarDiagram(self.surface, (curves[0], curves[0]))

    def test_legends_preserve_curve_identity_geometry_and_export(self):
        curves = (ColoredCurve('reference <a>', Arc(1,3), RAINBOW[0]),
                  ColoredCurve('image & b', Arc(2,4), RAINBOW[4]))
        plain = PlanarDiagram(self.surface, curves, True)
        original = layout(plain, Style())
        d = layout(replace(plain, show_legend=True), Style())
        self.assertEqual([(t.text,t.color) for t in d.texts], [(c.id,c.color) for c in curves])
        self.assertGreater(d.height, original.height)
        paths = [p for p in d.paths if p.role == 'arc']
        for before, after in zip(original.paths, paths):
            self.assertEqual(before.commands[0][1], after.commands[0][1])
            self.assertEqual(before.commands[1][1:6], after.commands[1][1:6])
        self.assertEqual(len([p for p in d.paths if p.role == 'curve-legend']), 2)
        reverse = layout(replace(plain, curves=curves[::-1], show_legend=True), Style())
        self.assertEqual([(t.text,t.color) for t in reverse.texts], [(c.id,c.color) for c in curves[::-1]])
        root = ET.fromstring(render_svg(replace(plain, show_legend=True)))
        self.assertIn('reference <a>', [t.text for t in root.iter()])
        self.assertIn('curve-legend', render_tikz(replace(plain, show_legend=True)))
        self.assertEqual(layout(PlanarDiagram(self.surface, show_legend=True), Style()),
                         layout(PlanarDiagram(self.surface), Style()))
        with self.assertRaises(ValueError):
            PlanarDiagram(self.surface, show_legend='yes')

    def test_braid_sign_changes_underpass_and_strand_transport(self):
        for word, under in (((1,), 1), ((-1,), 0)):
            d = layout(BraidDiagram(3, word), Style())
            self.assertEqual([i for i,p in enumerate(d.paths) if sum(c[0]=='M' for c in p.commands)==2], [under])
            bottom = [t.text for t in d.texts if t.y < 0]
            self.assertEqual(bottom, ['2','1','3'])
        d = layout(BraidDiagram(3, (1,-1)), Style())
        self.assertEqual([t.text for t in d.texts if t.y < 0], ['1','2','3'])
        self.assertEqual([p.stroke for p in d.paths[3:]], [RAINBOW[1],RAINBOW[0],RAINBOW[2]])
        empty = layout(BraidDiagram(2), Style())
        self.assertTrue(all(len(p.commands)==2 for p in empty.paths))
        for word in ((0,), (3,), (True,)):
            with self.assertRaises(ValueError):
                BraidDiagram(3, word)

    def test_figure_translates_arcs_preserving_radii_and_aligns_columns(self):
        diagram = self.surface.with_curves(Loop((0,4)))
        figure = Figure(((Panel(diagram, 'first'), Panel(BraidDiagram(3,(1,)))),
                         (Panel(diagram, 'second'), Panel(BraidDiagram(3,(1,2,1))))))
        original = layout(diagram, Style()).paths[0]
        d = layout(figure, Style())
        loops = [p for p in d.paths if p.role=='closed-curve']
        self.assertEqual(len(loops), 2)
        self.assertEqual(loops[0].commands[1][1:6], original.commands[1][1:6])
        self.assertEqual(loops[0].commands[0][1], loops[1].commands[0][1])
        self.assertGreater(loops[0].commands[0][2], loops[1].commands[0][2])
        ET.fromstring(render_svg(figure))
        self.assertIn('braid-strand', render_tikz(figure))

    def test_generator_labels_follow_signed_word_without_changing_strands(self):
        from dataclasses import replace
        for direction in ('top-to-bottom','bottom-to-top'):
            for crossing_style in ('straight','smooth'):
                plain=BraidDiagram(12,(10,-2,1),direction=direction,crossing_style=crossing_style)
                labelled=replace(plain,show_generators=True)
                a,b=layout(plain,Style()),layout(labelled,Style())
                self.assertEqual(a.paths,b.paths)
                self.assertEqual(a.texts,b.texts[:len(a.texts)])
                labels=b.texts[len(a.texts):]
                self.assertEqual([t.text for t in labels],['s10','s2^-1','s1'])
                self.assertEqual(labels[0].y<labels[-1].y,direction=='bottom-to-top')
                self.assertTrue(all(t.x>11*plain.spacing/2 for t in labels))
                self.assertTrue(all(t.x+len(t.text)*3<b.width/2 for t in labels))
                self.assertIn('s2^-1',render_svg(labelled))
                self.assertIn('s10',render_tikz(labelled))
        self.assertEqual(layout(BraidDiagram(2),Style()),layout(BraidDiagram(2,show_generators=True),Style()))
        with self.assertRaises(TypeError): BraidDiagram(2,show_generators='yes')

    def test_smooth_braids_preserve_signs_endpoints_colors_and_exports(self):
        for direction in ('top-to-bottom', 'bottom-to-top'):
            for sign in (1, -1):
                plain = BraidDiagram(3, (sign, -sign, 2), direction=direction)
                smooth = replace(plain, crossing_style='smooth')
                a, b = layout(plain, Style()), layout(smooth, Style())
                self.assertEqual(a.texts, b.texts)
                for old, new in zip(a.paths, b.paths):
                    self.assertEqual(old.stroke, new.stroke)
                    self.assertEqual(old.commands[0], new.commands[0])
                    self.assertEqual(old.commands[-1][-2:], new.commands[-1][-2:])
                    self.assertEqual(sum(c[0]=='M' for c in old.commands),
                                     sum(c[0]=='M' for c in new.commands))
                    curves = [c for c in new.commands if c[0]=='C']
                    if curves:
                        self.assertEqual(curves[0][1], new.commands[0][1])
                        self.assertEqual(curves[-1][3], curves[-1][5])
                ET.fromstring(render_svg(smooth))
                self.assertIn('.. controls', render_tikz(smooth))
        self.assertEqual(layout(BraidDiagram(3), Style()),
                         layout(BraidDiagram(3, crossing_style='smooth'), Style()))
        with self.assertRaises(ValueError):
            BraidDiagram(3, crossing_style='unknown')

    def test_circle_panels_clip_in_both_exports(self):
        circle = PlanarSurface.row('BP', spacing=60, height=140, margin=60).with_curves(Arc(1,2))
        figure = Figure(((Panel(circle, 'boundary to point', Style(boundary_shape='circle')),),))
        root = ET.fromstring(render_svg(figure))
        self.assertIsNotNone(root.find('.//{http://www.w3.org/2000/svg}clipPath'))
        self.assertIn(r"\pgfseteorule", render_tikz(figure))
        with self.assertRaises(ValueError):
            Panel(circle, style=Style(background='#fff'))


if __name__ == '__main__':
    unittest.main()
