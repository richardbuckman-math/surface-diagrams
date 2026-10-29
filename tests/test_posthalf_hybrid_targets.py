import json,unittest
from pathlib import Path
from dataclasses import asdict
from examples.analyze_posthalf_hybrid_targets import report
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY
class PosthalfHybridTargetsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_failed_prescribed_order_is_hypothetical_and_has_all_nonzero_witnesses(self):
        x=self.r['failed_proposed_order'];self.assertFalse(x['applied']);self.assertTrue(all(y['left']!=y['right'] for y in x['exact_integral_commutators']));self.assertFalse(x['faithful_output_miss']['equal']);self.assertIn('HYPOTHETICAL',x['hypothetical_outer'].id)
    def test_named_two_outer_chart_keeps_the_missing_pair_and_order_explicit(self):
        x=self.r['two_outer_named_target'];self.assertEqual(x['common_chart'],(-2,-3));self.assertTrue(all(y['exact_disk_equal'] for y in x['individual_two_outer_matches']));self.assertFalse(x['actual_older25_miss']['equal']);self.assertFalse(x['applied']);self.assertEqual(exact_action(product(x['inputs']),5),exact_action(product(x['outputs']),5));self.assertTrue(x['sphere_certificate']['certified']);self.assertEqual(x['chosen_lift'],IDENTITY);self.assertFalse(self.r['opposite_chart_probe']['hypothetical_outer_miss']['equal']);self.assertTrue(all(y['exact_disk_equal'] for y in self.r['opposite_chart_probe']['individual_actualO_and_older25_matches']))
    def test_saved_target_and_full_kernels_reproduce_without_any_source_move(self):
        r=self.r
        for x in r['full_source_target_normalized_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
        p=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-posthalf-hybrid-targets.json';self.assertEqual(json.loads(p.read_text(encoding='utf-8')),json.loads(json.dumps(r,default=asdict)));self.assertEqual((r['actual_source_moves'],r['sphere_moves'],r['exterior_caps']),(0,0,0));self.assertFalse(r['next_available_pair_product_target']['both_signs_tested']);self.assertFalse(r['next_available_pair_product_target']['block_gathered']);self.assertFalse(r['adopted']);self.assertFalse(r['public_replay_changed'])
if __name__=='__main__':unittest.main()