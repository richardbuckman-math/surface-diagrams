"""Compact braid spacing changes the picture, not its signed factor words."""

from hashlib import sha256
import re
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET

from surface_diagrams.boundary_playground_geometry import (
    braid_svg as boundary_braid_svg, factorization_svg as boundary_paired_svg,
    row_height as boundary_row_height,
)
from surface_diagrams.factorization_explorer import Factor, initial_factors
from surface_diagrams.factorization_geometry import (
    braid_svg as six_braid_svg, factorization_svg as six_paired_svg,
    row_height as six_row_height,
)
from surface_diagrams.visuals import RAINBOW


SVG = '{http://www.w3.org/2000/svg}'


def _factor(name, word):
    return SimpleNamespace(id=name, label=name, word=tuple(word))


def _assert_compact_braid(test, svg, factors, strands, row_height):
    root = ET.fromstring(svg)
    height = sum(row_height(factor, compact=True) for factor in factors)
    test.assertEqual(int(root.attrib['height']), height)
    rows = root.findall(f"{SVG}rect[@class='braid-row']")
    test.assertEqual([int(row.attrib['y']) for row in rows],
                     [0, *[sum(row_height(f, compact=True) for f in factors[:i])
                            for i in range(1, len(factors))]])
    test.assertEqual([int(row.attrib['height']) for row in rows],
                     [row_height(f, compact=True) for f in factors])
    separators = root.findall(f"{SVG}path[@stroke-dasharray='3 5']")
    test.assertEqual(len(separators), len(factors) - 1)
    test.assertIn(f'M 12 {row_height(factors[0], compact=True)} H',
                  separators[0].attrib['d'])

    order = list(range(strands))
    for letter in (letter for factor in factors for letter in factor.word):
        index = abs(letter) - 1
        order[index], order[index + 1] = order[index + 1], order[index]
    paths = [path for path in root.findall(f'{SVG}path')
             if 'stroke-dasharray' not in path.attrib]
    # Every factor finishes with a straight connector, so these are the
    # strand endpoints of the complete, unaltered word.
    for column, path in enumerate(paths[-strands:]):
        numbers = [float(part) for part in re.findall(r'-?\d+(?:\.\d+)?', path.attrib['d'])]
        x, y = numbers[-2:]
        width = float(root.attrib['width'])
        test.assertAlmostEqual(x, width / 2 + (column - (strands - 1) / 2) * 28)
        test.assertAlmostEqual(y, height)
        test.assertEqual(path.attrib['stroke'], RAINBOW[order[column] % len(RAINBOW)])


class CompactBraidGeometryTests(unittest.TestCase):
    def test_default_svg_is_preserved(self):
        boundary = (Factor('A', (), 1, 3), Factor('B', (2,), 1, 2, half=True))
        self.assertEqual(sha256(boundary_braid_svg(boundary, 3).encode()).hexdigest(),
                         'd02a900713176aa859f4a0f80d5fcdbc4d329cb4f3d5e44d6ef48054593f2158')
        self.assertEqual(sha256(six_braid_svg(initial_factors()[:2]).encode()).hexdigest(),
                         '185ffab418ce1671f7f5cc987d974f2dab4276a0c730c2aa5f17afa315c7ebf6')

    def test_compact_rows_shrink_commuting_blocks_and_preserve_endpoints(self):
        boundary = (_factor('A', (1, 3) * 20), _factor('B', (1, 2, 3)),
                    _factor('C', ()))
        self.assertLess(boundary_row_height(boundary[0], compact=True),
                        boundary_row_height(boundary[0]))
        _assert_compact_braid(self, boundary_braid_svg(boundary, 4, compact=True),
                              boundary, 4, boundary_row_height)

        six = (_factor('A', (1, 3, 5) * 20), _factor('B', (1, 2, 3)),
               _factor('C', ()))
        self.assertLess(six_row_height(six[0], compact=True), six_row_height(six[0]))
        _assert_compact_braid(self, six_braid_svg(six, compact=True),
                              six, 6, six_row_height)

    def test_compact_paired_exports_align_support_rows_and_braid(self):
        factors = (_factor('A', (1, 3) * 20), _factor('B', (1, 2, 3)))
        with patch('surface_diagrams.boundary_playground_geometry.support_svg',
                   return_value='<svg width="100" height="100"/>'):
            boundary = ET.fromstring(boundary_paired_svg(factors, 4, compact=True))
        self.assertEqual(int(boundary.attrib['height']),
                         sum(boundary_row_height(f, compact=True) for f in factors) + 28)
        self.assertEqual(int(boundary.find(f'.//{SVG}svg[@aria-label="Continuous 4-strand braid"]').attrib['height']),
                         sum(boundary_row_height(f, compact=True) for f in factors))

        with patch('surface_diagrams.factorization_geometry.support_svg',
                   return_value='<svg width="100" height="100"/>'), \
             patch('surface_diagrams.factorization_audit.support_audit',
                   return_value={'matches': True, 'message': 'ok'}):
            six = ET.fromstring(six_paired_svg(factors, compact=True))
        self.assertEqual(int(six.attrib['height']),
                         sum(six_row_height(f, compact=True) for f in factors) + 28)
        self.assertEqual(int(six.find(f'.//{SVG}svg[@aria-label="Continuous six-strand braid"]').attrib['height']),
                         sum(six_row_height(f, compact=True) for f in factors))


if __name__ == '__main__':
    unittest.main()
