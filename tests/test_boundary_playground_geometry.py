import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET

from surface_diagrams import Arc, Loop
from surface_diagrams.braid_actions import arc_ray_word, free_homotopy_key, inverse_word, loop_ray_word
from surface_diagrams.boundary_playground_geometry import (
    braid_svg, factorization_svg, row_height, support_curve, support_svg,
)
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.mapping_classes import supported_class


SVG = '{http://www.w3.org/2000/svg}'


class BoundaryPlaygroundGeometryTests(unittest.TestCase):
    def test_three_and_five_point_supports_round_trip_their_exact_classes(self):
        cases = (
            (3, Factor('outer', (), 1, 3)),
            (3, Factor('pair', (2,), 1, 2)),
            (3, Factor('arc', (2,), 1, 2, half=True)),
            (5, Factor('outer', (), 1, 5, 2)),
            (5, Factor('pair', (3, -2), 2, 2)),
            (5, Factor('arc', (3, -2), 2, 2, half=True)),
        )
        for strands, factor in cases:
            with self.subTest(strands=strands, factor=factor.id):
                curve = support_curve(factor.mapping_class, strands)
                expected = supported_class(factor.mapping_class, strands)
                if isinstance(curve, Arc):
                    path = arc_ray_word(strands, curve)
                    observed = (curve.start,) + path + (curve.end,) + inverse_word(path)
                else:
                    self.assertIsInstance(curve, Loop)
                    observed = loop_ray_word(strands, curve)
                self.assertEqual(free_homotopy_key(observed), expected)
                root = ET.fromstring(support_svg(factor, strands))
                role = 'arc' if isinstance(curve, Arc) else 'closed-curve'
                self.assertIsNotNone(root.find(f"{SVG}path[@class='{role}']"))
                self.assertEqual(len(root.findall(f'{SVG}circle')), strands)

    def test_six_point_support_uses_existing_renderer(self):
        factor = Factor('F', (), 1, 2, half=True)
        with patch('surface_diagrams.boundary_playground_geometry.support_drawing', return_value='<svg/>') as old:
            self.assertEqual(support_svg(factor, 6), '<svg/>')
        old.assert_called_once_with(factor.mapping_class)

    def test_continuous_braid_and_paired_export_retain_factor_boundaries(self):
        factors = (Factor('A', (), 1, 3), Factor('B', (2,), 1, 2, half=True))
        braid = ET.fromstring(braid_svg(factors, 3))
        self.assertEqual([node.attrib['data-index'] for node in braid.findall(f"{SVG}rect[@class='braid-row']")],
                         ['0', '1'])
        self.assertEqual(int(braid.attrib['height']), sum(row_height(f) for f in factors))
        braid_paths = 3 * (sum(len(f.word) for f in factors) + 2 * len(factors)) + 1
        self.assertEqual(len(braid.findall(f'{SVG}path')), braid_paths)
        self.assertIn('Continuous 3-strand braid', braid.attrib['aria-label'])
        paired = ET.fromstring(factorization_svg(factors, 3))
        self.assertIsNotNone(paired.find(f'.//{SVG}svg[@aria-label="Continuous 3-strand braid"]'))
        self.assertEqual(len(paired.findall(f'.//{SVG}path')), braid_paths + len(factors))

    def test_support_failure_is_visible_without_erasing_exact_braid(self):
        factor = Factor('A', (), 1, 3)
        with patch('surface_diagrams.boundary_playground_geometry.support_svg', side_effect=ValueError('route failed')):
            root = ET.fromstring(factorization_svg((factor,), 3))
        text = ' '.join(node.text or '' for node in root.iter())
        self.assertIn('Support picture unavailable', text)
        self.assertIn('route failed', text)
        self.assertIsNotNone(root.find(f'.//{SVG}svg[@aria-label="Continuous 3-strand braid"]'))

    def test_invalid_point_count_and_crossing_index_are_rejected(self):
        factor = Factor('A', (), 1, 2, half=True)
        with self.assertRaises(ValueError):
            support_svg(factor, True)
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            braid_svg((Factor('bad', (3,), 1, 2, half=True),), 3)
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            support_curve(Factor('bad', (3,), 1, 2, half=True).mapping_class, 3)


if __name__ == '__main__':
    unittest.main()
