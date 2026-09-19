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
