import json,unittest
from dataclasses import asdict,replace
from pathlib import Path
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_upper_cabled import report
from examples.build_posthalf_upper_cabled_comparison import pictures,picture
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.posthalf_upper_cabled import contract_posthalf_upper_cabled,upper_cabled_pattern
ROOT=Path(__file__).resolve().parents[1]


class PosthalfUpperCabledTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=report();cls.q=cls.r['route'];cls.source=cls.q['stages'][0]['factors']
    def test_three_actual_moves_preserve_donors_and_both_exteriors(self):
        q=self.q;self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['named_substitutions']),(3,1,1));self.assertEqual((len(q['factors']),q['after_score']['max_support_word'],q['after_score']['total_support_word'],q['after_score']['braid_letters'],q['peak_support_word']),(13,7,52,136,7))
        before={f.id:f for f in self.source};after={f.id:f for f in q['factors']};shared=set(before)&set(after);self.assertEqual(len(shared),11);self.assertTrue(all(before[n]==after[n] for n in shared));self.assertTrue(all(n not in after for n in q['consumed_source_ids']));self.assertEqual(q['remaining_123_donor_petal'],before['reflected.loan.2'])
        for n in ('reflected.exterior','posthalf.exterior','reflected.inner125','outer.loan.1','outer.loan.2','cyclic135.supply.2'):self.assertEqual(before[n],after[n])
        self.assertEqual((self.r['posthalf_combined_operations'],self.r['posthalf_combined_adjacent_checks'],self.r['research_prefix_operation_count_at_checkpoint']),(48,32,91))
    def test_actual_interchange_changes_only13_and_cyclic_word_is_raw_exact(self):
        q=self.q;before={f.id:f for f in self.source};after={f.id:f for f in q['stages'][1]['factors']};self.assertEqual([n for n in before if before[n]!=after[n]],['reflected.loan.1']);self.assertEqual(after['reflected.loan.2'],before['reflected.loan.2']);self.assertEqual([f.id for f in q['stages'][1]['factors'][4:8]],['reflected.loan.2','reflected.loan.1','alternative.prepare.F5.1','alternative.prepare.F5.2'])
        for a in q['actual_adjacent_certificates']:self.assertFalse(a['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in a['individual_presentations']))
        s=q['stages'][2];self.assertFalse(s['raw_cyclic_discrepancy']);self.assertFalse(reduce_word(s['frame']+product(q['stages'][1]['factors'])+inverse_word(s['frame'])+inverse_word(product(s['factors']))))
    def test_delta4_reflection_every_input_and_internal_upper_order(self):
        p=upper_cabled_pattern();self.assertEqual(len(p['generator_matches']),3)
        for g in p['generator_matches']:self.assertEqual(exact_action(g['conjugated'],5),exact_action(g['reflected'],5))
        for n in ('individual_reflected_inputs','individual_reflected_outputs','individual_upper_root_interchange_matches'):self.assertTrue(all(x['exact_disk_equal'] for x in p[n]))
        self.assertTrue(all(not x for x in p['internal_raw_cyclic_discrepancies']))
        for a in p['independently_known_output_invariances']:self.assertTrue(all(x['exact_disk_equal'] for x in a))
        self.assertEqual(exact_action(product(p['inputs']),5),exact_action(product(p['outputs']),5));self.assertFalse(p['retained_upper_root_interchange']['disk_word_certificate']['discrepancy']);self.assertIn('retained_unit_interchange',p['retained_base_named_lantern'])
    def test_actual_common_chart_full_framing_local_lift_and_kernels(self):
        s=self.q['stages'][-1];w=s['named_pattern_witness'];self.assertEqual(w['common_chart'],(-3,-3,-2));self.assertEqual(s['framed_balance_before_minus_after'],(1,0,1,0,0));self.assertTrue(all(x['exact_disk_equal'] for x in w['individual_matches']+w['individual_output_matches']));self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
        self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
        for x in w['complete_actual_and_normalized_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
    def test_complete_states_and_two_odd_exteriors_are_not_capped(self):
        q=self.q
        for c in q['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY);self.assertLessEqual(c['score']['max_support_word'],20)
        for x in q['endpoint_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
        self.assertEqual(len(q['two_visible_exteriors']),2)
        for f in q['two_visible_exteriors']:self.assertEqual(homology_action(f.word),tuple(tuple(-x for x in row) for row in IDENTITY))
        self.assertEqual((q['half_factors'],q['negative_factors'],q['sphere_moves'],q['exterior_caps']),(0,0,0,0));self.assertFalse(q['useful_complete_join_reached']);self.assertFalse(q['public_replay_changed'])
    def test_finite_unchanged_order_witnesses_are_scoped_and_unapplied(self):
        for family in self.r['finite_unchanged_selected_families']:
            self.assertFalse(family['applied']);self.assertIn('outside interactions',family['scope'])
            for order in family['orders']:self.assertTrue(any(x['left']!=x['right'] for x in order['commutators']))
        for p in self.r['unapplied45_root_probes']+self.r['unapplied123_petal_block_probes']:self.assertFalse(p['applied'])
    def test_new15_supplier_target_retains_full_rechart_and_both_empty_kernels(self):
        p=self.r['next_new15_supplier_target'];self.assertFalse(p['applied']);self.assertTrue(p['requires_every_transport_crossing_and_actual_context_match']);self.assertFalse(p['current_pair_matches'])
        for n in ('parent_match','individual_last_petal_match','individual_positive_actor_root_match'):self.assertTrue(all(x['exact_disk_equal'] for x in p[n]))
        self.assertTrue(p['sphere_certificate']['certified']);self.assertEqual(p['chosen_lift'],IDENTITY);self.assertFalse(p['full_split5'].kernel_loop);self.assertFalse(p['full_split4'].kernel_loop);self.assertEqual(exact_action(p['full_split4'].shadow_word,3),exact_action((1,2,2,-1),3));self.assertEqual(exact_action(p['full_split5'].reconstructed_word,5),exact_action(p['normalized_actor'].word,5));self.assertEqual(exact_action(p['full_split4'].reconstructed_word,4),exact_action(p['full_split5'].shadow_word,4))
        for x in p['full_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
    def test_source_guards_reproduced_report_and_exact_support_grid(self):
        for bad in (self.source[:-1],self.source[:4]+(replace(self.source[4],half=True),)+self.source[5:]):
            with self.assertRaises(ValueError):contract_posthalf_upper_cabled(bad)
        r,items=pictures();self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),r);rows=[];counts=[]
        for name,title,s in items:
            svg=picture(s,title);self.assertEqual(svg,(ROOT/'docs/proofs/posthalf-upper-cabled-comparison'/(name+'.svg')).read_text(encoding='utf-8'));doc=ET.fromstring(svg);counts.append(sum(n.get('class')=='marked-point' for n in doc.iter()));self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()));d={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));d[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            rows.append(d)
        self.assertEqual(counts,[84,84,84,78]);shared=set(rows[0])&set(rows[-1]);self.assertEqual(len(shared),11);self.assertTrue(all(rows[0][n]==rows[-1][n] for n in shared))


if __name__=='__main__':unittest.main()