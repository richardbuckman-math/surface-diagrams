import unittest

from surface_diagrams import GenusSurface, TypeIBoundary, BoundaryPair, Style, render_svg, render_tikz
from surface_diagrams.genus_diagrams import MarkedArc, NamedCut
from surface_diagrams.disk_routes import ItineraryError
from surface_diagrams.layout import layout


class BorderedMarkedArcTests(unittest.TestCase):
    def family(self, positions, **kwargs):
        return GenusSurface(2, type_i=(TypeIBoundary(6),),
                            marks=tuple(positions), **kwargs).with_reference_arcs(mark_positions=positions)

    def test_exact_endpoints_and_selection_in_all_views(self):
        positions={'P':(-35,30),'Q':(35,30),'R':(-35,-30),'S':(35,-30)}
        for v in ('above','below'):
            for h in ('left','right'):
                family=self.family(positions,view_vertical=v,view_horizontal=h)
                diagram=family.with_curves(MarkedArc('P','Q')).with_curves(MarkedArc('R','S'))
                drawing=layout(diagram.select(),Style())
                routes=[p for p in drawing.paths if p.role=='surface-route']
                self.assertEqual([p.commands for p in routes],[
                    (('M',-35,30),('L',35,30)),(('M',-35,-30),('L',35,-30))])
                self.assertTrue(all(not p.dashed for p in routes))
                self.assertEqual(sum(e.role=='marked-point' for e in drawing.ellipses),4)
                self.assertFalse(any(p.role in ('named-cut','mark-reference-spoke') for p in drawing.paths))
                self.assertEqual(family.curves,())
                self.assertIn('surface-route',render_svg(diagram))
                self.assertIn('surface-route',render_tikz(diagram))

    def test_mixed_type_ii_and_shared_endpoint(self):
        positions={'P':(-40,30),'Q':(0,30),'R':(40,30)}
        diagram=self.family(positions,type_ii=(BoundaryPair('left'),)).with_curves(
            MarkedArc('P','Q'),MarkedArc('Q','R'))
        self.assertEqual(sum(p.role=='surface-route' for p in layout(diagram,Style()).paths),2)

    def test_cross_band_and_intervening_mark_rejected(self):
        for positions,arc in [({'P':(-35,30),'Q':(35,-30)},MarkedArc('P','Q')),
                              ({'P':(-40,30),'Q':(0,30),'R':(40,30)},MarkedArc('P','R'))]:
            with self.assertRaises(ItineraryError): render_svg(self.family(positions).with_curves(arc))

    def test_crossing_and_overlap_rejected(self):
        family=self.family({'P':(-50,28),'Q':(50,36),'R':(-25,36),'S':(25,28)})
        with self.assertRaisesRegex(ItineraryError,'intersect'):
            render_svg(family.with_curves(MarkedArc('P','Q'),MarkedArc('R','S')))
        family=self.family({'P':(-35,30),'Q':(35,30)})
        with self.assertRaisesRegex(ItineraryError,'overlap'):
            render_svg(family.with_curves(MarkedArc('P','Q','a'),MarkedArc('Q','P','b')))

    def test_bad_inputs_rejected(self):
        family=self.family({'P':(-35,30),'Q':(35,30)})
        with self.assertRaises(TypeError): family.with_curves(NamedCut(2))
        with self.assertRaisesRegex(ValueError,'unknown'):
            render_svg(family.with_curves(MarkedArc('P','missing')))
        with self.assertRaisesRegex(ValueError,'distinct'):
            render_svg(family.with_curves(MarkedArc('P','Q'),MarkedArc('P','Q')))

    def test_reference_numbers_can_be_hidden_without_changing_geometry(self):
        family=self.family({'P':(-35,30),'Q':(35,30)}).with_curves(MarkedArc('P','Q'))
        for selected in (family, family.select(2,7), family.select()):
            original=layout(selected,Style())
            quiet=layout(selected.with_labels(reference=False),Style())
            self.assertEqual(quiet.paths,original.paths)
            self.assertEqual(quiet.ellipses,original.ellipses)
            self.assertEqual([label.text for label in quiet.texts],['P','Q'])
            self.assertEqual(layout(selected.with_labels(reference=False).with_labels(),Style()),original)
        with self.assertRaises(TypeError): family.with_labels(reference='no')

    def test_opt_in_crossings_preserve_straight_paths_in_all_views(self):
        for vertical in ('above','below'):
            for horizontal in ('left','right'):
                family=self.family({'P':(-50,28),'Q':(50,36),'R':(-25,36),'S':(25,28)},
                                   view_vertical=vertical,view_horizontal=horizontal)
                diagram=family.with_curves(MarkedArc('P','Q'),allow_intersections=True).with_curves(MarkedArc('R','S'))
                paths=[p for p in layout(diagram.select(),Style()).paths if p.role=='surface-route']
                self.assertEqual([p.commands for p in paths],[
                    (('M',-50,28),('L',50,36)),(('M',-25,36),('L',25,28))])
                self.assertIn('surface-route',render_tikz(diagram))
                with self.assertRaises(ItineraryError): render_svg(diagram.with_curves(allow_intersections=False))
        with self.assertRaises(TypeError): family.with_curves(allow_intersections='yes')

    def test_intersection_option_does_not_allow_overlap_or_intervening_marks(self):
        family=self.family({'P':(-35,30),'Q':(35,30)})
        with self.assertRaisesRegex(ItineraryError,'overlap'):
            render_svg(family.with_curves(MarkedArc('P','Q','a'),MarkedArc('Q','P','b'),allow_intersections=True))
        family=self.family({'P':(-40,30),'Q':(0,30),'R':(40,30)})
        with self.assertRaisesRegex(ItineraryError,'another mark'):
            render_svg(family.with_curves(MarkedArc('P','R'),allow_intersections=True))
