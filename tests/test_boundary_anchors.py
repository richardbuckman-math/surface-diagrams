import unittest
from surface_diagrams import GenusSurface, TypeIBoundary, BoundaryPair, Style, render_svg, render_tikz
from surface_diagrams.genus_geometry import presentation
from surface_diagrams.layout import layout


class BoundaryAnchorTests(unittest.TestCase):
    def test_actual_rim_endpoints_and_identity_in_all_views(self):
        expected=None
        for vertical in ('above','below'):
            for horizontal in ('left','right'):
                surface=GenusSurface(2,type_i=(TypeIBoundary(2),TypeIBoundary(6)),
                    type_ii=(BoundaryPair('top'),),view_vertical=vertical,view_horizontal=horizontal)
                anchors=surface.boundary_anchors()
                self.assertEqual(len(anchors),8)
                ids=tuple(a.id for a in anchors)
                if expected is None: expected=ids
                self.assertEqual(ids,expected)
                for rim in presentation(surface).rims:
                    for bank,point in zip(('a','b'),rim.anchors):
                        anchor=surface.boundary_anchor(rim.id,bank)
                        self.assertEqual(anchor.point,point)
                        self.assertEqual(anchor.id,rim.id+':'+bank)
                        # Both drawn half-rims end at precisely these attachments.
                        for sign in (-1,1):
                            self.assertIn(point,(rim.half(sign)[0][1:],rim.half(sign)[-1][-2:]))
                d=layout(surface.boundary_guide(),Style())
                self.assertEqual(sum(e.role=='boundary-anchor' for e in d.ellipses),8)
                self.assertIn('boundary-anchor',render_svg(surface.boundary_guide()))
                self.assertIn('boundary-anchor',render_tikz(surface.boundary_guide()))
                with self.assertRaises(ValueError): surface.boundary_anchor('missing','a')
                with self.assertRaises(ValueError): surface.boundary_anchor('fixed-2','front')

    def test_no_false_mark_or_cut_binding(self):
        self.assertEqual(GenusSurface().boundary_anchors(),())
        surface=GenusSurface(2,type_ii=(BoundaryPair('left'),),marks=('P',))
        with self.assertRaises(NotImplementedError): render_svg(surface.boundary_guide())
        with self.assertRaises(NotImplementedError): surface.cut_system()

    def test_end_reference_arcs_meet_rims_and_cusps_in_all_views(self):
        for vertical in ('above','below'):
            for horizontal in ('left','right'):
                surface=GenusSurface(2,type_i=(TypeIBoundary(1),TypeIBoundary(6)),
                                    view_vertical=vertical,view_horizontal=horizontal)
                d=layout(surface.with_reference_arcs(),Style())
                arcs=[p for p in d.paths if p.role=='boundary-reference-arc']
                self.assertEqual(len(arcs),4)
                self.assertEqual(sum(p.dashed for p in arcs),2)
                endpoints={p.commands[0][1:] for p in arcs}|{p.commands[-1][-2:] for p in arcs}
                self.assertTrue({r.point(0,sign*r.depth) for r in presentation(surface).rims for sign in (-1,1)} <= endpoints)
                outline=presentation(surface)
                self.assertEqual(endpoints - {r.point(0,sign*r.depth) for r in presentation(surface).rims for sign in (-1,1)},
                    {outline.handles[1][0][1:],outline.handles[-1][-1][-2:]})
                self.assertIn('boundary-reference-arc',render_tikz(surface.with_reference_arcs()))
                with self.assertRaises(NotImplementedError): surface.cut_system()
        for surface in (GenusSurface(type_ii=(BoundaryPair('left'),BoundaryPair('left'))),):
            with self.assertRaises(NotImplementedError): render_svg(surface.with_reference_arcs())

    def test_all_type_i_slots_attach_and_opened_rims_stay_inside_wrap(self):
        from surface_diagrams.mesh_atlas import cubic_point
        from surface_diagrams.visuals import RAINBOW
        for view in ('above','below'):
            surface=GenusSurface(2,type_i=tuple(TypeIBoundary(i) for i in range(1,7)),view_vertical=view)
            drawing=layout(surface.with_reference_arcs(),Style())
            arcs=[p for p in drawing.paths if p.role=='boundary-reference-arc']
            self.assertEqual(len(arcs),6)
            ends={p.commands[0][1:] for p in arcs}|{p.commands[-1][-2:] for p in arcs}
            self.assertEqual(ends,{r.point(0,sign*r.depth) for r in presentation(surface).rims for sign in (-1,1)})
            for number in (2,4):
                wrap=[p for p in drawing.paths if p.role=='named-cut' and p.stroke==RAINBOW[number-1]]
                points=[cmd[-2:] for p in wrap for cmd in p.commands]
                for rim in presentation(surface).rims:
                    if rim.id not in (f'fixed-{number}',f'fixed-{number+1}'): continue
                    for sign in (-1,1):
                        commands=rim.half(sign)
                        start=commands[0][1:]
                        for command in commands[1:]:
                            curve=(start,command[1:3],command[3:5],command[5:7])
                            for i in range(31):
                                x,y=cubic_point(curve,i/30)
                                # Ray casting against the actual rounded wrap,
                                # not merely its bounding rectangle.
                                crossings=0
                                for a,b in zip(points,points[1:]+points[:1]):
                                    if (a[1]>y)!=(b[1]>y):
                                        hit=a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])
                                        crossings += hit>x
                                self.assertEqual(crossings%2,1)
                                self.assertLess(min(p[0] for p in points),x)
                                self.assertGreater(max(p[0] for p in points),x)
                                self.assertLess(min(p[1] for p in points),y)
                                self.assertGreater(max(p[1] for p in points),y)
                            start=command[-2:]

    def test_top_bottom_perimeter_arcs_end_only_at_rims(self):
        for view in ('above','below'):
            for bank in ('a','b'):
                surface=GenusSurface(2,type_i=(TypeIBoundary(2),),
                    type_ii=(BoundaryPair('top'),),view_vertical=view)
                d=layout(surface.with_reference_arcs(pair_bank=bank),Style())
                arcs=[p for p in d.paths if p.role=='boundary-reference-perimeter']
                self.assertEqual(len(arcs),2)
                anchors={p for r in presentation(surface).rims if r.role=='type-ii-boundary' for p in r.anchors}
                endpoints=[p.commands[i][-2:] for p in arcs for i in (0,-1)]
                self.assertEqual(set(endpoints),anchors)
                self.assertEqual(len(endpoints),len(anchors))
                self.assertFalse(any('spoke' in p.role for p in d.paths))
                self.assertIn('boundary-reference-perimeter',render_tikz(surface.with_reference_arcs()))
        with self.assertRaises(ValueError):
            render_svg(GenusSurface().with_reference_arcs(pair_bank='front'))

    def test_vertical_cubic_hit_is_not_a_sampled_approximation(self):
        from surface_diagrams.genus_diagrams import _vertical_hits
        commands=(('M',0.,0.),('C',1.,1.,2.,1.,3.,0.))
        hit,=tuple(_vertical_hits(commands,1.5))
        self.assertAlmostEqual(hit[0],1.5,places=12)
        self.assertAlmostEqual(hit[1],.75,places=12)

    def test_side_pair_connection_is_continuous_across_axis(self):
        for side in ('left','right'):
            for view in ('above','below'):
                surface=GenusSurface(2,type_ii=(BoundaryPair(side),),view_vertical=view)
                d=layout(surface.with_reference_arcs(),Style())
                anchors={surface.boundary_anchor(f'pair-1-{sign}','a').point for sign in ('upper','lower')}
                arcs=[p for p in d.paths if p.role=='boundary-reference-perimeter']
                inner=[p for p in arcs if {p.commands[0][1:],p.commands[-1][-2:]}==anchors]
                self.assertEqual(len(inner),1)
                self.assertTrue(any(abs(c[-1])<1e-8 for c in inner[0].commands[1:-1]))
                self.assertEqual(len(arcs),2)

    def test_reference_presentation_does_not_require_closed_mesh(self):
        from unittest.mock import patch
        surface=GenusSurface(2,type_ii=(BoundaryPair('left'),))
        with patch('surface_diagrams.genus_diagrams.genus_binding',side_effect=AssertionError('mesh requested')):
            self.assertIn('boundary-reference-perimeter',render_svg(surface.with_reference_arcs()))

    def test_marks_split_perimeter_and_preserve_explicit_coordinates(self):
        surface=GenusSurface(2,type_i=(TypeIBoundary(6),),marks=('P','Q'))
        positions={'Q':(35.,-30.),'P':(-35.,30.)}
        d=layout(surface.with_reference_arcs(mark_positions=positions),Style())
        marks=[e for e in d.ellipses if e.role=='marked-point']
        self.assertEqual([(e.x,e.y) for e in marks],[positions['P'],positions['Q']])
        arcs=[p for p in d.paths if p.role=='boundary-reference-perimeter']
        ends=[p.commands[i][-2:] for p in arcs for i in (0,-1)]
        for point in positions.values(): self.assertEqual(ends.count(point),2)
        self.assertFalse(any('spoke' in p.role for p in d.paths))
        auto=layout(surface.with_reference_arcs(),Style())
        a,b=[(e.x,e.y) for e in auto.ellipses if e.role=='marked-point']
        self.assertEqual(a,(b[0],-b[1]))
        for points in ({'P':(-1000.,0.),'Q':(35.,30.)},
                       {'P':(-35.,30.),'Q':(-35.,30.)}):
            with self.assertRaises(ValueError): render_svg(surface.with_reference_arcs(mark_positions=points))

    def test_member_selection_keeps_geometry_colors_and_marks(self):
        from surface_diagrams.visuals import RAINBOW
        family=GenusSurface(2,type_i=(TypeIBoundary(6),),marks=('P',)).with_reference_arcs(
            mark_positions={'P':(-35,30)})
        full=layout(family,Style())
        self.assertEqual(family.member_numbers,(1,2,3,4,5,6,7))
        selected=layout(family.select(2),Style())
        self.assertEqual([p for p in selected.paths if p.role=='named-cut'],
                         [p for p in full.paths if p.role=='named-cut' and p.stroke==RAINBOW[1]])
        self.assertEqual(selected.ellipses,full.ellipses)
        self.assertEqual({t.text for t in selected.texts},{'P','2'})
        spoke=layout(family.select(6),Style())
        self.assertEqual(sum(p.role=='boundary-reference-perimeter' for p in spoke.paths),1)
        empty=layout(family.select(),Style())
        self.assertFalse(any('reference' in p.role or p.role=='named-cut' for p in empty.paths))
        for numbers in ((0,),(8,),(True,),(2,2)):
            with self.assertRaises(ValueError): family.select(*numbers)

    def test_opposite_end_mixed_reference_family_in_four_views(self):
        expected=None
        for vertical in ('above','below'):
            for horizontal in ('left','right'):
                surface=GenusSurface(3,type_i=(TypeIBoundary(8),),
                    type_ii=(BoundaryPair('left'),BoundaryPair('top'),BoundaryPair('top')),
                    marks=('M',),view_vertical=vertical,view_horizontal=horizontal)
                family=surface.with_reference_arcs()
                drawing=layout(family,Style())
                self.assertEqual(sum(p.role=='boundary-reference-perimeter' for p in drawing.paths),8)
                self.assertFalse(any('spoke' in p.role for p in drawing.paths))
                mark,=drawing.ellipses
                self.assertAlmostEqual(mark.y,0)
                self.assertEqual(family.member_numbers,tuple(range(1,16)))
                ids=tuple(a.id for a in surface.boundary_anchors())
                if expected is None: expected=ids
                self.assertEqual(ids,expected)
                self.assertIn('boundary-reference-perimeter',render_tikz(family))
        with self.assertRaises(NotImplementedError):
            render_svg(GenusSurface(2,type_i=(TypeIBoundary(1),),
                type_ii=(BoundaryPair('left'),)).with_reference_arcs())

    def test_closed_curve_visibility_has_no_invented_wrap_transitions(self):
        from surface_diagrams.visuals import RAINBOW
        for view in ('above','below'):
            surface=GenusSurface(3,type_i=(TypeIBoundary(8),),view_vertical=view)
            solid=layout(surface.with_reference_arcs(),Style())
            self.assertFalse(any(p.dashed for p in solid.paths if p.role=='named-cut'))
            split=layout(surface.with_reference_arcs(closed_curve_style='split'),Style())
            for number in (2,4,6):
                wraps=[p for p in split.paths if p.role=='named-cut' and p.stroke==RAINBOW[number-1]]
                self.assertEqual(len(wraps),1)
                self.assertFalse(wraps[0].dashed)
                self.assertEqual(wraps[0].commands[0][-2:],wraps[0].commands[-1][-2:])
            odd=[p for p in split.paths if p.role=='named-cut' and p.dashed]
            self.assertEqual(len(odd),3)
        with self.assertRaises(ValueError): GenusSurface().with_reference_arcs(closed_curve_style='invalid')

    def test_mixed_perimeter_never_leaves_outer_silhouette(self):
        from surface_diagrams.mesh_atlas import cubic_point, _segment_distance
        def points(commands):
            result=[commands[0][-2:]]
            for cmd in commands[1:]:
                if cmd[0]=='C':
                    curve=(result[-1],cmd[1:3],cmd[3:5],cmd[-2:])
                    result.extend(cubic_point(curve,i/80) for i in range(1,81))
                else: result.append(cmd[-2:])
            return result
        for side in ('left','right'):
            surface=GenusSurface(3,type_i=(TypeIBoundary(8 if side=='left' else 1),),
                type_ii=(BoundaryPair(side),BoundaryPair('top'),BoundaryPair('top')))
            outline=presentation(surface)
            chunks=[points(c) for c in outline.contours]+[points(r.half(1)) for r in outline.rims]
            edges=[(a,b) for chunk in chunks for a,b in zip(chunk,chunk[1:])]
            drawing=layout(surface.with_reference_arcs(),Style())
            for path in drawing.paths:
                if path.role not in ('boundary-reference-perimeter','named-cut','boundary-reference-arc'): continue
                for x,y in points(path.commands):
                    inside=sum((a[1]>y)!=(b[1]>y) and a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])>x
                               for a,b in edges)%2
                    self.assertTrue(inside or min(_segment_distance((x,y),a,b) for a,b in edges)<.015,
                                    (side,path.role,x,y))

    def test_marks_without_outer_rims_keep_member_count_and_closed_perimeter(self):
        for marks in (('M',),('P','Q'),('M','P','Q')):
            family=GenusSurface(2,marks=marks).with_reference_arcs()
            drawing=layout(family,Style())
            arcs=[p for p in drawing.paths if p.role=='boundary-reference-perimeter']
            self.assertEqual(len(arcs),len(marks))
            locations={(e.x,e.y) for e in drawing.ellipses}
            self.assertTrue(all(p.commands[0][-2:] in locations and p.commands[-1][-2:] in locations for p in arcs))
            self.assertEqual(len(family.member_numbers),5+len(marks))
