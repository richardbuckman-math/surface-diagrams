import json
from dataclasses import asdict
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_hybrid_rose import report
from examples.build_posthalf_hybrid_rose_comparison import pictures, picture
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action
ROOT = Path(__file__).resolve().parents[1]


class PosthalfHybridRoseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = report()

    def test_nine_move_third_checkpoint_and_five_actual_named_substitutions(self):
        q = self.r['third_exterior_route']
        self.assertEqual((q['graphical_operations'], q['adjacent_checks'], q['named_substitutions']), (9, 6, 5))
        self.assertEqual((len(q['factors']), q['after_score']['max_support_word'], q['after_score']['total_support_word'], q['after_score']['braid_letters']), (11, 6, 40, 108))
        self.assertEqual(q['peak_support_word'], 7)
        self.assertTrue(all(sum(f.points == 5 for f in s['factors']) == 2 for s in q['stages'][:-1]))
        self.assertEqual(len(self.r['three_visible_exteriors']), 3)
        self.assertEqual((self.r['third_closed_matrix']['total'], self.r['third_closed_matrix']['maximum']), (62, 6))

    def test_consumed_old_petals_and_distinct_first_donor_leftovers(self):
        r = self.r
        source = {f.id: f for f in r['source_factors']}
        after = {f.id: f for f in r['third_exterior_route']['factors']}
        self.assertEqual(len(r['shared_source_third_ids']), 6)
        self.assertTrue(all(source[n] == after[n] for n in r['shared_source_third_ids']))
        for n in ('outer.loan.1', 'outer.loan.2', 'reflected.inner125', 'hybrid.second.1', 'hybrid.second.2'):
            self.assertNotIn(n, after)
        for old, new in (('outer.loan.1', 'hybrid.first.1'), ('outer.loan.2', 'hybrid.first.2')):
            self.assertNotEqual(source[old].id, after[new].id)
            self.assertEqual(exact_action(source[old].word, 5), exact_action(after[new].word, 5))
        self.assertIn('hybrid.second.0', after)

    def test_all_raw_adjacent_moves_and_cyclic_words_precede_presentations(self):
        for q in (self.r['third_exterior_route'], self.r['closure_route']):
            self.assertTrue(all(p['bounded'] for p in q['preapplication_previews']))
            for x in q['actual_adjacent_certificates']:
                self.assertEqual(x['raw_move']['disk_word_certificate']['discrepancy'], ())
                self.assertTrue(all(m['exact_disk_equal'] for m in x['individual_presentations']))
            for s in q['stages']:
                if s['kind'] == 'disk_cyclic_start':
                    self.assertEqual(s['raw_cyclic_discrepancy'], ())
            for x in q['state_sphere_lift_certificates']:
                self.assertTrue(x['sphere_certificate']['certified'])
                self.assertEqual(x['chosen_lift'], IDENTITY)
                self.assertLessEqual(x['score']['max_support_word'], 20)

    def test_seven_full_named_rules_keep_balances_inputs_outputs_and_kernels(self):
        stages = [s for q in (self.r['third_exterior_route'], self.r['closure_route'])
                  for s in q['stages'] if 'named_pattern_witness' in s]
        self.assertEqual(len(stages), 7)
        for s in stages:
            w = s['named_pattern_witness']
            self.assertEqual(len(s['framed_balance_before_minus_after']), 5)
            self.assertTrue(all(m['exact_disk_equal'] for m in w['individual_matches'] + w['individual_output_matches']))
            self.assertEqual(exact_action(product(s['local_before']), 5), exact_action(product(s['local_after']), 5))
            self.assertTrue(w['sphere_certificate']['certified'])
            self.assertEqual(w['chosen_lift_discrepancy'], IDENTITY)
            for x in w['complete_actual_and_normalized_point_pushing']:
                self.assertEqual(exact_action(x['actual'].word, 5), exact_action(x['split'].reconstructed_word, 5))

    def test_longer_named_closure_and_literal_four_unit_terminal_join(self):
        r = self.r
        q = r['closure_route']
        self.assertEqual((q['graphical_operations'], q['adjacent_checks']), (16, 15))
        self.assertEqual(q['peak_support_word'], 18)
        self.assertEqual(q['stages'][14]['score']['max_support_word'], 12)
        self.assertEqual(tuple(r['third_exterior_route']['factors']), tuple(q['stages'][0]['factors']))
        self.assertTrue(r['complete_named_join_reached'])
        self.assertEqual((r['new_source_operations'], r['new_external_adjacent_checks'], r['complete_source_plan_operations']), (25, 21, 118))
        minus = tuple(tuple(-v for v in row) for row in IDENTITY)
        self.assertEqual(len(q['factors']), 4)
        for f in q['factors']:
            self.assertEqual((f.points, f.power, f.half), (5, 1, False))
            self.assertEqual(homology_action(f.word), minus)
        p = r['terminal_plan']
        self.assertTrue(all(x['only_id_changed'] for x in p['id_only_alignment']))
        self.assertEqual(p['combine']['raw_free_word_discrepancy'], ())
        self.assertFalse(p['combine_applied'])
        self.assertFalse(p['cap_applied'])
        self.assertEqual(tuple(p['full_cap_discrepancy_word']), p['combine']['local_after'][0].word)
        self.assertFalse(r['adopted'])
        self.assertFalse(r['public_replay_changed'])

    def test_saved_report_and_six_source_exact_unnumbered_panels(self):
        saved, items = pictures()
        self.assertEqual(saved, json.loads(json.dumps(self.r, default=asdict)))
        counts, rows = [], []
        for name, title, s in items:
            svg = picture(s, title)
            self.assertEqual(svg, (ROOT / 'docs/proofs/posthalf-hybrid-rose-comparison' / (name + '.svg')).read_text(encoding='utf-8'))
            doc = ET.fromstring(svg)
            points = [n for n in doc.iter() if n.get('class') == 'marked-point']
            counts.append(len(points))
            self.assertFalse(any(n.get('class') == 'marked-point-label' for n in doc.iter()))
            d = {}
            for row in doc:
                if row.get('data-factor'):
                    v = next(n for n in row if n.tag.endswith('svg'))
                    scale = float(v.get('width')) / float(v.get('viewBox').split()[2])
                    dots = [n for n in v.iter() if n.get('class') == 'marked-point']
                    for dot in dots:
                        self.assertAlmostEqual(float(dot.get('r')) * scale, 1.68)
                    xs = sorted(float(n.get('cx')) for n in dots)
                    for left, right in zip(xs, xs[1:]):
                        self.assertAlmostEqual((right - left) * scale, 24.0)
                    d[row.get('data-factor')] = (v.get('viewBox'), v.get('width'), v.get('height'), tuple(ET.tostring(x) for x in v))
            rows.append(d)
        self.assertEqual(counts, [78, 72, 66, 66, 48, 24])
        shared = set(rows[0]) & set(rows[3])
        self.assertEqual(len(shared), 6)
        self.assertTrue(all(rows[0][n] == rows[3][n] for n in shared))


if __name__ == '__main__':
    unittest.main()
