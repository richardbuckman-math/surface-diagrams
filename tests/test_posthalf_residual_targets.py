import json,unittest
from pathlib import Path
from dataclasses import asdict
from examples.analyze_posthalf_residual_targets import report
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY

class PosthalfResidualTargetsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_four_exact_nonzero_necessary_witnesses_are_scoped(self):
        x=self.r['failed_adjacent_four_point_daisy'];self.assertFalse(x['applied']);self.assertEqual(len(x['exact_integral_commutators']),4);self.assertTrue(all(a['left']!=a['right'] for a in x['exact_integral_commutators']));self.assertIn('Outside interactions',x['scope'])
    def test_actual_adjacent_tail_has_every_named_match_and_raw_internal_word(self):
        r=self.r;x=r['exact_adjacent_tail_rose_target'];self.assertEqual(x['source_interval'],(7,10));self.assertEqual(r['source_factors'][7:10],x['actual_inputs']);self.assertTrue(all(m['exact_disk_equal'] for m in x['individual_matches']));c=x['internal_cyclic_certificate'];self.assertFalse(c['raw_cyclic_discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in c['independently_known_output_invariance']));self.assertEqual(exact_action(product(x['actual_inputs']),5),exact_action(x['parent'].word,5));self.assertTrue(x['sphere_certificate']['certified']);self.assertEqual(x['chosen_lift'],IDENTITY);self.assertFalse(x['applied'])
    def test_full_kernels_saved_audit_reproduces_and_no_source_move_claimed(self):
        r=self.r
        for x in r['full_source_and_target_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
        p=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-posthalf-residual-targets.json';self.assertEqual(json.loads(p.read_text(encoding='utf-8')),json.loads(json.dumps(r,default=asdict)));self.assertEqual((r['actual_source_moves'],r['sphere_moves'],r['exterior_caps']),(0,0,0));self.assertFalse(r['public_replay_changed']);self.assertEqual((r['preferred_moves'],r['preferred_steps']),(101,71))

if __name__=='__main__':unittest.main()