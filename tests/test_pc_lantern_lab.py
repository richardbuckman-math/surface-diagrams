"""Checked PC lantern factorization and its three aligned prefix pictures."""

import json
import runpy
import unittest
from pathlib import Path

from surface_diagrams.boundary_playground import new_project
from surface_diagrams.braid_actions import artin_action
from surface_diagrams.pc_lantern_lab import PCLanternLab, chain_arcs, cut_system_svg


ASSETS = Path(__file__).resolve().parents[1] / 'src' / 'surface_diagrams' / 'boundary_assets'


class PCLanternLabTests(unittest.TestCase):
    def apply(self, lab, **payload):
        lab.mutate(dict(payload, revision=lab.revision))

    def test_opening_relation_and_every_prefix_are_exact(self):
        lab = PCLanternLab()
        state = lab.state()
        self.assertEqual([factor['id'] for factor in state['factors']],
                         ['T12', 'T13', 'T23'])
        self.assertEqual(len(state['cut_steps']), 5)  # F0–F3 and direct T123
        self.assertEqual([step['index'] for step in state['cut_steps']],
                         [0, 1, 2, 3, 'target'])
        target = new_project(3)
        self.assertEqual(artin_action(3, lab.project.word),
                         artin_action(3, target.word))
        self.assertEqual(chain_arcs(lab.project.word), chain_arcs(target.word))
        self.assertEqual(state['cut_steps'][3]['arcs'], state['cut_steps'][4]['arcs'])
        self.assertEqual(state['cut_steps'][0]['word'], ())
        for index, step in enumerate(state['cut_steps'][1:4], 1):
            self.assertEqual(step['word'],
                             tuple(letter for factor in lab.project.factors[:index]
                                   for letter in factor.word))
            self.assertEqual(step['arcs'], tuple(dict(start=arc.start, end=arc.end,
                cuts=arc.cuts, initial_up=arc.initial_up) for arc in chain_arcs(step['word'])))
            self.assertEqual(step['svg'].count('class="arc"'), 3)

    def test_mirror_is_display_only_for_cut_paths_and_supports(self):
        lab = PCLanternLab()
        state = lab.state()
        self.assertIn('scale(1 -1)', cut_system_svg((1, 1), True))
        self.assertNotIn('scale(1 -1)', cut_system_svg((1, 1), False))
        self.assertEqual([factor['word'] for factor in state['factors']],
                         [factor.word for factor in lab.project.factors])
        for factor in state['factors']:
            self.assertTrue(factor['svg_mirrored'])
            self.assertTrue(factor['svg_unmirrored'])
            self.assertIn('scale(1 -1)', factor['svg_mirrored'])
            self.assertNotIn('scale(1 -1)', factor['svg_unmirrored'])
        self.assertEqual(state['braid'].count('scale(1 -1)'), 0)

    def test_hurwitz_split_combine_undo_and_saved_history(self):
        lab = PCLanternLab()
        original = lab.project.word
        self.apply(lab, op='move', index=0, target=1)
        self.assertEqual(artin_action(3, lab.project.word), artin_action(3, original))
        self.apply(lab, op='split', index=1, kind='halves')
        self.assertEqual(len(lab.project.factors), 4)
        self.apply(lab, op='combine', index=1)
        self.assertEqual(len(lab.project.factors), 3)
        saved = lab.session_document()
        restored = PCLanternLab()
        restored.restore(saved)
        self.assertEqual(restored.project.to_dict(), lab.project.to_dict())
        self.apply(restored, op='undo')
        self.assertEqual(len(restored.project.factors), 4)
        self.apply(restored, op='redo')
        self.assertEqual(len(restored.project.factors), 3)
        self.assertIn('<svg', restored.export_svg())
        self.apply(restored, op='new', points=3, power=1)
        self.assertEqual(len(restored.project.factors), 1)
        self.apply(restored, op='example')
        self.assertEqual(len(restored.project.factors), 3)

    def test_rejects_other_targets_without_replacing_session(self):
        lab = PCLanternLab()
        saved = lab.session_document()
        with self.assertRaises(ValueError):
            self.apply(lab, op='new', points=5, power=1)
        with self.assertRaises(ValueError):
            self.apply(lab, op='import', document=new_project(5).to_dict())
        self.assertEqual(lab.session_document(), saved)
        foreign = dict(saved, history=[new_project(5).to_dict()])
        with self.assertRaises(ValueError):
            lab.restore(foreign)
        self.assertEqual(lab.session_document(), saved)

    def test_browser_adapter_and_column_controls(self):
        browser = runpy.run_path(str(ASSETS / 'pc-backend.py'))
        dispatch = browser['dispatch']
        opening = json.loads(dispatch('/api/state', 'GET', ''))
        self.assertEqual(opening['status'], 200)
        state = json.loads(opening['body'])
        self.assertEqual(len(state['factors']), 3)
        self.assertEqual(len(state['cut_steps']), 5)
        self.assertIn('braid_compact', state)
        compact = json.loads(dispatch('/api/export.svg?compact=1&mirror=0', 'GET', ''))
        self.assertEqual(compact['status'], 200)
        self.assertNotIn('scale(1 -1)', compact['body'])
        mirrored = json.loads(dispatch('/api/export.svg?compact=1&mirror=1', 'GET', ''))
        self.assertEqual(mirrored['status'], 200)
        self.assertIn('scale(1 -1)', mirrored['body'])
        changed = json.loads(dispatch('/api/action', 'POST', json.dumps({
            'op':'move', 'index':0, 'target':1, 'revision':state['revision']})))
        self.assertEqual(changed['status'], 200)
        moved = json.loads(changed['body'])
        self.assertEqual(moved['cut_steps'][1]['word'], moved['factors'][0]['word'])
        reopened = runpy.run_path(str(ASSETS / 'pc-backend.py'))
        reopened['restore_browser_session'](json.dumps(changed['session']))
        replay = json.loads(reopened['dispatch']('/api/state', 'GET', ''))
        self.assertEqual(replay['status'], 200)
        self.assertEqual(json.loads(replay['body'])['position'], 1)
        page = (ASSETS / 'pc-lantern.html').read_text(encoding='utf-8')
        script = (ASSETS / 'pc-cuts.js').read_text(encoding='utf-8')
        for control in ('pc-show-column', 'pc-arc-1', 'pc-arc-2', 'pc-arc-3',
                        'pc-show-all', 'pc-hide-all', 'pc-orientation', 'pc-cuts-column'):
            self.assertIn(f'id="{control}"', page)
        self.assertIn('state.cut_steps.slice(1, -1)', script)
        self.assertIn('state.factors[index].height', script)
        self.assertIn('factorCards[index]?.offsetHeight', script)
        self.assertIn('ResizeObserver(syncPcRowHeights)', script)
        self.assertIn('path.arc', script)


if __name__ == '__main__':
    unittest.main()
