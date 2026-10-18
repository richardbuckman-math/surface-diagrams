"""Dictated support classes, honest closure status, and isolated lab histories."""
import json
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
import unittest

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_audit import support_audit
from surface_diagrams.factorization_explorer import export_factors, product
from surface_diagrams.factorization_lab import LabServer, validated_session_document
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.model import PlanarSurface, Style
from surface_diagrams.svg import render_svg
from surface_diagrams.ten_ten import (TEN_TEN_FACTORS, SOURCE_ROUTES,
                                     SOURCE_DESCRIPTIONS, route_boundary,
                                     transcription_certificate)

ASSETS = Path(__file__).resolve().parents[1] / 'src/surface_diagrams/lab_assets'


class TenTenLabTests(unittest.TestCase):
    def test_every_dictated_route_matches_its_exact_support_and_draws(self):
        self.assertEqual(len(SOURCE_ROUTES), 20)
        self.assertEqual(len(SOURCE_DESCRIPTIONS), 20)
        for i, (curve, factor) in enumerate(zip(SOURCE_ROUTES, TEN_TEN_FACTORS), 1):
            with self.subTest(factor=i):
                self.assertEqual(factor.id, f'F{i}')
                self.assertEqual(route_boundary(curve), supported_class(factor.mapping_class))
                self.assertTrue(support_audit(factor)['matches'])
                self.assertIn('<svg', render_svg(
                    PlanarSurface.row('PPPPPP', spacing=50, height=220, margin=55).with_curves(curve),
                    style=Style(curve_width=1.5, marked_point_radius=3.5)))
        self.assertEqual(TEN_TEN_FACTORS[3].mapping_class, TEN_TEN_FACTORS[12].mapping_class)
        self.assertEqual(TEN_TEN_FACTORS[4].mapping_class, TEN_TEN_FACTORS[13].mapping_class)
        self.assertEqual(TEN_TEN_FACTORS[6].mapping_class, TEN_TEN_FACTORS[17].mapping_class)

    def test_twenty_factor_count_does_not_masquerade_as_identity(self):
        self.assertEqual(sum(f.half for f in TEN_TEN_FACTORS), 10)
        self.assertEqual(sum(not f.half and f.points == 3 and f.power == 2
                             for f in TEN_TEN_FACTORS), 10)
        check = transcription_certificate()
        self.assertTrue(all(check['supports_match']))
        self.assertEqual(check['provisional_factors'], [])
        self.assertEqual(check['confirmed_clarifications'], ['F7'])
        self.assertFalse(check['sphere_identity'])
        self.assertFalse(check['disk_identity'])
        self.assertFalse(check['homology_identity'])
        self.assertEqual(check['homology'], ((-14,19,19,-20),(12,-15,-16,16),
                                             (-9,12,13,-12),(15,-19,-19,21)))
        word = product(TEN_TEN_FACTORS)
        self.assertEqual(sum(1 if x > 0 else -1 for x in word), 130)

    def test_moves_splits_export_and_reopen_preserve_this_seed_only(self):
        expected = exact_action(product(TEN_TEN_FACTORS))
        lab = LabServer(seed_slug='10-10')
        try:
            state = lab.state()
            self.assertEqual(state['export']['seed'], '10-10')
            self.assertEqual(len(state['source_transcription']), 20)
            self.assertIn('half twist squared', state['source_transcription'][6]['description'].lower())
            lab.mutate(dict(op='move', index=0, target=1, revision=0))
            self.assertEqual(exact_action(product(lab.history[-1])), expected)
            lab.mutate(dict(op='split', index=0, kind='powers', revision=1))
            self.assertEqual(len(lab.history[-1]), 21)
            lab.mutate(dict(op='combine', index=0, revision=2))
            self.assertEqual(len(lab.history[-1]), 20)
            document = json.loads(json.dumps(lab.session_document()))
            history, frames, _, position, limited = validated_session_document(document, '10-10')
            self.assertEqual(exact_action(product(history[position])), expected)
            self.assertEqual(limited, [])
            with self.assertRaisesRegex(ValueError, 'different factorization lab'):
                validated_session_document(document)
            wrong = json.loads(json.dumps(export_factors(TEN_TEN_FACTORS, '10-10')))
            wrong['factors'][0]['power'] = 1
            wrong['factors'][0].pop('word')
            with self.assertRaisesRegex(ValueError, 'disk action'):
                lab.mutate(dict(op='import', document=wrong, revision=3))
            lab.mutate(dict(op='conjugate', word=[1], revision=3))
            self.assertEqual(exact_action(product(lab.history[-1])),
                             exact_action((1,) + product(TEN_TEN_FACTORS) + inverse_word((1,))))
        finally:
            lab.server_close()

    def test_browser_adapter_restores_a_separate_transcription_workspace(self):
        adapter = runpy.run_path(str(ASSETS / 'public-lab-backend.py'))
        adapter['select_lab_seed']('10-10')
        reply = json.loads(adapter['dispatch']('/api/action', 'POST', json.dumps(
            dict(op='move', index=0, target=1, revision=0))))
        self.assertEqual(reply['status'], 200)
        self.assertEqual(reply['session']['seed'], '10-10')
        fresh = runpy.run_path(str(ASSETS / 'public-lab-backend.py'))
        fresh['select_lab_seed']('10-10')
        fresh['restore_browser_session'](json.dumps(reply['session']))
        self.assertEqual(fresh['lab'].position, 1)
        self.assertEqual(fresh['lab'].history[-1], adapter['lab'].history[-1])
        other = runpy.run_path(str(ASSETS / 'public-lab-backend.py'))
        other['select_lab_seed']('4-3')
        other['restore_browser_session'](json.dumps(reply['session']))
        self.assertEqual(other['lab'].position, 0)
        self.assertEqual(other['lab'].seed_slug, '4-3')

    def test_file_session_remains_seed_bound(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / 'ten-ten-session.json'
            lab = LabServer(seed_slug='10-10', session_path=path)
            try:
                lab.mutate(dict(op='move', index=0, target=1, revision=0))
            finally:
                lab.server_close()
            reopened = LabServer(seed_slug='10-10', session_path=path)
            try:
                self.assertEqual(reopened.position, 1)
                self.assertEqual(reopened.history[-1], lab.history[-1])
            finally:
                reopened.server_close()
            with self.assertRaisesRegex(ValueError, 'different factorization lab'):
                LabServer(session_path=path)


if __name__ == '__main__':
    unittest.main()
