"""The Xiao workspace preserves its own exact disk product and saved state."""

import json
import runpy
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from surface_diagrams.factorization_explorer import export_factors, initial_factors, product
from surface_diagrams.factorization_lab import LabServer, validated_session_document
from surface_diagrams.fibration_lab_seeds import XIAO_FOUR_THREE
from surface_diagrams.mapping_classes import exact_action


ASSETS = Path(__file__).resolve().parents[1] / 'src' / 'surface_diagrams' / 'lab_assets'


class XiaoFactorizationLabTests(unittest.TestCase):
    def test_variant_moves_split_combine_reset_and_seed_bound_import(self):
        seed = XIAO_FOUR_THREE.factors
        seed_action = exact_action(product(seed))
        self.assertNotEqual(seed_action, exact_action(()))
        lab = LabServer(seed_slug='4-3')
        try:
            state = lab.state()
            self.assertEqual(state['seed_slug'], '4-3')
            self.assertEqual([factor['id'] for factor in state['factors']],
                             ['D', '1', 'R', 'U', 'infinity', 'L', '0'])
            self.assertEqual(state['export']['seed'], '4-3')
            lab.mutate(dict(op='move', index=0, target=1, revision=0))
            self.assertEqual([factor.id for factor in lab.history[-1][:2]], ['1', 'D'])
            self.assertEqual(exact_action(product(lab.history[-1])), seed_action)
            lab.mutate(dict(op='split', index=0, kind='powers', revision=1))
            self.assertEqual(len(lab.history[-1]), 8)
            lab.mutate(dict(op='combine', index=0, revision=2))
            self.assertEqual(len(lab.history[-1]), 7)
            self.assertEqual(exact_action(product(lab.history[-1])), seed_action)
            lab.mutate(dict(op='undo', revision=3))
            self.assertEqual(len(lab.history[lab.position]), 8)
            lab.mutate(dict(op='redo', revision=4))
            exported = json.loads(json.dumps(lab.state()['export']))
            lab.mutate(dict(op='import', document=exported, revision=5))
            self.assertEqual(exact_action(product(lab.history[-1])), seed_action)
            previous = lab.session_document()
            wrong = export_factors(seed)
            with self.assertRaisesRegex(ValueError, 'different lab seed'):
                lab.mutate(dict(op='import', document=wrong, revision=6))
            wrong = json.loads(json.dumps(export_factors(initial_factors())))
            wrong['seed'] = '4-3'
            with self.assertRaisesRegex(ValueError, 'disk action'):
                lab.mutate(dict(op='import', document=wrong, revision=6))
            altered = json.loads(json.dumps(exported))
            altered['factors'][-1]['power'] = 1
            altered['factors'][-1].pop('word')
            with self.assertRaisesRegex(ValueError, 'disk action'):
                lab.mutate(dict(op='import', document=altered, revision=6))
            self.assertEqual(lab.session_document(), previous)
            lab.mutate(dict(op='reset', revision=6))
            self.assertEqual(lab.history[-1], seed)
        finally:
            lab.server_close()

    def test_variant_global_frame_and_disk_session_are_seed_bound(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / 'xiao-session.json'
            lab = LabServer(session_path=path, seed_slug='4-3')
            try:
                lab.mutate(dict(op='conjugate', word=[1], revision=0))
                exported = lab.state()['export']
                self.assertEqual(exported['global_conjugator'], (1,))
                self.assertEqual(lab.frames[-1], (1,))
            finally:
                lab.server_close()
            reopened = LabServer(session_path=path, seed_slug='4-3')
            try:
                self.assertEqual(reopened.history[-1], lab.history[-1])
                self.assertEqual(reopened.frames[-1], (1,))
            finally:
                reopened.server_close()
            with self.assertRaisesRegex(ValueError, 'different factorization lab'):
                LabServer(session_path=path)
            saved = json.loads(path.read_text(encoding='utf-8'))
            saved['history'][-1]['factors'][-1]['power'] = 1
            saved['history'][-1]['factors'][-1].pop('word')
            with self.assertRaises(ValueError):
                validated_session_document(saved, '4-3')

    def test_public_adapter_selects_xiao_and_restores_its_own_history(self):
        adapter = runpy.run_path(str(ASSETS / 'public-lab-backend.py'))
        adapter['select_lab_seed']('4-3')
        dispatch = adapter['dispatch']
        state = json.loads(dispatch('/api/state', 'GET', ''))
        self.assertEqual(json.loads(state['body'])['seed_slug'], '4-3')
        moved = json.loads(dispatch('/api/action', 'POST', json.dumps(
            dict(op='move', index=0, target=1, revision=0))))
        self.assertEqual(moved['status'], 200)
        self.assertEqual(moved['session']['seed'], '4-3')
        fresh = runpy.run_path(str(ASSETS / 'public-lab-backend.py'))
        fresh['select_lab_seed']('4-3')
        fresh['restore_browser_session'](json.dumps(moved['session']))
        restored = json.loads(fresh['dispatch']('/api/state', 'GET', ''))
        self.assertEqual(json.loads(restored['body'])['position'], 1)
        other = runpy.run_path(str(ASSETS / 'public-lab-backend.py'))
        other['restore_browser_session'](json.dumps(moved['session']))
        fallback = json.loads(other['dispatch']('/api/state', 'GET', ''))
        self.assertEqual(json.loads(fallback['body'])['seed_slug'], '6-7')
        self.assertEqual(json.loads(fallback['body'])['position'], 0)


if __name__ == '__main__':
    unittest.main()
