import json
from dataclasses import replace
from pathlib import Path
import unittest
from unittest.mock import patch

from surface_diagrams.alternative_sphere_chart import fixed_point_chart_predictions, audit_alternative_point_four
from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action, VerificationLimitError
from surface_diagrams.puncture_boundary import BOUNDARY_WORD


class AlternativeSphereChartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        c = json.loads((cls.root / 'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
        cls.source = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator']))) for f in c['early_alternative_transport']['stages'][39]['factors'])
        cls.report = audit_alternative_point_four(cls.source)

    def test_incidence_selects_only_point4_but_is_not_a_relation_certificate(self):
        p = self.report['predictions']
        self.assertEqual(p['minimal_predicted_points'], (4,))
        self.assertEqual([c['predicted_normalized_power'] for c in p['candidates']], [5, 5, 4, 3, 5, 4])
        self.assertTrue(p['requires_exact_rechart'])
        simple = fixed_point_chart_predictions((Factor('boundary', (), 1, 5, 4),))
        self.assertEqual([c['predicted_normalized_power'] for c in simple['candidates']], [0, 0, 0, 0, 0, 4])
        for f, power in [(self.source, 3), (self.source, True), (self.source[:-1], 4),
                         ((replace(self.source[0], half=True),) + self.source[1:], 4)]:
            with self.assertRaises(ValueError): fixed_point_chart_predictions(f, boundary_power=power)

    def test_nine_corrections_are_visible_and_both_odd_pieces_have_negative_lift(self):
        r = self.report
        self.assertEqual((r['normalized_boundary_power'], r['boundary_correction_power'], r['corrected_boundary_power']), (3, 9, 12))
        boundary = Factor('alt4.boundary.corrections', (), 1, 5, 9)
        self.assertEqual(r['factors'][0], boundary)
        self.assertEqual(r['corrected_factors'][0], boundary)
        self.assertEqual(r['sphere_move']['explicit_boundary_corrections'], (boundary,))
        self.assertEqual(r['disk_move']['boundary_corrections_retained'], (boundary,))
        negative = homology_action(BOUNDARY_WORD)
        self.assertNotEqual(negative, IDENTITY)
        self.assertEqual(r['normalized_lift'], negative)
        self.assertEqual(r['correction_lift'], negative)
        self.assertEqual(homology_action(product(r['factors'])), IDENTITY)
        self.assertEqual(r['boundary_caps'], 0)

    def test_sphere_move_has_full_nonzero_disk_discrepancy_and_separate_positive_lift_check(self):
        r = self.report
        m = r['sphere_move']
        self.assertEqual(m['kind'], 'sphere_rechart')
        self.assertIn('SPHERE MOVE', m['title'])
        self.assertFalse(m['disk_equal'])
        self.assertEqual(m['disk_writhe_discrepancy'], -160)
        self.assertTrue(m['not_a_cap'])
        discrepancy = m['disk_discrepancy']
        self.assertEqual(homology_action(discrepancy), IDENTITY)
        self.assertTrue(m['sphere_certificate']['certified'])
        self.assertEqual(m['lift_homology'], IDENTITY)
        self.assertEqual(exact_action(product(m['factors']), 5), exact_action(BOUNDARY_WORD * 12, 5))
        # Dropping the nine explicit corrections would pass a sphere action
        # test, but it changes the chosen genus-two lift by -I.
        self.assertFalse(r['chart']['joint_rechart_preserves_lift'])
        self.assertNotEqual(r['chart']['joint_lift_homology'], IDENTITY)

    def test_old_visible_exterior_is_accounted_for_in_the_retained_corrections(self):
        r = self.report
        c = next(c for c in r['chart']['factor_certificates'] if c['id'] == 'alternative.exterior')
        self.assertIsNone(c['factor'])
        self.assertEqual(c['boundary_power'], 3)
        self.assertEqual(sum(c['boundary_power'] for c in r['chart']['factor_certificates']), 9)
        frame = r['global_frame']['frame']
        self.assertEqual(frame, (5, 4))
        self.assertEqual(exact_action(product(r['global_frame']['factors']), 6),
                         exact_action(frame + product(self.source) + inverse_word(frame), 6))

    def test_adjacent_lantern_has_individual_common_chart_and_disk_presentation_matches(self):
        r = self.report
        m = r['disk_move']
        w = m['named_pattern_witness']
        self.assertEqual(w['frame'], (-1, -1, 2, 1, 1, 2, 3, 3, 4))
        self.assertEqual(len(w['individual_matches']), 3)
        for c in w['individual_matches'] + w['presentation_matches']:
            self.assertTrue(c['exact_disk_equal'])
            self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))
        self.assertEqual(exact_action(product(m['local_before']), 5), exact_action(product(m['local_after']), 5))
        self.assertEqual(exact_action(product(w['canonical']), 5), exact_action(product(w['canonical_after']), 5))
        a, b, q = m['local_before']
        self.assertNotEqual(exact_action(product((b, a, q)), 5), exact_action(product(m['local_after']), 5))
        self.assertEqual(len(r['normalized_factors']), 13)
        self.assertEqual(r['normalized_score']['max_support_word'], 18)
        self.assertTrue(all(not f.half and f.power > 0 for f in r['factors']))

    def test_framed_lantern_balance_is_recorded_and_never_used_as_a_cap(self):
        m = self.report['disk_move']
        before, after = m['local_before'], m['local_after']
        balance = tuple(sum(i in enclosed_boundaries(f.mapping_class, 5) for f in before)
                        - sum(i in enclosed_boundaries(f.mapping_class, 5) for f in after) for i in range(1, 6))
        self.assertEqual(m['framed_balance_before_minus_after'], balance)
        self.assertFalse(self.report['applied_to_public_replay'])
        self.assertFalse(self.report['complete_named_derivation'])
        self.assertFalse(self.report['replacement_for_full_proof'])

    def test_uncertified_sphere_action_is_unknown_not_an_accepted_rechart(self):
        with patch('surface_diagrams.alternative_sphere_chart.sphere_chain_certificate', return_value={'certified': False}):
            with self.assertRaises(VerificationLimitError): audit_alternative_point_four(self.source)

    def test_saved_report_is_exact_and_separate_from_both_public_routes(self):
        saved = json.loads((self.root / 'docs/proofs/six-seven-alternative-sphere-chart.json').read_text(encoding='utf-8'))
        self.assertEqual(saved['boundary_correction_power'], 9)
        self.assertEqual(saved['sphere_move']['disk_writhe_discrepancy'], -160)
        self.assertFalse(saved['applied_to_public_replay'])
        c = json.loads((self.root / 'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
        self.assertEqual(c['named_full_route']['summary']['graphical_steps'], 106)
        self.assertEqual(c['early_alternative_transport']['graphical_steps'], 51)


if __name__ == '__main__': unittest.main()
