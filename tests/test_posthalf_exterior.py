import json,unittest
from pathlib import Path
from dataclasses import asdict
from collections import Counter
from examples.analyze_posthalf_exterior import report
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.posthalf_exterior import expose_posthalf_exterior

class PosthalfExteriorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report();cls.route=cls.r['route']
    def test_actual_repeated_rose_and_supplier_keep_every_ordered_input_output_match(self):
        s=self.route['stages'];self.assertEqual((self.route['graphical_operations'],self.route['adjacent_checks']),(14,10))
        named=[x for x in s if x.get('named_pattern_witness')];self.assertEqual(len(named),6)
        for x in named:
            w=x['named_pattern_witness'];self.assertTrue(all(m['exact_disk_equal'] for m in w['individual_matches']+w['individual_output_matches']));self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY);self.assertEqual(len(x['framed_balance_before_minus_after']),5)
        supplier=s[5]['named_pattern_witness'];self.assertTrue(supplier['internal_parent_match'][0]['exact_disk_equal']);self.assertTrue(supplier['matched_spare'][0]['exact_disk_equal']);self.assertFalse(supplier['normalized45_split5'].kernel_loop);self.assertFalse(supplier['normalized45_split4'].kernel_loop)
    def test_all_actual_adjacent_and_cyclic_moves_and_retained_states_are_certified(self):
        r=self.route;self.assertEqual(len(r['state_sphere_lift_certificates']),25);self.assertEqual(r['peak_support_word'],18)
        for c in r['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY);self.assertLessEqual(c['score']['max_support_word'],18)
        for a in r['actual_adjacent_certificates']:self.assertFalse(a['raw_certificate']['discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in a['individual_presentations']))
        for s in r['stages']:
            if s['kind']=='disk_cyclic_start':self.assertFalse(s['raw_cyclic_discrepancy']);self.assertIn('frame',s)
        w=r['stages'][-1]['named_pattern_witness'];self.assertFalse(w['internal_raw_cyclic_discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in w['individually_known_output_frame_matches']))
    def test_first_loan_returned_second_supplier_expanded_and_odd_exterior_stays_visible(self):
        r=self.route;self.assertTrue(r['first_round12_loan_returned']);self.assertTrue(r['round45_supplier_still_expanded']);self.assertEqual(Counter((f.points,f.power,f.half) for f in r['factors']),Counter({(5,1,False):1,(3,1,False):8,(2,1,False):6}))
        negative=tuple(tuple(-x for x in row) for row in IDENTITY)
        self.assertEqual(homology_action(r['exterior'].word),negative);self.assertEqual(homology_action(product(r['factors'][1:])),negative);self.assertEqual(homology_action(product(r['factors'])),IDENTITY)
        self.assertEqual((r['sphere_moves'],r['exterior_caps'],r['half_factors_introduced']),(0,0,0));self.assertFalse(r['residual_named_closure_complete'])
        self.assertTrue(r['stages'][11]['named_pattern_witness']['restored_original_donor'][0]['exact_disk_equal'])
        final={f.id:f for f in r['factors']};self.assertNotEqual(exact_action(final['posthalf.supply.0'].word,5),exact_action(final['posthalf.output.1'].word,5))
        for e in r['endpoint_point_pushing']:self.assertEqual(exact_action(e['factor'].word,5),exact_action(e['split'].reconstructed_word,5))
    def test_scoped_geometry_comparison_failures_and_unapplied_next_target(self):
        r=self.r;self.assertEqual((r['reference_first_exterior']['closed_matrix']['total'],r['reference_first_exterior']['closed_matrix']['maximum'],r['endpoint_closed_matrix']['total'],r['endpoint_closed_matrix']['maximum']),(1536,74,862,36))
        self.assertEqual([p['support_length'] for p in r['limited_unapplied_45_probes']],[10,10,146,144]);self.assertTrue(all(not p['exact_match']['equal'] and not p['applied'] for p in r['limited_unapplied_45_probes']));self.assertFalse(r['next_cabled_candidate']['applied']);self.assertFalse(r['public_replay_changed'])
        with self.assertRaises(ValueError):expose_posthalf_exterior(self.route['factors'])
    def test_source_pinned_report_reproduces_without_any_preferred_artifact_change(self):
        saved=json.loads((Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-posthalf-exterior.json').read_text(encoding='utf-8'));self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),saved)
        self.assertEqual((self.r['complete_preferred_moves'],self.r['complete_preferred_steps']),(101,71));self.assertTrue(self.r['seven_more_source_operations_than_reference'])

if __name__=='__main__':unittest.main()
