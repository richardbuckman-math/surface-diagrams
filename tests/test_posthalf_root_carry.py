import json
from dataclasses import asdict
from pathlib import Path
import unittest
from examples.analyze_posthalf_root_carry import report
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
ROOT=Path(__file__).resolve().parents[1]

class RootCarryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()

    def test_complete_source_exact_root_carry_and_local_scores(self):
        r=self.r;q=r['route']
        self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['named_substitutions']),(11,12,4))
        self.assertEqual(r['chosen_peak'],dict(max_support_word=6,total_support_word=40,braid_letters=108))
        self.assertEqual(q['stages'][8]['score'],dict(max_support_word=5,total_support_word=29,braid_letters=92))
        self.assertEqual((r['posthalf_combined_operations'],r['posthalf_combined_external_checks'],r['research_prefix_operations_at_four_exteriors'],r['complete_source_plan_operations']),(68,50,111,113))
        self.assertEqual(q['stages'][0]['factors'],r['source_factors'])
        self.assertTrue(q['root_stayed_literal_during_carry']);self.assertTrue(q['restored_three_records_literal'])
        self.assertEqual(q['actual_restored_outputs'],q['actual_consolidated_inputs'])
        self.assertEqual(len(q['shared_source_late_ids']),7)
        self.assertTrue(r['full_ordered_parent_match']['equal']);self.assertNotEqual(r['full_ordered_parent_raw_discrepancy'],())

    def test_scoped_failed_target_and_finite_actual_outside_probes(self):
        r=self.r;f=r['initial_short15_order_failure']
        self.assertEqual(len(f['exact_integral_commutators']),4)
        self.assertTrue(all(x['left']!=x['right'] for x in f['exact_integral_commutators']))
        self.assertTrue(all(not x['comparison']['equal'] for x in f['faithful_B5_product_input_comparisons']))
        self.assertFalse(f['applied'])
        self.assertEqual([x['support_length'] for x in r['necessary35_probes']],[10,4,12,2])
        self.assertEqual([x['comparison']['equal'] for x in r['necessary35_probes']],[False,False,False,True])
        self.assertTrue(all(not x['unit_block_transport_applied'] for x in r['necessary35_probes']))
        self.assertTrue(all(x['exact_disk_equal'] for x in r['positive_full_product_effect_matches']))

    def test_every_raw_move_named_rule_and_full_kernel_reconstruction(self):
        q=self.r['route']
        self.assertTrue(all(p['bounded'] for p in q['preapplication_previews']))
        for x in q['actual_adjacent_certificates']:
            self.assertEqual(x['raw_move']['disk_word_certificate']['discrepancy'],())
            self.assertTrue(all(m['exact_disk_equal'] for m in x['individual_presentations']))
        named=[s for s in q['stages'] if 'named_pattern_witness' in s];self.assertEqual(len(named),4)
        for s in named:
            w=s['named_pattern_witness']
            self.assertTrue(all(m['exact_disk_equal'] for m in w['individual_matches']+w['individual_output_matches']))
            self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
            self.assertEqual(len(s['framed_balance_before_minus_after']),5)
            self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
            for x in w['complete_actual_and_normalized_point_pushing']:
                self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
        for c in q['state_sphere_lift_certificates']:
            self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
            self.assertLessEqual(c['score']['max_support_word'],6)

    def test_actual_final_chart_and_unchanged_terminal_fourth_power_cap(self):
        r=self.r;chosen=[x for x in r['derived_final_chart_order_comparisons'] if x['chosen']]
        self.assertEqual(len(chosen),1);self.assertTrue(all(x['equal'] for x in chosen[0]['individual_comparisons']))
        self.assertEqual(r['final_chart_G_then_sigma4'],r['final_chart_source_G']+(4,))
        self.assertEqual((r['new_late_closed_matrix']['total'],r['new_late_closed_matrix']['maximum']),(20,2))
        q=r['route'];p=r['terminal_plan'];self.assertEqual(len(q['factors']),4)
        minus=tuple(tuple(-x for x in row) for row in IDENTITY)
        self.assertTrue(all((f.points,f.power,f.half)==(5,1,False) and homology_action(f.word)==minus for f in q['factors']))
        self.assertTrue(all(x['only_id_changed'] for x in p['id_only_alignment']))
        self.assertEqual(p['combine']['raw_free_word_discrepancy'],())
        self.assertEqual(p['full_cap_discrepancy_word'],p['combine']['local_after'][0].word)
        self.assertFalse(p['combine_applied']);self.assertFalse(p['cap_applied'])

    def test_saved_root_carry_report_reproduces(self):
        saved=json.loads((ROOT/'docs/proofs/six-seven-posthalf-root-carry.json').read_bytes())
        self.assertEqual(saved,json.loads(json.dumps(self.r,default=asdict)))
if __name__=='__main__':unittest.main()
