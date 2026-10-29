import json,unittest
from dataclasses import asdict,replace
from pathlib import Path
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_residual_closure import report
from examples.build_posthalf_residual_closure_comparison import pictures,picture
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.posthalf_residual_closure import close_posthalf_residual
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
ROOT=Path(__file__).resolve().parents[1]


class PosthalfResidualClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report();cls.q=cls.r['route'];cls.source=cls.q['stages'][0]['factors']
    def test_six_actual_moves_and_four_named_substitutions_reach_four_standard_units(self):
        q=self.q;self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['named_substitutions']),(6,2,4));self.assertEqual([len(s['factors']) for s in q['stages']],[11,9,11,11,8,8,4]);self.assertEqual(len(q['factors']),4)
        standard=Factor('standard.D5',(),1,5)
        for f in q['factors']:self.assertEqual((f.conjugator,f.first,f.points,f.power,f.half),((),1,5,1,False));self.assertEqual(exact_action(f.word,5),exact_action(standard.word,5))
        self.assertEqual(exact_action(product(q['factors']),5),exact_action(BOUNDARY_WORD*4,5));self.assertEqual(q['peak_support_word'],7);self.assertEqual((self.r['posthalf_combined_operations'],self.r['posthalf_combined_adjacent_checks']),(61,41));self.assertEqual((self.r['after_closed_matrix']['total'],self.r['after_closed_matrix']['maximum']),(0,0))
    def test_every_actual_named_input_output_and_separate_local_checks(self):
        stages=[s for s in self.q['stages'] if 'named_pattern_witness' in s];self.assertEqual(len(stages),4)
        for s in stages:
            w=s['named_pattern_witness'];self.assertTrue(all(x['exact_disk_equal'] for x in w['individual_matches']+w['individual_output_matches']));self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY);self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5));self.assertEqual(len(s['framed_balance_before_minus_after']),5)
            for x in w['complete_actual_and_normalized_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
    def test_modified_daisy_internal_checks_and_full_cyclic_words_are_retained(self):
        q=self.q;self.assertEqual(q['internal_adjacent_checks'],3);self.assertTrue(q['residual_named_closure_complete']);self.assertTrue(q['named_disk_boundary_four_complete']);self.assertTrue(q['useful_complete_join_reached']);self.assertFalse(q['terminal_power_combined']);self.assertFalse(q['separate_fourth_power_cap_applied']);self.assertTrue(all(x['exact_disk_equal'] for x in q['terminal_standard_unit_matches']))
        for index in (1,4,6):
            c=q['stages'][index]['named_pattern_witness']['internal_cyclic_certificate'];self.assertFalse(c['raw_cyclic_discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in c['independently_known_output_invariance']))
        w4=q['stages'][4]['named_pattern_witness'];self.assertEqual(w4['common_chart'],(1,2,3));self.assertFalse(w4['retained_internal_interchange']['disk_word_certificate']['discrepancy'])
        w5=q['stages'][6]['named_pattern_witness'];self.assertEqual(w5['common_chart'],(1,-4,-3,-2,-2,1,2,3,4,1,2,3,1,2,1));self.assertEqual(len(w5['retained_internal_interchanges']),2)
        for m in w5['retained_internal_interchanges']:self.assertFalse(m['disk_word_certificate']['discrepancy'])
    def test_both_external_checks_and_full_actual_cyclic_start_are_raw_exact(self):
        q=self.q;self.assertEqual(len(q['actual_adjacent_certificates']),2)
        for x in q['actual_adjacent_certificates']:self.assertFalse(x['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in x['individual_presentations']))
        for i,s in enumerate(q['stages']):
            if s['kind']=='disk_cyclic_start':self.assertFalse(s['raw_cyclic_discrepancy']);self.assertFalse(reduce_word(s['frame']+product(q['stages'][i-1]['factors'])+inverse_word(s['frame'])+inverse_word(product(s['factors']))))
        before={f.id:f for f in q['stages'][2]['factors']};after={f.id:f for f in q['stages'][3]['factors']};changed=[n for n in before if before[n]!=after[n]];self.assertEqual(len(changed),2)
    def test_three_earlier_exteriors_stay_literal_and_four_odd_units_are_not_capped(self):
        old={f.id:f for f in self.source if f.points==5};self.assertEqual(len(old),3);minus=tuple(tuple(-x for x in row) for row in IDENTITY)
        for s in self.q['stages']:
            by={f.id:f for f in s['factors']}
            for n,f in old.items():self.assertEqual(by[n],f)
        for f in self.q['factors']:self.assertEqual(homology_action(f.word),minus)
        self.assertEqual(homology_action(product(self.q['factors'])),IDENTITY);self.assertEqual((self.q['half_factors'],self.q['negative_factors'],self.q['sphere_moves'],self.q['exterior_caps']),(0,0,0,0));self.assertFalse(self.q['public_replay_changed'])
    def test_complete_state_checks_and_endpoint_kernels_are_retained(self):
        for s in self.q['state_sphere_lift_certificates']:self.assertTrue(s['sphere_certificate']['certified']);self.assertEqual(s['chosen_lift'],IDENTITY);self.assertLessEqual(s['score']['max_support_word'],20)
        for x in self.q['endpoint_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
    def test_actual_tail_uses_three_distinct_named_units_and_complete_context(self):
        s=self.q['stages'][1];self.assertEqual([f.id for f in s['local_before']],['outer.loan.1','outer.loan.2','third.loan.0']);self.assertEqual(len(s['local_after']),1);self.assertEqual(s['local_after'][0].points,3);self.assertEqual(exact_action(product(s['local_before']),5),exact_action(s['local_after'][0].word,5));self.assertEqual(s['score']['max_support_word'],7)
    def test_source_guard_and_exact_saved_report_reproduce(self):
        for bad in (self.source[:-1],(replace(self.source[0],half=True),)+self.source[1:]):
            with self.assertRaises(ValueError):close_posthalf_residual(bad)
        r,_=pictures();self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),r)
    def test_complete_source_join_keeps_every_chart_scope_and_terminal_plan_separate(self):
        j=self.r['route_join'];self.assertEqual(j['complete_source_operations'],106);self.assertEqual(tuple(j['route_parts']),(43,55,6,1,1));self.assertEqual(j['actual_reached_source_operations'],104);self.assertEqual(len(j['literal_joins']),10);self.assertTrue(all(x['literal_complete_factor_tuple_equal'] for x in j['literal_joins']));self.assertTrue(j['literal_terminal_join_after_id_alignment'])
        terminal=j['terminal_plan'];self.assertFalse(terminal['combine_applied']);self.assertFalse(terminal['cap_applied']);self.assertTrue(terminal['full_terminal_disk_discrepancy_unchanged']);self.assertEqual(tuple(j['existing_raw_sphere_indices']),(14,16,17));self.assertEqual(tuple(j['planned_raw_sphere_indices']),(14,16,17,106));self.assertFalse(j['parallel_step_count_claimed'])
        frames=j['explicit_full_frame_certificates'];self.assertTrue(any(x['tail_B5_frame'] for x in frames))
        for x in frames:
            self.assertFalse(x['source_centrality_assumed']);self.assertTrue(x['faithful_complete_frame_equal'])
            if x['tail_B5_frame']:self.assertTrue(all(1<=abs(k)<=4 for k in x['frame']))
        for x in j['tail_terminal_centrality_certificates']:self.assertTrue(x['terminal_fourth_power_fixed']);self.assertFalse(x['source_centrality_assumed'])
        self.assertEqual(len(j['terminal_standard_unit_matches']),4);self.assertTrue(all(x['exact_disk_equal'] for x in j['terminal_standard_unit_matches']));self.assertEqual(len(j['terminal_id_ancestry_alignment']),4);self.assertTrue(all(x['only_id_changed'] for x in j['terminal_id_ancestry_alignment']))
    def test_source_exact_support_grid_and_all_three_shared_exterior_svgs(self):
        _,items=pictures();rows=[];counts=[]
        for name,title,s in items:
            svg=picture(s,title);self.assertEqual(svg,(ROOT/'docs/proofs/posthalf-residual-closure-comparison'/(name+'.svg')).read_text(encoding='utf-8'));doc=ET.fromstring(svg);counts.append(sum(n.get('class')=='marked-point' for n in doc.iter()));self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()));d={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));d[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            rows.append(d)
        self.assertEqual(counts,[66,54,66,48,48,24]);shared=set(rows[0])&set(rows[-1]);self.assertEqual(len(shared),3);self.assertTrue(all(rows[0][n]==rows[-1][n] for n in shared))


if __name__=='__main__':unittest.main()