import unittest
from surface_diagrams import GenusSurface, PlanarSurface, Style, MarkedArc, render_svg
from surface_diagrams.genus_diagrams import NamedCut
from surface_diagrams.genus_geometry import presentation
from surface_diagrams.genus_mesh import genus_binding
from surface_diagrams.layout import layout
from surface_diagrams.mesh_atlas import cubic_point, _near
from surface_diagrams.disk_routes import ItineraryError


class ReferenceAppearanceTests(unittest.TestCase):
    def test_default_is_above_and_planar_reference_follows_every_interval(self):
        self.assertEqual(GenusSurface().view_vertical,'above')
        surface=PlanarSurface.row('BPPB',spacing=65,height=180,margin=65)
        diagram=surface.with_cut_system()
        self.assertEqual([(c.curve.start,c.curve.end) for c in diagram.curves],
                         [(0,1),(1,2),(2,3),(3,4),(4,5)])
        paths=layout(diagram,Style(boundary_shape='circle')).paths
        self.assertEqual(len(paths),5)
        self.assertTrue(all([c[0] for c in p.commands]==['M','L'] for p in paths))
        self.assertTrue(all(c[2]==0 for p in paths for c in p.commands))
        self.assertEqual(len({p.stroke for p in paths}),5)
        self.assertFalse(PlanarSurface.row('').with_cut_system().curves)

    def test_tight_even_cuts_and_solid_default_in_both_views(self):
        for view,sign in (('above',1),('below',-1)):
            surface=GenusSurface(2,view_vertical=view)
            for number in (1,2,3,4,5):
                paths=[p for p in layout(surface.with_curves(NamedCut(number)),Style()).paths if p.role=='named-cut']
                self.assertEqual({p.dashed for p in paths},{False})
            curves=[p for p in layout(surface.with_curves(NamedCut(2)),Style()).paths if p.role=='named-cut']
            points=[c[1:] for p in curves for c in p.commands]
            hole= presentation(surface).handles[:2]
            hole_points=[]
            for c in hole:
                controls=(c[0][1:],c[1][1:3],c[1][3:5],c[1][5:7])
                hole_points.extend(cubic_point(controls,i/100) for i in range(101))
            self.assertLess(max(x for x,y in points)-max(x for x,y in hole_points),surface.handle_spacing*.05)
            self.assertLess(max(y for x,y in points)-max(y for x,y in hole_points),surface.handle_spacing*.08)

    def test_split_style_keeps_wraps_solid_and_preserves_walks_in_all_views(self):
        for vertical in ('above','below'):
            for horizontal in ('left','right'):
                surface=GenusSurface(2,view_vertical=vertical,view_horizontal=horizontal)
                solid=layout(surface.with_cut_system(),Style())
                diagram=surface.with_cut_system(closed_curve_style='split').with_curves(NamedCut(2))
                self.assertEqual(diagram.closed_curve_style,'split')
                split=layout(diagram,Style())
                self.assertEqual(solid.texts,split.texts)
                for color in {p.stroke for p in solid.paths if p.role=='named-cut'}:
                    a=[p for p in solid.paths if p.role=='named-cut' and p.stroke==color]
                    b=[p for p in split.paths if p.role=='named-cut' and p.stroke==color]
                    # Path breaks may change, but every directed segment stays.
                    def segments(paths):
                        return [(u[-2:],v[-2:]) for p in paths for u,v in zip(p.commands,p.commands[1:])]
                    self.assertEqual(segments(a),segments(b))
                wraps=layout(surface.with_curves(NamedCut(2),closed_curve_style='split'),Style())
                self.assertFalse(any(p.dashed for p in wraps.paths if p.role=='named-cut'))
                self.assertEqual(sum(p.dashed for p in split.paths if p.role=='named-cut'),3)
        with self.assertRaises(ValueError): GenusSurface().with_cut_system(closed_curve_style='bad')

    def test_style_does_not_change_explicit_disk_routes(self):
        from surface_diagrams.disk_routes import DiskRoute, Crossing
        route=DiskRoute((Crossing('front.3.0.0.s0',.23),Crossing('front.126.2.1.s0',.63)),id='long')
        surface=GenusSurface(2)
        a=layout(surface.with_curves(route),Style())
        b=layout(surface.with_curves(route,closed_curve_style='split'),Style())
        self.assertEqual(a,b)
        self.assertTrue(any(p.dashed for p in a.paths if p.role=='surface-route'))

    def test_straight_marked_arc_uses_actual_endpoints_and_rejects_obstacles(self):
        surface=GenusSurface(2,marks=('P','Q'))
        drawing=layout(surface.with_curves(MarkedArc('P','Q')),Style())
        path=next(p for p in drawing.paths if p.role=='surface-route')
        self.assertEqual([c[0] for c in path.commands],['M','L'])
        marks=[(m.x,m.y) for m in drawing.ellipses if m.role=='marked-point']
        self.assertTrue(_near(path.commands[0][1:],marks[0]))
        self.assertTrue(_near(path.commands[-1][1:],marks[1]))
        with self.assertRaises(ValueError):
            render_svg(surface.with_curves(MarkedArc('P','missing')))
        with self.assertRaises(ItineraryError):
            render_svg(surface.with_curves(MarkedArc('P','Q'),MarkedArc('Q','P')))
        three=GenusSurface(2,marks=('P','Q','R'))
        with self.assertRaises(ItineraryError):
            render_svg(three.with_curves(MarkedArc('P','R')))
        self.assertIn('surface-route',render_svg(three.with_curves(MarkedArc('P','Q'),MarkedArc('Q','R'))))


if __name__=='__main__': unittest.main()
