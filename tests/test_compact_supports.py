import unittest
from xml.etree import ElementTree as ET
from pathlib import Path
import json

from surface_diagrams.compact_svg import compact_support_svg
from surface_diagrams.mapping_classes import ConjugatedTwist
from surface_diagrams.twist_supports import support_drawing
from surface_diagrams.factorization_geometry import number_support_points
from surface_diagrams.peripheral_sphere import five_point_cap_certificate
from surface_diagrams.hyperelliptic_homology import IDENTITY
from surface_diagrams.normal_cut_engine import calculate_cut_system
from surface_diagrams.curves import Arc
from surface_diagrams.braid_schedule import commuting_layers
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.braid_stack import stack_row_height


class CompactSupportsTests(unittest.TestCase):
    def test_whitespace_trim_preserves_every_path_and_all_six_marks(self):
        for twist in (ConjugatedTwist((),3,3,power=2),ConjugatedTwist((4,),5,2,half=True)):
            old=number_support_points(support_drawing(twist))
            new=compact_support_svg(old)
            a,b=ET.fromstring(old),ET.fromstring(new)
            self.assertEqual([c.get('d') for c in a.iter() if c.tag.endswith('path')],
                             [c.get('d') for c in b.iter() if c.tag.endswith('path')])
            self.assertEqual(len([c for c in b.iter() if c.get('class')=='marked-point']),6)
            self.assertEqual(len([c for c in b.iter() if c.get('class')=='marked-point-label']),6)
            self.assertFalse(any(c.get('class')=='outer-boundary' for c in b.iter()))
            self.assertLess(float(b.get('height')),float(a.get('height')))

    def test_bezier_control_hull_and_mirror_are_inside_viewport(self):
        svg='<svg viewBox="0 0 400 300"><g transform="translate(0 300) scale(1 -1)"><path d="M 30 20 C 40 250 60 250 70 20"/></g></svg>'
        root=ET.fromstring(compact_support_svg(svg))
        self.assertGreaterEqual(float(root.get('height')),230+14)
        self.assertLess(float(root.get('width')),100)

    def test_single_peripheral_cap_is_sphere_trivial_but_changes_lift(self):
        single,double=five_point_cap_certificate(),five_point_cap_certificate(2)
        self.assertTrue(single['sphere_action']['certified'])
        self.assertFalse(single['lift_preserving'])
        self.assertEqual(single['genus_two_lift'],tuple(tuple(-x for x in r) for r in IDENTITY))
        self.assertTrue(double['lift_preserving'])
        self.assertEqual(len(single['disk_discrepancy']),20)
        self.assertEqual(len(double['disk_discrepancy']),40)
        self.assertFalse(single['disk_equal'])
        self.assertEqual(single['disk_writhe'],20)

    def test_published_sphere_comparison_has_six_points_and_five_joint_arcs(self):
        folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        data=json.loads((folder/'sphere-cut-certificate.json').read_text())
        self.assertEqual(data['points'],6)
        arcs=tuple(Arc(**dict(a,cuts=tuple(a['cuts']))) for a in data['arcs'])
        self.assertEqual([(a.start,a.end) for a in arcs],[(i,i+1) for i in range(1,6)])
        self.assertEqual(len(calculate_cut_system(arcs).paths),5)
        self.assertEqual(len([c for c in ET.fromstring((folder/'sphere-cut.svg').read_text()).iter()
                              if c.get('class')=='marked-point']),6)

    def test_every_published_compact_braid_uses_only_exact_commutations(self):
        folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        data=json.loads((folder/'display.json').read_text())
        for word in {tuple(row['word']) for row in data['rows']}:
            layered=tuple(letter for layer in commuting_layers(6,word) for letter in layer.letters)
            self.assertEqual(exact_action(layered),exact_action(word))
        for row in data['rows']:
            self.assertEqual(row['height'],stack_row_height(row['word'],compact=True))
        for svg in data['supports']:
            nodes=list(ET.fromstring(svg).iter())
            self.assertFalse(any(n.get('class')=='outer-boundary' for n in nodes))
            self.assertEqual(sum(n.get('class')=='marked-point' for n in nodes),6)


if __name__=='__main__':unittest.main()
