"""Continuity and the user's explicit arc/cylinder calibration."""
import unittest
from xml.etree import ElementTree as ET

from surface_diagrams.braid_stack import braid_fragment_svg, connected_braid_svg, stack_row_height
from surface_diagrams.braid_actions import arc_ray_word, free_homotopy_key, inverse_word
from surface_diagrams.mapping_classes import ConjugatedTwist, supported_class, exact_action
from surface_diagrams.twist_supports import support_curve


class BraidStackTests(unittest.TestCase):
    def test_below_five_half_twist_is_four_five_inverse_four(self):
        twist = ConjugatedTwist((4,), 5, 2, half=True)
        self.assertEqual(twist.word, (4,5,-4))
        arc = support_curve(twist)
        self.assertEqual((arc.start,arc.end,arc.cuts,arc.direction), (4,6,(),'down'))
        # The neighborhood boundary is the exact support of the squared half.
        path = arc_ray_word(6,arc)
        boundary = (arc.start,) + path + (arc.end,) + inverse_word(path)
        self.assertEqual(free_homotopy_key(boundary), supported_class(twist))
        full = ConjugatedTwist((4,),5,2)
        self.assertEqual(exact_action(twist.word*2), exact_action(full.word))

    def test_fragments_reach_the_edges_and_carry_permuted_colors(self):
        first = braid_fragment_svg((4,5,-4))
        second = braid_fragment_svg((1,-3),order=first['exit_order'])
        self.assertEqual(first['exit_order'], (0,1,2,5,4,3))
        for fragment in (first,second):
            root = ET.fromstring(fragment['svg'])
            paths = list(root)
            self.assertEqual(len(paths[:6]),6)
            self.assertTrue(all(float(p.attrib['d'].split()[2])==0 for p in paths[:6]))
            self.assertTrue(all(float(p.attrib['d'].split()[-1])==fragment['height'] for p in paths[-6:]))
        start_colors = [p.attrib['stroke'] for p in list(ET.fromstring(second['svg']))[:6]]
        self.assertEqual(start_colors,['#d73027','#e08214','#b59b00','#5254c8','#168aad','#23964f'])

    def test_continuous_export_has_aligned_factor_separators(self):
        words=((4,5,-4),(2,2),())
        root=ET.fromstring(connected_braid_svg(words))
        self.assertEqual(int(root.attrib['height']),sum(map(stack_row_height,words)))
        self.assertEqual(sum(c.get('class')=='factor-separator' for c in root),2)
        self.assertEqual([c.get('transform') for c in root if c.get('data-factor') is not None],
                         ['translate(0 0)','translate(0 130)','translate(0 260)'])


if __name__=='__main__':unittest.main()
