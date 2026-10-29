import json,unittest
from dataclasses import asdict
from pathlib import Path
from examples.analyze_posthalf_lantern_targets import report
from examples.analyze_posthalf_petal import multiply
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY
from surface_diagrams.named_two_pair_cabled import two_pair_cabled_lantern


class PosthalfLanternTargetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_generic_identity_retains_named_daisies_cyclic_frames_and_both_commutations(self):
        for chart in ((),(-3,-4,-3,-2),(1,-2,3)):
            q=two_pair_cabled_lantern(chart=chart);self.assertEqual(q['cluster_sizes'],(2,2,1));self.assertEqual(exact_action(product(q['inputs']),5),exact_action(product(q['outputs']),5));self.assertEqual(q['internal_adjacent_checks'],2)
            for checks in q['shared_petal_matches']:self.assertTrue(all(x['exact_disk_equal'] for x in checks))
            for c in q['internal_cyclic_certificates']:self.assertFalse(c['raw_cyclic_discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in c['independently_known_output_invariance']));self.assertEqual(exact_action(product(c['before']),5),exact_action(product(c['after']),5))
            for m in q['retained_internal_adjacent_moves']:self.assertFalse(m['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in m['individual_commutation_matches']))
            self.assertTrue(all(x['exact_disk_equal'] for x in q['final_individual_daisy_matches']));self.assertTrue(q['sphere_certificate']['certified']);self.assertEqual(q['chosen_lift_discrepancy'],IDENTITY);self.assertFalse(q['applied_to_replay'])
            for p in q['complete_point_pushing']:self.assertEqual(exact_action(p['actual'].word,5),exact_action(p['split'].reconstructed_word,5))
    def test_invalid_chart_letters_are_rejected_before_a_target_is_constructed(self):
        for chart in ((0,),(5,),(-5,),(True,),('1',)):
            with self.assertRaises(ValueError):two_pair_cabled_lantern(chart=chart)
    def test_actual_two_input_chart_has_full_source_and_new_normalizations(self):
        t=self.r['two_pair_lantern_target'];self.assertEqual(t['source_outer_chart'],(-3,-4));self.assertEqual(t['inside_outer_rechart'],(-3,-2));self.assertEqual(t['common_chart'],(-3,-4,-3,-2));self.assertTrue(all(x['exact_disk_equal'] for x in t['individual_source_matches']));self.assertFalse(t['existing_root_matches']);self.assertTrue(all(not x['matches'] for x in t['existing_petal_matches']));self.assertFalse(t['applied'])
        self.assertEqual(t['pattern']['signed_pc_balance'],(0,0,1,0,0));s=t['source_normalized234_split'];self.assertEqual(s.kernel_loop,(-4,2,3,4));self.assertEqual(s.shadow_word,(2,2));self.assertEqual(exact_action(t['source_normalized234'].word,5),exact_action(s.reconstructed_word,5))
        for f,p in zip(t['new_normalized_actual_inputs'],t['new_normalized_splits']):self.assertEqual(exact_action(f.word,5),exact_action(p.reconstructed_word,5))
        self.assertEqual([x['certificate']['intersection_number'] for x in t['actual_pair_root_intersections']],[4,4,4,8])
    def test_new_triangle_exclusion_keeps_exact_integer_nonzero_witnesses_and_scope(self):
        t=self.r['new15_triangle'];self.assertEqual(len(t['orders']),6);self.assertEqual([x['certificate']['intersection_number'] for x in t['closed_pairs']],[14,2,10]);self.assertFalse(t['gathered'])
        for o in t['orders']:
            self.assertTrue(any(not w['commutes'] for w in o['noncentrality_witnesses']))
            for w in o['noncentrality_witnesses']:self.assertEqual(w['left'],multiply(w['product_lift'],w['input_lift']));self.assertEqual(w['right'],multiply(w['input_lift'],w['product_lift']));self.assertEqual(w['commutes'],w['left']==w['right'])
        self.assertIn('UNIT-factor',t['scope']);self.assertIn('Outside changes',t['scope'])
    def test_exact13_supplier_and_reused35_certificate_stay_unapplied(self):
        q=self.r['exact13_supplier'];self.assertFalse(q['applied']);self.assertEqual(q['internal_frame'],(-2,-2));self.assertFalse(q['normalized_split5'].kernel_loop);self.assertFalse(q['normalized_split4'].kernel_loop);self.assertEqual(q['normalized_split4'].shadow_word,(-2,1,1,2));self.assertEqual(q['simplified_normalized_required13'].conjugator,(-2,));self.assertTrue(all(x['exact_disk_equal'] for x in q['parent_match']+q['exact_required13_match']));self.assertTrue(q['sphere_certificate']['certified']);self.assertEqual(q['chosen_lift_discrepancy'],IDENTITY)
        old=self.r['required35_reuses_prior_target'];self.assertTrue(all(x['exact_disk_equal'] for x in old['individual_match']));self.assertEqual([x['closed_certificate']['intersection_number'] for x in old['unchanged_donor_diagnostics']],[4,4]);self.assertTrue(all(not x['comparison']['equal'] and not x['applied'] and x['support_length']==10 for x in self.r['limited_unapplied_round234_probes']))
    def test_saved_report_all_full_splits_and_no_actual_replay_or_graphics_change(self):
        r=self.r;root=Path(__file__).resolve().parents[1];saved=json.loads((root/'docs/proofs/six-seven-posthalf-lantern-targets.json').read_text(encoding='utf-8'));self.assertEqual(saved,json.loads(json.dumps(r,default=asdict)))
        for p in r['complete_point_pushing']:self.assertEqual(exact_action(p['actual'].word,5),exact_action(p['split'].reconstructed_word,5))
        self.assertEqual((r['graphical_operations_added'],r['external_adjacent_checks_added'],r['new_sphere_moves'],r['exterior_caps']),(0,0,0,0));self.assertFalse(r['public_replay_changed']);self.assertFalse(r['useful_complete_join_reached']);self.assertEqual((r['preferred_moves'],r['preferred_steps']),(101,71))


if __name__=='__main__':unittest.main()
