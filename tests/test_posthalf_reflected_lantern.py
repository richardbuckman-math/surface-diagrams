import json,unittest
from dataclasses import asdict,replace
from pathlib import Path
import xml.etree.ElementTree as ET
from examples.build_posthalf_reflected_lantern_comparison import pictures,picture
from examples.analyze_posthalf_reflected_lantern import report
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import product
from surface_diagrams.braid_actions import reduce_word,inverse_word
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.posthalf_reflected_lantern import contract_posthalf_reflected_lantern,reflected_cabled_pattern,expose_posthalf_second_exterior

ROOT=Path(__file__).resolve().parents[1]


class PosthalfReflectedLanternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=tuple(factor_from_data(f) for f in json.loads((ROOT/'docs/proofs/six-seven-posthalf-cyclic-rose.json').read_text(encoding='utf-8'))['route']['factors']);cls.r=report();cls.q=contract_posthalf_reflected_lantern(cls.source);cls.full=cls.r['route']
    def test_four_actual_moves_keep_both_donor_petals_and_shared_records(self):
        q=self.q;self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['named_substitutions']),(4,2,2));self.assertEqual(len(q['factors']),15);self.assertEqual([f.id for f in q['remaining_123_donor_petals']],['reflected.loan.1','reflected.loan.2']);self.assertFalse(q['round12_loan_returned'])
        before={f.id:f for f in self.source};after={f.id:f for f in q['factors']};shared=set(before)&set(after);self.assertEqual(len(shared),11);self.assertTrue(all(before[n]==after[n] for n in shared));self.assertTrue(all(n not in after for n in q['consumed_source_ids']));self.assertIn('outer.loan.1',after);self.assertIn('outer.loan.2',after);self.assertEqual((q['after_score']['max_support_word'],q['after_score']['total_support_word'],q['after_score']['braid_letters']),(7,64,146))
    def test_every_generator_and_reflected_input_output_is_individually_matched(self):
        p=reflected_cabled_pattern();self.assertEqual(len(p['generator_matches']),4)
        for x in p['generator_matches']:self.assertEqual(exact_action(x['conjugated'],5),exact_action(x['reflected'],5))
        for key in ('individual_reflected_inputs','individual_reflected_outputs'):self.assertTrue(all(x['exact_disk_equal'] for x in p[key]))
        self.assertEqual(exact_action(product(p['inputs']),5),exact_action(product(p['outputs']),5));self.assertIn('retained_unit_interchange',p['base_named_cabled_lantern'])
    def test_actual_patterns_framing_and_local_disk_sphere_lift_checks(self):
        patterns=[s for s in self.q['stages'] if 'named_pattern_witness' in s];self.assertEqual(len(patterns),2)
        for s in patterns:
            w=s['named_pattern_witness'];self.assertTrue(all(x['exact_disk_equal'] for x in w['individual_matches']+w['individual_output_matches']));self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY);self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5));self.assertEqual(len(s['framed_balance_before_minus_after']),5)
        self.assertEqual(patterns[-1]['named_pattern_witness']['common_chart'],(-3,-1,2,1));self.assertIn('retained_reflected_named_pattern',patterns[-1]['named_pattern_witness'])
    def test_all_adjacent_moves_are_reconstructed_and_commuting_neighbors_literal(self):
        q=self.q;self.assertTrue(q['bounded_loan_preview']['bounded']);self.assertEqual(len(q['actual_adjacent_certificates']),2)
        for a in q['actual_adjacent_certificates']:self.assertFalse(a['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in a['individual_presentations']))
        before={f.id:f for f in self.source}
        for s in q['stages']:
            by={f.id:f for f in s['factors']}
            for n in ('outer.O1245','posthalf.exterior'):self.assertEqual(by[n],before[n])
        cyclic=q['stages'][1];self.assertFalse(cyclic['raw_cyclic_discrepancy']);self.assertFalse(reduce_word(cyclic['frame']+product(q['stages'][0]['factors'])+inverse_word(cyclic['frame'])+inverse_word(product(cyclic['factors']))))
    def test_complete_sphere_lift_and_nonabelian_kernels_and_odd_exterior_retained(self):
        q=self.full
        for c in q['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY);self.assertLessEqual(c['score']['max_support_word'],20)
        for p in q['endpoint_point_pushing']:self.assertEqual(exact_action(p['actual'].word,5),exact_action(p['split'].reconstructed_word,5))
        self.assertEqual(homology_action(q['exterior'].word),tuple(tuple(-x for x in row) for row in IDENTITY));self.assertEqual((q['half_factors'],q['negative_factors'],q['sphere_moves'],q['exterior_caps']),(0,0,0,0));self.assertFalse(q['useful_complete_join_reached']);self.assertFalse(q['public_replay_changed'])
    def test_source_guards_and_source_exact_grid_and_shared_supports(self):
        for bad in (self.source[:-1],self.source[:10]+(replace(self.source[10],half=True),)+self.source[11:]):
            with self.assertRaises(ValueError):contract_posthalf_reflected_lantern(bad)
        r,items=pictures();self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),r);rows=[];counts=[]
        for name,title,stage in items:
            svg=picture(stage,title);self.assertEqual(svg,(ROOT/'docs/proofs/posthalf-reflected-lantern-comparison'/(name+'.svg')).read_text(encoding='utf-8'));doc=ET.fromstring(svg);counts.append(sum(n.get('class')=='marked-point' for n in doc.iter()));self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()));d={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));d[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            rows.append(d)
        self.assertEqual(counts,[84,96,96,90,90,84]);self.assertEqual(len(set(rows[0])&set(rows[-1])),9);self.assertTrue(all(rows[0][n]==rows[-1][n] for n in set(rows[0])&set(rows[-1])))

    def test_second_exterior_cabled_lantern_has_every_actual_input_and_internal_word(self):
        q=self.full
        for i,s in enumerate(q['stages']):
            if s['kind']=='disk_cyclic_start':self.assertFalse(s['raw_cyclic_discrepancy']);self.assertFalse(reduce_word(s['frame']+product(q['stages'][i-1]['factors'])+inverse_word(s['frame'])+inverse_word(product(s['factors']))))
        for a in q['actual_adjacent_certificates']:self.assertFalse(a['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in a['individual_presentations']))
        self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['named_substitutions']),(7,3,3));self.assertEqual((len(q['factors']),q['after_score']['max_support_word'],q['after_score']['total_support_word'],q['after_score']['braid_letters']),(14,7,62,148));self.assertEqual(q['peak_support_word'],9)
        patterns=[s for s in q['stages'] if 'named_pattern_witness' in s];self.assertEqual(len(patterns),3);last=patterns[-1]['named_pattern_witness'];self.assertEqual(last['common_chart'],(-3,-4,-3));self.assertTrue(all(not w for w in last['internal_raw_cyclic_discrepancies']))
        for family in last['independently_known_output_invariances']:self.assertTrue(all(x['exact_disk_equal'] for x in family))
        for family in last['canonical_commutation_matches']:self.assertTrue(all(x['exact_disk_equal'] for x in family))
        for s in patterns:
            w=s['named_pattern_witness'];self.assertTrue(all(x['exact_disk_equal'] for x in w['individual_matches']+w['individual_output_matches']));self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
            for x in w['complete_actual_and_normalized_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
        before={f.id:f for f in self.source};after={f.id:f for f in q['factors']};shared=set(before)&set(after);self.assertEqual(len(shared),9);self.assertTrue(all(before[n]==after[n] for n in shared));self.assertEqual(len(q['two_visible_exteriors']),2)
        for f in q['two_visible_exteriors']:self.assertEqual(homology_action(f.word),tuple(tuple(-x for x in row) for row in IDENTITY))
        self.assertEqual(q['residual_chosen_lift'],IDENTITY);self.assertEqual(q['residual_boundary_power_diagnostic'],2);self.assertFalse(q['residual_named_closure_complete']);self.assertEqual((self.r['after_closed_matrix']['total'],self.r['after_closed_matrix']['maximum']),(240,14));self.assertEqual((self.r['posthalf_combined_operations'],self.r['posthalf_combined_adjacent_checks'],self.r['research_prefix_operation_count_at_checkpoint']),(45,31,88))
    def test_precise_inverse_fresh_block_failure_is_unapplied_and_not_a_gather(self):
        p=self.r['failed_inverse_fresh_block_probe'];self.assertEqual(p['support_length'],19);self.assertFalse(p['applied']);self.assertFalse(p['exact_class_comparison']['equal']);self.assertIsNotNone(p['exact_class_comparison']['first_difference']);self.assertEqual(exact_action(p['candidate'].word,5),exact_action(p['full_candidate_point_pushing'].reconstructed_word,5))


if __name__=='__main__':unittest.main()
