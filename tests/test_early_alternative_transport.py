import json
from dataclasses import replace
from pathlib import Path
import unittest

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.early_alternative_transport import transport_alternative_roots
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import homology_action
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.puncture_boundary import BOUNDARY_WORD


class AlternativeTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks'
        cls.public = json.loads((cls.folder / 'certificate.json').read_text(encoding='utf-8'))
        rows = cls.public['early_boundary']['chart']['factors']
        cls.source = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator']))) for f in rows)
        cls.route = transport_alternative_roots(cls.source)

    def test_every_reached_and_adjacent_state_is_positive_bounded_disk_and_lift_exact(self):
        r = self.route
        self.assertEqual((r['graphical_steps'], r['adjacent_checks'], r['first_pair_step'], r['all_pure_step']), (39, 57, 17, 29))
        expected = exact_action(BOUNDARY_WORD * 4, 5)
        lift = homology_action(BOUNDARY_WORD * 4)
        peak = 0
        for s in r['stages']:
            for record in (s,) + s.get('atomic_steps', ()):
                fs = record['factors']
                self.assertEqual(exact_action(product(fs), 5), expected)
                self.assertEqual(homology_action(product(fs)), lift)
                self.assertTrue(all(f.power > 0 for f in fs))
                self.assertLessEqual(sum(f.half for f in fs), 4)
                peak = max(peak, max(len(supported_class(f.mapping_class, 5)) for f in fs))
                self.assertNotIn('sphere', record.get('kind', ''))
        self.assertEqual(peak, 20)
        self.assertEqual(r['actual_peak_support_word'], peak)
        self.assertEqual((r['half_twists_remaining'], r['half_twists_introduced'], r['sphere_move_count']), (0, 0, 0))

    def test_each_local_move_and_explicit_frame_retains_its_exact_order(self):
        for s in self.route['stages']:
            if 'local_before' not in s:
                continue
            before, after = product(s['local_before']), product(s['local_after'])
            if s['kind'] in ('disk_cyclic_start', 'global_conjugation'):
                g = s['frame']
                before = g + before + inverse_word(g)
            self.assertEqual(exact_action(before, 5), exact_action(after, 5))
        last = self.route['stages'][-1]
        a, b, c = last['local_before']
        self.assertNotEqual(exact_action(product((b, a, c)), 5), exact_action(product(last['local_after']), 5))

    def test_transported_daisy_retains_two_internal_interchanges_and_every_actual_match(self):
        s = next(s for s in self.route['stages'] if 'retained_interchanges' in s.get('named_pattern_witness', {}))
        w = s['named_pattern_witness']
        self.assertTrue(w['outer_preserved'])
        self.assertEqual(w['cyclic_offset'], 2)
        self.assertEqual([(m['source'], m['target']) for m in w['retained_interchanges']], [(3, 2), (2, 1)])
        self.assertEqual(len(w['individual_matches']), 4)
        for m in w['retained_interchanges']:
            self.assertFalse(m['disk_word_certificate']['discrepancy'])
        for c in w['individual_matches']:
            self.assertTrue(c['exact_disk_equal'])
            self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))
        for s in self.route['stages']:
            for c in s.get('named_pattern_witness', {}).get('individual_matches', ()):
                self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))

    def test_borrowed_petals_recover_the_round_square_before_the_last_match(self):
        r = self.route
        restored = next(s for s in r['stages'] if s['title'].startswith('Close the original daisy'))
        square = next(f for f in restored['factors'] if f.id == 'alternative.T12.square')
        self.assertEqual(square, Factor('alternative.T12.square', (), 1, 2, 2))
        for key in ('first_half_match', 'second_half_match'):
            a, b = r[key][0]['actual'], r[key][0]['pattern']
            self.assertTrue(a.half and b.half)
            self.assertEqual(exact_action(a.word, 5), exact_action(b.word, 5))
        self.assertEqual(len(r['all_pure_factors']), 16)
        self.assertTrue(all(not f.half for f in r['all_pure_factors']))
        self.assertEqual(r['all_pure_factors'][0], Factor('alternative.O1234', (), 1, 4))

    def test_framed_balances_keep_powers_and_exterior_is_not_capped(self):
        for s in self.route['stages']:
            if s['kind'] not in ('disk_pc_daisy', 'disk_cluster_lantern'):
                continue
            sets = [[(f.power, enclosed_boundaries(f.mapping_class, 5)) for f in s[k]] for k in ('local_before', 'local_after')]
            expected = tuple(sum(p for p, b in sets[0] if i in b) - sum(p for p, b in sets[1] if i in b) for i in range(1, 6))
            self.assertEqual(s['framed_balance_before_minus_after'], expected)
        exterior = self.route['factors'][0]
        self.assertEqual(exterior, Factor('alternative.exterior', (), 1, 5))
        self.assertNotEqual(homology_action(exterior.word), homology_action(()))
        self.assertTrue(self.route['exterior_not_capped'])
        self.assertFalse(self.route['replacement_for_full_proof'])

    def test_public_research_route_is_disk_exact_and_full_proof_is_still_106_steps(self):
        d = json.loads((self.folder / 'display-pure.json').read_text(encoding='utf-8'))
        states = d['routes']['earlyalttransport']
        self.assertEqual(len(states), 40)
        for a, b in zip(self.route['stages'], states):
            self.assertEqual(a['kind'], b['kind'])
            for f, i in zip(a['factors'], b['factors']):
                self.assertFalse(d['rows'][i]['sphere_rechart'])
                self.assertEqual(exact_action(f.word, 5), exact_action(d['rows'][i]['word'], 5))
        self.assertEqual(self.public['named_full_route']['summary']['graphical_steps'], 106)
        self.assertEqual(len(d['routes']['namedfull']), 107)
        self.assertFalse(self.public['early_alternative_transport']['replacement_for_full_proof'])

    def test_new_residual_lantern_uses_its_actual_frame_and_reduces_curve_intersections(self):
        from surface_diagrams.disk_intersection import disk_curve_intersection
        r = self.route
        self.assertEqual(r['first_exterior_step'], 36)
        self.assertEqual(r['after_score'], dict(max_support_word=12, total_support_word=90, braid_letters=182))
        self.assertEqual(len(r['factors']), 15)
        witness = r['stages'][-1]['named_pattern_witness']
        self.assertEqual(len(witness['individual_matches']), 3)
        for c in witness['presentation_matches']:
            self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))
        for stage, expected in [(r['stages'][36], (74, 1536)), (r['stages'][-1], (34, 672))]:
            fs = stage['factors']
            counts = [disk_curve_intersection(a.mapping_class, b.mapping_class, strands=5)
                      for i, a in enumerate(fs) for b in fs[i + 1:]]
            self.assertEqual((max(counts), sum(counts)), expected)
        # Same enclosed sets and necessary centralization did not justify
        # the discarded round B4 chart. Its actual 34 input is different.
        g = (-3, 1, 2, 2, 3)
        actual = r['stages'][-1]['local_before'][1]
        self.assertNotEqual(exact_action(actual.word, 5), exact_action(Factor('wrong.round.chart', g, 3, 2).word, 5))

    def test_wrong_source_is_rejected(self):
        with self.assertRaises(ValueError):
            transport_alternative_roots(self.source[:-1])
        with self.assertRaises(ValueError):
            transport_alternative_roots((replace(self.source[0], power=2),) + self.source[1:])


if __name__ == '__main__':
    unittest.main()
