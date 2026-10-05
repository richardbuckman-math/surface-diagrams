import json
import runpy
import unittest
from pathlib import Path

from surface_diagrams.boundary_playground_app import BoundaryLab


class BoundaryPlaygroundAppTests(unittest.TestCase):
    def apply(self, lab, **payload):
        lab.mutate(dict(payload, revision=lab.revision))

    def test_three_point_walkthrough_keeps_every_checked_step(self):
        lab = BoundaryLab()
        opening = lab.state()
        self.assertEqual((opening['points'], opening['power']), (3, 1))
        self.assertIn('<svg', opening['braid'])
        self.assertTrue(opening['factors'][0]['svg'])
        self.apply(lab, op='example')
        state = lab.state()
        self.assertEqual(len(state['steps']), 7)
        self.assertEqual(len(state['factors']), 3)
        self.assertEqual([factor['half'] for factor in state['factors']],
                         [True, True, False])
        self.assertEqual(state['factors'][-1]['power'], 2)
        self.assertIn('<svg', lab.export_svg())
        self.apply(lab, op='seek', position=2)
        self.assertEqual(len(lab.project.factors), 3)
        self.apply(lab, op='redo')
        self.assertEqual(len(lab.project.factors), 4)

    def test_five_point_power_split_and_durable_history(self):
        lab = BoundaryLab()
        self.apply(lab, op='new', points=5, power=2)
        self.apply(lab, op='split', index=0, kind='powers')
        self.assertEqual(len(lab.project.factors), 2)
        self.assertEqual(lab.state()['target_word'], tuple(range(1, 5)) * 10)
        saved = lab.session_document()
        restored = BoundaryLab()
        restored.restore(saved)
        self.assertEqual(restored.project.to_dict(), lab.project.to_dict())
        self.apply(restored, op='undo')
        self.assertEqual(len(restored.project.factors), 1)
        self.apply(restored, op='redo')
        self.assertEqual(len(restored.project.factors), 2)

    def test_invalid_import_and_session_leave_workspace_intact(self):
        lab = BoundaryLab()
        before = lab.session_document()
        with self.assertRaises(ValueError):
            self.apply(lab, op='import', document={'format':'wrong'})
        self.assertEqual(lab.session_document(), before)
        bad = dict(before, position=100)
        with self.assertRaises(ValueError):
            lab.restore(bad)
        self.assertEqual(lab.session_document(), before)

    def test_published_browser_adapter_uses_same_checked_engine(self):
        backend = Path(__file__).resolve().parents[1] / 'src' / 'surface_diagrams' / 'boundary_assets' / 'backend.py'
        browser = runpy.run_path(str(backend))
        dispatch = browser['dispatch']
        opening = json.loads(dispatch('/api/state', 'GET', ''))
        self.assertEqual(opening['status'], 200)
        state = json.loads(opening['body'])
        self.assertEqual((state['points'], state['power']), (3, 1))
        changed = json.loads(dispatch('/api/action', 'POST', json.dumps({
            'op': 'example', 'revision': state['revision'],
        })))
        self.assertEqual(changed['status'], 200)
        self.assertEqual(len(json.loads(changed['body'])['steps']), 7)
        saved = json.dumps(changed['session'])
        reopened = runpy.run_path(str(backend))
        reopened['restore_browser_session'](saved)
        reopened_response = json.loads(reopened['dispatch']('/api/state', 'GET', ''))
        self.assertEqual(len(json.loads(reopened_response['body'])['factors']), 3)
        svg = json.loads(reopened['dispatch']('/api/export.svg', 'GET', ''))
        self.assertEqual(svg['status'], 200)
        self.assertIn('<svg', svg['body'])


if __name__ == '__main__':
    unittest.main()
