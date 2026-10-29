import json
from dataclasses import asdict
from pathlib import Path
import unittest

from examples.analyze_posthalf_hybrid_block import report
from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY
from surface_diagrams.mapping_classes import exact_action


class PosthalfHybridBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = report()

    def test_full_ordered_product_has_exact_inverse_match_and_scoped_positive_miss(self):
        probes = self.r['preliminary_sign_comparisons']
        self.assertEqual(tuple(x['sign'] for x in probes), (-1, 1))
        self.assertTrue(probes[0]['exact_match']['equal'])
        self.assertFalse(probes[1]['exact_match']['equal'])
        self.assertEqual(tuple(x['support_length'] for x in probes), (6, 8))
        self.assertTrue(all(not x['applied'] for x in probes))
        self.assertTrue(self.r['full_ordered_block_fixes_needed15']['equal'])

    def test_complete_bounded_candidate_retains_raw_frames_and_all_context(self):
        c = self.r['bounded_candidate']
        self.assertEqual((c['graphical_operations'], c['adjacent_checks']), (17, 15))
        self.assertEqual(c['peak_support_word'], 18)
        self.assertFalse(c['selected'])
        self.assertFalse(c['applied_to_selected_research_source'])
        before = {f.id: f for f in self.r['source_factors']}
        after = {f.id: f for f in c['factors']}
        changed = {n for n in before if before[n] != after[n]}
        self.assertEqual(changed, {'outer.loan.2', 'cyclic135.supply.2',
                                   'reflected.inner125', 'reflected.output.1'})
        for actor in c['actual_ordered_actors']:
            self.assertEqual(after[actor.id], actor)
        for name in ('posthalf.exterior', 'reflected.exterior', 'upper.O1234'):
            self.assertEqual(after[name], before[name])
        for stage in c['stages']:
            if stage['kind'] == 'disk_cyclic_start':
                self.assertEqual(stage['raw_cyclic_discrepancy'], ())
        for x in c['actual_adjacent_certificates']:
            self.assertEqual(x['raw_move']['disk_word_certificate']['discrepancy'], ())
            self.assertTrue(all(m['exact_disk_equal'] for m in x['individual_presentations']))
        self.assertEqual(exact_action(product(c['factors']), 5),
                         exact_action(product(self.r['source_factors']), 5))

    def test_hypothetical_supplier_and_followup_failures_are_not_reached_moves(self):
        r = self.r
        s = r['hypothetical_named15_supplier']
        self.assertFalse(s['applied'])
        self.assertEqual(s['chosen_lift'], IDENTITY)
        self.assertTrue(s['sphere_certificate']['certified'])
        self.assertEqual(s['signed_pc_balance'], (-1, -1, 0, 0, -1))
        self.assertEqual(exact_action(s['actual_parent'].word, 5),
                         exact_action(product(s['target_outputs']), 5))
        for x in r['hypothetical_followup_order_failures']:
            self.assertFalse(x['applied'])
            self.assertTrue(all(w['left'] != w['right'] for w in x['exact_integral_commutators']))
        self.assertFalse(r['UP_predicted25_vs_needed_last25']['equal'])
        self.assertEqual(tuple(x['support_length'] for x in r['hypothetical_changed_old15_repair_misses']), (62, 66))
        self.assertTrue(all(not x['exact_match']['equal'] for x in r['hypothetical_changed_old15_repair_misses']))
        self.assertEqual((r['selected_source_moves'], r['preferred_moves'], r['preferred_steps']), (0, 101, 71))
        self.assertFalse(r['adopted'])
        self.assertFalse(r['public_replay_changed'])

    def test_full_kernels_closed_counts_and_saved_report_reproduce(self):
        r = self.r
        records = list(r['bounded_candidate']['endpoint_point_pushing'])
        records += list(r['hypothetical_named15_supplier']['full_point_pushing'])
        for p in r['preliminary_sign_comparisons'] + r['hypothetical_followup_order_failures'] + r['hypothetical_changed_old15_repair_misses']:
            records += list(p['full_point_pushing'])
        for x in records:
            self.assertEqual(exact_action(x['actual'].word, 5),
                             exact_action(x['split'].reconstructed_word, 5))
        self.assertEqual((r['before_closed_matrix']['total'], r['after_candidate_closed_matrix']['total']), (170, 194))
        self.assertEqual((sum(x['delta'] > 0 for x in r['changed_closed_pairs']),
                          sum(x['delta'] < 0 for x in r['changed_closed_pairs'])), (8, 5))
        path = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-posthalf-hybrid-block.json'
        self.assertEqual(json.loads(path.read_bytes()), json.loads(json.dumps(r, default=asdict)))


if __name__ == '__main__':
    unittest.main()
