import json
from pathlib import Path
from dataclasses import replace
import unittest
from surface_diagrams.early_alternative_exterior import expose_second_alternative_exterior
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.hyperelliptic_homology import homology_action, IDENTITY
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.disk_intersection import disk_curve_intersection


class AlternativeExteriorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks'
        cls.saved = json.loads((cls.folder / 'certificate.json').read_text(encoding='utf-8'))
        cls.source = tuple(Factor(**dict(x, conjugator=tuple(x['conjugator']))) for x in cls.saved['early_alternative_transport']['factors'])
        cls.route = expose_second_alternative_exterior(cls.source)

    def test_every_retained_state_is_positive_bounded_and_disk_lift_exact(self):
        r = self.route
        self.assertEqual((r['graphical_steps'], r['adjacent_checks'], r['combined_research_steps']), (8, 6, 59))
        expected = exact_action(BOUNDARY_WORD * 4, 5)
        peak = 0
        for s in r['stages']:
            for a in (s,) + s.get('atomic_steps', ()):
                fs = a['factors']
                self.assertEqual(exact_action(product(fs), 5), expected)
                self.assertEqual(homology_action(product(fs)), IDENTITY)
                self.assertTrue(all(not f.half and f.power > 0 for f in fs))
                peak = max(peak, max(len(supported_class(f.mapping_class, 5)) for f in fs))
                self.assertNotIn('sphere', a.get('kind', ''))
        self.assertEqual((peak, r['actual_peak_support_word']), (16, 16))
        self.assertEqual(r['sphere_move_count'], 0)

    def test_each_move_retains_order_and_both_cyclic_conjugations(self):
        r = self.route
        self.assertEqual(sum(s['kind'] == 'disk_cyclic_start' for s in r['stages']), 2)
        self.assertEqual(r['stages'][1]['frame'], (2, 3, 4, -2, -1))
        for s in r['stages']:
            if 'local_before' not in s: continue
            before, after = product(s['local_before']), product(s['local_after'])
            if s['kind'] in ('disk_cyclic_start', 'global_conjugation'):
                g = s['frame']; before = g + before + inverse_word(g)
            self.assertEqual(exact_action(before, 5), exact_action(after, 5))
        a, b, c = r['stages'][-1]['local_before']
        self.assertNotEqual(exact_action(product((b, a, c)), 5), exact_action(product(r['stages'][-1]['local_after']), 5))

    def test_nonabelian_chart_and_every_actual_input_match_are_retained(self):
        w = self.route['stages'][-1]['named_pattern_witness']
        self.assertEqual(w['normalized_y_split'].kernel_loop, (-4, -3, 1, 2, 3, 4))
        self.assertEqual(w['canonical_y_split'].kernel_loop, (1, 2))
        self.assertEqual(w['transported_y_split'].kernel_loop, w['normalized_y_split'].kernel_loop)
        self.assertEqual(exact_action(w['transported_y_split'].shadow_word, 4), exact_action(w['normalized_y_split'].shadow_word, 4))
        self.assertEqual(exact_action(product(w['canonical']), 5), exact_action(product(w['canonical_after']), 5))
        for c in w['individual_matches'] + w['presentation_matches'] + w['donor_target_match']:
            self.assertTrue(c['exact_disk_equal'])
            self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))
        # Equal kernel exponent counts would be insufficient; the complete
        # retained conjugated word is used in the joint disk chart.
        self.assertNotEqual(w['normalized_y_split'].kernel_loop, (1, 2))

    def test_signed_framing_balances_and_both_visible_exteriors_are_kept(self):
        r = self.route
        for s in r['stages']:
            if s['kind'] not in ('disk_pc_daisy', 'disk_cluster_lantern'): continue
            before, after = s['local_before'], s['local_after']
            expected = tuple(sum(f.power for f in before if i in enclosed_boundaries(f.mapping_class, 5)) - sum(f.power for f in after if i in enclosed_boundaries(f.mapping_class, 5)) for i in range(1, 6))
            self.assertEqual(s['framed_balance_before_minus_after'], expected)
        exteriors = tuple(f for f in r['factors'] if f.points == 5)
        self.assertEqual(len(exteriors), 2)
        self.assertTrue(all(f.power == 1 for f in exteriors))
        self.assertNotEqual(homology_action(exteriors[0].word), IDENTITY)
        self.assertEqual(homology_action(product(exteriors)), IDENTITY)
        self.assertEqual(r['exterior_caps'], 0)
        remaining = tuple(f for f in r['factors'] if f.points != 5)
        self.assertEqual(len(remaining), 14)
        self.assertEqual(exact_action(product(remaining), 5), exact_action(BOUNDARY_WORD * 2, 5))

    def test_endpoint_metrics_and_research_scope_are_honest(self):
        r = self.route
        self.assertEqual(r['after_score'], dict(max_support_word=16, total_support_word=98, braid_letters=164))
        self.assertEqual([sum(f.points == n for f in r['factors']) for n in (2, 3, 4, 5)], [13, 0, 1, 2])
        fs = r['factors'];counts = [disk_curve_intersection(a.mapping_class, b.mapping_class, strands=5) for i, a in enumerate(fs) for b in fs[i + 1:]]
        self.assertEqual((max(counts), sum(counts)), (36, 472))
        self.assertFalse(r['replacement_for_full_proof'])
        self.assertEqual(self.saved['named_full_route']['summary']['graphical_steps'], 89)

    def test_public_display_is_disk_exact_and_wrong_sources_are_rejected(self):
        d = json.loads((self.folder / 'display-pure.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['routes']['earlyaltexterior']), 9)
        for actual, shown in zip(self.route['stages'], d['routes']['earlyaltexterior']):
            for f, i in zip(actual['factors'], shown['factors']):
                self.assertFalse(d['rows'][i]['sphere_rechart'])
                self.assertEqual(exact_action(f.word, 5), exact_action(d['rows'][i]['word'], 5))
        for wrong in (self.source[:-1], (replace(self.source[0], power=2),) + self.source[1:]):
            with self.assertRaises(ValueError): expose_second_alternative_exterior(wrong)


if __name__ == '__main__': unittest.main()