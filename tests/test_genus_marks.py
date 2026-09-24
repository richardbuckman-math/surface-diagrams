import unittest
from dataclasses import replace
from surface_diagrams import GenusSurface, Style, render_svg
from surface_diagrams.layout import layout
from surface_diagrams.cut_systems import validate_cut_system
from surface_diagrams.genus_mesh import genus_binding
from surface_diagrams.disk_routes import DiskRoute, MarkPoint
from surface_diagrams.mesh_atlas import _near


class GenusMarkTests(unittest.TestCase):
    def test_marked_complements_and_stable_spokes_in_all_views(self):
        expected = None
        for vertical in ('above','below'):
            for horizontal in ('left','right'):
                surface = GenusSurface(2,marks=('P','Q'),view_vertical=vertical,view_horizontal=horizontal)
                binding = genus_binding(surface)
                report = binding.system.validate()
                self.assertTrue(report.certified, report.diagnostics)
                self.assertTrue(all(not c.interior_marks for c in report.complement))
                self.assertEqual(len(binding.charts()[0].charts), 2)
                walks = tuple(p.walk for p in binding.system.cellulation.parents)
                if expected is not None:
                    self.assertEqual(expected, walks)
                expected = walks
                self.assertEqual(tuple(n for n,_ in binding.system.numbers), tuple(range(1,8)))

    def test_omitted_spoke_leaves_interior_mark_and_is_not_certified(self):
        system = GenusSurface(1,marks=('P',)).cut_system()
        cell = system.cellulation
        spoke = cell.parents[-1]
        by_side = {s:p.id for p in cell.pairs for s in (p.first,p.second)}
        removed = {by_side[s] for s in spoke.walk}
        broken = replace(cell,cuts=tuple(c for c in cell.cuts if c not in removed),parents=cell.parents[:-1],attachments=())
        report = validate_cut_system(broken,system.surface)
        self.assertFalse(report.certified)
        self.assertTrue(any(c.interior_marks for c in report.complement))

    def test_arc_endpoints_are_the_actual_mark_vertices(self):
        surface = GenusSurface(2,marks=('P','Q'))
        binding = genus_binding(surface)
        route = DiskRoute((),MarkPoint('P'),MarkPoint('Q'),id='PQ')
        projected = binding.project(route)
        geometry = {t.face:t for t in binding.triangles}
        point_by_side = {s:geometry[f.id].points[i] for f in binding.system.cellulation.faces for i,s in enumerate(f.sides)}
        expected = [point_by_side[m.corner] for m in binding.system.cellulation.marks]
        self.assertTrue(_near(projected[0].points[0],expected[0]))
        self.assertTrue(_near(projected[-1].points[-1],expected[1]))
        for a,b in zip(projected,projected[1:]):
            self.assertTrue(_near(a.points[-1],b.points[0]))
        self.assertIn('marked-point',render_svg(surface))
        self.assertIn('surface-route',render_svg(surface.with_curves(route)))

    def test_maximum_automatic_marks_and_invalid_ids(self):
        for genus in (1,2,5):
            binding = genus_binding(GenusSurface(genus,marks=tuple('P'+str(i) for i in range(2*genus+1))))
            self.assertEqual(len(binding.charts()[0].charts),2)
        for marks in (('P','P'),('',),(1,),('a','b','c','d')):
            with self.assertRaises(ValueError):
                GenusSurface(1,marks=marks)

    def test_rendered_routes_meet_displayed_marks_in_every_view(self):
        for vertical in ('above','below'):
            for horizontal in ('left','right'):
                for start,end in (('P','Q'),('Q','P')):
                    with self.subTest(vertical=vertical,horizontal=horizontal,start=start):
                        surface=GenusSurface(2,marks=('P','Q'),
                            view_vertical=vertical,view_horizontal=horizontal)
                        route=DiskRoute((),MarkPoint(start),MarkPoint(end),id='between-marks')
                        drawing=layout(surface.with_curves(route),Style())
                        marks=[(e.x,e.y) for e in drawing.ellipses if e.role=='marked-point']
                        paths=[p for p in drawing.paths if p.role=='surface-route']
                        self.assertEqual(len(marks),2)
                        self.assertTrue(paths)
                        expected=marks if start=='P' else marks[::-1]
                        self.assertTrue(_near(paths[0].commands[0][-2:],expected[0]))
                        self.assertTrue(_near(paths[-1].commands[-1][-2:],expected[1]))
                        for a,b in zip(paths,paths[1:]):
                            self.assertTrue(_near(a.commands[-1][-2:],b.commands[0][-2:]))
