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
        self.assertEqual((r['graphical_steps'], r['adjacent_checks'], r['first_pair_step'], r['all_pure_step']), (51, 83, 17, 29))
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
        last = self.route['stages'][self.route['shared_petal_step']]
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
        exterior = next(f for f in self.route['factors'] if f.id == 'alternative.exterior')
        self.assertEqual(exterior, Factor('alternative.exterior', (), 1, 5))
        self.assertNotEqual(homology_action(exterior.word), homology_action(()))
        self.assertTrue(self.route['exterior_not_capped'])
        self.assertFalse(self.route['replacement_for_full_proof'])

    def test_public_research_route_is_disk_exact_and_full_proof_is_now_91_steps(self):
        d = json.loads((self.folder / 'display-pure.json').read_text(encoding='utf-8'))
        states = d['routes']['earlyalttransport']
        self.assertEqual(len(states), 52)
        for a, b in zip(self.route['stages'], states):
            self.assertEqual(a['kind'], b['kind'])
            for f, i in zip(a['factors'], b['factors']):
                self.assertFalse(d['rows'][i]['sphere_rechart'])
                self.assertEqual(exact_action(f.word, 5), exact_action(d['rows'][i]['word'], 5))
        self.assertEqual(self.public['named_full_route']['summary']['graphical_steps'], 85)
        self.assertEqual(len(d['routes']['namedfull']), 86)
        self.assertFalse(self.public['early_alternative_transport']['replacement_for_full_proof'])

    def test_new_residual_lantern_uses_its_actual_frame_and_reduces_curve_intersections(self):
        from surface_diagrams.disk_intersection import disk_curve_intersection
        r = self.route
        self.assertEqual(r['first_exterior_step'], 36)
        self.assertEqual(r['stages'][39]['score'], dict(max_support_word=12, total_support_word=90, braid_letters=182))
        self.assertEqual(len(r['stages'][39]['factors']), 15)
        witness = r['stages'][39]['named_pattern_witness']
        self.assertEqual(len(witness['individual_matches']), 3)
        for c in witness['presentation_matches']:
            self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))
        for stage, expected in [(r['stages'][36], (74, 1536)), (r['stages'][39], (34, 672))]:
            fs = stage['factors']
            counts = [disk_curve_intersection(a.mapping_class, b.mapping_class, strands=5)
                      for i, a in enumerate(fs) for b in fs[i + 1:]]
            self.assertEqual((max(counts), sum(counts)), expected)
        # Same enclosed sets and necessary centralization did not justify
        # the discarded round B4 chart. Its actual 34 input is different.
        g = (-3, 1, 2, 2, 3)
        actual = r['stages'][39]['local_before'][1]
        self.assertNotEqual(exact_action(actual.word, 5), exact_action(Factor('wrong.round.chart', g, 3, 2).word, 5))

    def test_shared_petal_lantern_and_two_unwindings_reduce_the_actual_geometry(self):
        from surface_diagrams.disk_intersection import disk_curve_intersection
        r = self.route
        self.assertEqual((r['residual_lantern_step'], r['shared_petal_step']), (39, 43))
        w = r['stages'][43]['named_pattern_witness']
        self.assertEqual(w['canonical_cyclic_order'], 'Q S R')
        self.assertEqual(w['frame'], (-1, -4, -3, -2, 3, 4, -3))
        self.assertEqual(exact_action(product(w['canonical']), 5), exact_action(product(w['canonical_after']), 5))
        for c in w['individual_matches'] + w['presentation_matches']:
            self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))
        self.assertEqual([s.get('adjacent_moves', 0) for s in r['stages'][40:46]], [0, 2, 2, 0, 1, 4])
        self.assertEqual(r['stages'][45]['score'], dict(max_support_word=12, total_support_word=83, braid_letters=178))
        fs = r['stages'][45]['factors']
        self.assertEqual(len(fs), 16)
        self.assertEqual([sum(f.points == n for f in fs) for n in (2, 3, 4, 5)], [11, 2, 2, 1])
        root = next(f for f in fs if f.id == 'alternative.return.0')
        self.assertEqual(root, Factor('alternative.return.0', (1,), 2, 3))
        square = next(f for f in fs if f.id == 'alternative.T12.square')
        self.assertEqual(square, Factor('alternative.T12.square', (-4, -3, -2), 1, 2, 2))
        counts = [disk_curve_intersection(a.mapping_class, b.mapping_class, strands=5)
                  for i, a in enumerate(fs) for b in fs[i + 1:]]
        self.assertEqual((max(counts), sum(counts)), (30, 430))
        self.assertEqual(exact_action(product(fs[1:]), 5), exact_action(BOUNDARY_WORD * 3, 5))

    def test_inside_four_daisy_retains_its_common_frame_and_geometric_reduction(self):
        from surface_diagrams.disk_intersection import disk_curve_intersection
        r = self.route
        self.assertEqual((r['shared_unwinding_step'], r['inside_daisy_step']), (45, 50))
        self.assertEqual(r['stages'][46]['frame'], (3, 2))
        w = r['stages'][50]['named_pattern_witness']
        self.assertTrue(w['outer_preserved'])
        self.assertEqual(w['frame'], (3, 2, 1, 1, 2, 3))
        self.assertEqual([(m['source'], m['target']) for m in w['retained_interchanges']], [(3, 2), (2, 1)])
        for c in w['individual_matches']:
            self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))
        for m in w['retained_interchanges']:
            self.assertFalse(m['disk_word_certificate']['discrepancy'])
        self.assertEqual([s.get('adjacent_moves', 0) for s in r['stages'][46:]], [0, 0, 8, 1, 0, 8])
        retained = [x['factors'] for s in r['stages'][46:] for x in (s,) + s.get('atomic_steps', ())]
        self.assertEqual(max(len(supported_class(f.mapping_class, 5)) for fs in retained for f in fs), 18)
        self.assertEqual(r['after_score'], dict(max_support_word=12, total_support_word=86, braid_letters=192))
        fs = r['factors']
        self.assertEqual(len(fs), 13)
        self.assertEqual([sum(f.points == n for f in fs) for n in (2, 3, 4, 5)], [8, 1, 3, 1])
        self.assertEqual(fs[0], Factor('alternative.inside.D4', (), 1, 4))
        counts = [disk_curve_intersection(a.mapping_class, b.mapping_class, strands=5)
                  for i, a in enumerate(fs) for b in fs[i + 1:]]
        self.assertEqual((max(counts), sum(counts)), (10, 160))
        self.assertEqual(exact_action(product(tuple(f for f in fs if f.points != 5)), 5), exact_action(BOUNDARY_WORD * 3, 5))

    def test_next_shared_petal_targets_are_individually_exact_but_unapplied(self):
        w = self.route['next_daisy_targets']
        self.assertFalse(w['applied'])
        self.assertTrue(w['requires_transport'])
        self.assertEqual([enclosed_boundaries(f.mapping_class, 5) for f in w['outer_daisy']], [(2, 3, 4), (4, 5), (3, 5), (2, 5)])
        self.assertEqual([enclosed_boundaries(f.mapping_class, 5) for f in w['triple_daisy']], [(1, 3), (1, 5), (3, 5)])
        for key in ('shared_35_match', 'existing_45_match', 'existing_25_match', 'existing_15_unit_match'):
            for c in w[key]:
                self.assertEqual(exact_action(c['actual'].word, 5), exact_action(c['pattern'].word, 5))

    def test_wrong_source_is_rejected(self):
        with self.assertRaises(ValueError):
            transport_alternative_roots(self.source[:-1])
        with self.assertRaises(ValueError):
            transport_alternative_roots((replace(self.source[0], power=2),) + self.source[1:])


if __name__ == '__main__':
    unittest.main()
