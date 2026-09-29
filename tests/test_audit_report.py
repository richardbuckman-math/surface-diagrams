"""The report's selectable pieces must retain the exported curve geometry."""
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from surface_diagrams import Arc, PlanarSurface, render_svg

spec=importlib.util.spec_from_file_location('audit_factor_nine',
    Path(__file__).resolve().parents[1]/'examples'/'audit_factor_nine.py')
report=importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


class AuditReportTests(unittest.TestCase):
    def test_overlay_preserves_arc_and_segment_continuity(self):
        arc=Arc(1,4,(4,2,1,4,5,1,2,4,2),direction='down')
        svg=render_svg(PlanarSurface.row('PPPPPP',spacing=50,height=220,margin=55).with_curves(arc))
        ns={'s':'http://www.w3.org/2000/svg'}
        original=ET.fromstring(svg).find("s:path[@class='arc']",ns)
        result=ET.fromstring(report.segment_overlay(svg,10))
        self.assertEqual(result.find("s:path[@class='arc']",ns).attrib,original.attrib)
        pieces=result.findall("s:path[@class='audit-segment']",ns)
        self.assertEqual([p.get('id') for p in pieces],[f'segment-{i}' for i in range(1,11)])
        words=original.get('d').split()
        previous=words[1:3]
        rebuilt=words[:3]
        for piece in pieces:
            tokens=piece.get('d').split()
            self.assertEqual(tokens[:3],['M']+previous)
            rebuilt.extend(tokens[3:])
            previous=tokens[-2:]
        self.assertEqual(rebuilt,words)
        with self.assertRaises(ValueError): report.segment_overlay(svg,9)
