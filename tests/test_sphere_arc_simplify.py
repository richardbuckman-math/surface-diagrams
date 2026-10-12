import json
import runpy
import unittest
from pathlib import Path

from surface_diagrams.factorization_lab import LabServer


class SphereArcColumnTests(unittest.TestCase):
    def test_original_thirteen_rows_have_joint_five_arc_charts(self):
        server = LabServer()
        try:
            rows = [server.sphere_cut_row(row, 7) for row in range(1, 14)]
        finally:
            server.server_close()
        self.assertEqual([row['direction'] for row in rows],
                         ['forward'] * 7 + ['backward'] * 6)
        self.assertTrue(all(row['joint_certified'] for row in rows))
        self.assertTrue(all(row['svg'].count('class="arc"') == 5 for row in rows))
        self.assertTrue(all(row['svg_strip'].count('class="arc"') == 5 for row in rows))
        self.assertTrue(all('<rect class="outer-boundary"' in row['svg_strip']
                            and '<ellipse class="outer-boundary"' in row['svg']
                            for row in rows))
        self.assertTrue(all(row['svg_strip'].count('class="vertical-ray"') == 6
                            and row['svg_strip'].count('class="horizontal-cut"') == 1
                            for row in rows))
        self.assertTrue(rows[6]['meet_certified'])
        self.assertFalse(rows[6]['meet_disk_equal'])
        self.assertTrue(rows[6]['meet_backward']['joint_certified'])
        self.assertTrue(rows[6]['meet_picture_equal'])
        self.assertTrue(rows[6]['meet_picture_equal_strip'])
        self.assertEqual(rows[6]['svg'], rows[7]['svg'])
        self.assertEqual(rows[6]['svg_strip'], rows[7]['svg_strip'])
        self.assertEqual(rows[6]['meet_backward']['svg'], rows[7]['svg'])
        self.assertEqual(rows[-1]['cut_counts'], (0, 7, 0, 7, 5))
        self.assertEqual(rows[-1]['braid_letters'], 14)  # inverse F13, before its action
        self.assertLess(sum(rows[6]['cut_counts']), 147 + 220 + 40 + 275 + 68)
        self.assertEqual(rows[6]['endpoints'], ((4, 5), (5, 3), (1, 3), (1, 2), (2, 6)))

    def test_split_selector_changes_direction_and_validates_bounds(self):
        server = LabServer()
        try:
            backward=server.sphere_cut_row(5, 4)
            forward=server.sphere_cut_row(4, 4)
            self.assertEqual(backward['direction'], 'backward')
            self.assertEqual(forward['direction'], 'forward')
            self.assertTrue(forward['meet_certified'])
            self.assertEqual(forward['svg'], backward['svg'])
            with self.assertRaisesRegex(ValueError, 'factor row'):
                server.sphere_cut_row(0, 7)
            with self.assertRaisesRegex(ValueError, 'at least one factor'):
                server.sphere_cut_row(7, 13)
        finally:
            server.server_close()

    def test_public_adapter_exposes_same_chart(self):
        asset = Path(__file__).resolve().parents[1] / 'src' / 'surface_diagrams' / 'lab_assets' / 'public-lab-backend.py'
        dispatch = runpy.run_path(str(asset))['dispatch']
        result = json.loads(dispatch('/api/sphere-cut?row=13&split=7&revision=0', 'GET', ''))
        self.assertEqual(result['status'], 200)
        data = json.loads(result['body'])
        self.assertEqual(data['direction'], 'backward')
        self.assertEqual(data['cut_counts'], [0, 7, 0, 7, 5])
        self.assertEqual(data['svg'].count('class="arc"'), 5)
        self.assertEqual(data['svg_strip'].count('class="arc"'), 5)


if __name__ == '__main__':
    unittest.main()
