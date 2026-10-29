import json,unittest
from dataclasses import asdict,replace
from pathlib import Path
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_third_exterior import report
from examples.build_posthalf_third_exterior_comparison import pictures,picture
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.posthalf_third_exterior import expose_posthalf_third_exterior
from surface_diagrams.projected_relations import pc_daisy_terms
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
ROOT=Path(__file__).resolve().parents[1]


class PosthalfThirdExteriorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report();cls.q=cls.r['route'];cls.source=cls.q['stages'][0]['factors']
    def test_seven_moves_keep_old_records_and_account_for_all_donor_units(self):
        q=self.q;self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['named_substitutions']),(7,7,2));self.assertEqual((len(q['factors']),q['after_score']['max_support_word'],q['after_score']['total_support_word'],q['after_score']['braid_letters'],q['peak_support_word']),(11,7,44,126,7))
        before={f.id:f for f in self.source};after={f.id:f for f in q['factors']};shared=set(before)&set(after);self.assertEqual(len(shared),9);self.assertTrue(all(before[n]==after[n] for n in shared));self.assertTrue(all(n not in after for n in q['consumed_source_ids']));self.assertEqual(q['remaining_125_donor_petal'].id,'third.loan.0');self.assertNotIn('third.loan.1',after);self.assertNotIn('third.loan.2',after)
        for n in ('reflected.exterior','posthalf.exterior','reflected.loan.2','outer.loan.1','outer.loan.2'):self.assertEqual(before[n],after[n])
    def test_positive_root_carry_changes_only35_and_keeps_actual_root_literal(self):
        before={f.id:f for f in self.source};after={f.id:f for f in self.q['stages'][1]['factors']};self.assertEqual([n for n in before if before[n]!=after[n]],['reflected.output.1']);self.assertEqual(before['reflected.inner125'],after['reflected.inner125']);canonical=pc_daisy_terms(Factor('D5',(),1,5).mapping_class);self.assertEqual(exact_action(after['reflected.output.1'].word,5),exact_action(canonical[2].word,5))
    def test_actual125_rose_parent_rechart_and_both_needed_petals_match(self):
        s=self.q['stages'][2];w=s['named_pattern_witness'];self.assertEqual(w['common_chart'],(-4,-3,1));self.assertTrue(all(x['exact_disk_equal'] for x in w['actual_parent_rechart_match']));self.assertTrue(all(x['exact_disk_equal'] for x in w['individual_matches']+w['individual_output_matches']));self.assertEqual(s['framed_balance_before_minus_after'],(-1,-1,0,0,-1))
        canonical=pc_daisy_terms(Factor('D5',(),1,5).mapping_class);loan=s['local_after'];self.assertEqual(exact_action(loan[0].word,5),exact_action(Factor('12',(),1,2).word,5))
        for f,t in zip(loan[1:],canonical[3:]):self.assertEqual(exact_action(f.word,5),exact_action(t.word,5))
    def test_all_adjacent_checks_raw_cyclic_starts_and_shortside_are_explicit(self):
        q=self.q;self.assertTrue(q['bounded_12_preview']['bounded']);self.assertTrue(q['bounded_short_side_preview']['bounded']);self.assertEqual(len(q['actual_adjacent_certificates']),7)
        for x in q['actual_adjacent_certificates']:self.assertFalse(x['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in x['individual_presentations']))
        for i,s in enumerate(q['stages']):
            if s['kind']=='disk_cyclic_start':self.assertFalse(s['raw_cyclic_discrepancy']);self.assertFalse(reduce_word(s['frame']+product(q['stages'][i-1]['factors'])+inverse_word(s['frame'])+inverse_word(product(s['factors']))))
        before={f.id:f for f in self.source}
        for s in q['stages']:
            by={f.id:f for f in s['factors']}
            for n in ('reflected.loan.2','reflected.exterior','posthalf.exterior'):self.assertEqual(before[n],by[n])
    def test_full_actual_cyclic_daisy_and_local_kernel_framing_sphere_lift(self):
        patterns=[s for s in self.q['stages'] if 'named_pattern_witness' in s];self.assertEqual(len(patterns),2);last=patterns[-1];w=last['named_pattern_witness'];self.assertEqual(w['common_chart'],());self.assertEqual(last['framed_balance_before_minus_after'],(1,1,1,1,3));self.assertFalse(w['internal_cyclic_certificate']['raw_cyclic_discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in w['internal_cyclic_certificate']['independently_known_output_invariance']))
        for s in patterns:
            w=s['named_pattern_witness'];self.assertTrue(all(x['exact_disk_equal'] for x in w['individual_matches']+w['individual_output_matches']));self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY);self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
            for x in w['complete_actual_and_normalized_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
    def test_three_odd_exteriors_and_residual_boundary_one_are_not_a_named_closure(self):
        q=self.q;minus=tuple(tuple(-x for x in row) for row in IDENTITY);self.assertEqual(len(q['three_visible_exteriors']),3)
        for f in q['three_visible_exteriors']:self.assertEqual(homology_action(f.word),minus)
        self.assertEqual(q['residual_boundary_power_diagnostic'],1);self.assertEqual(q['residual_chosen_lift'],minus);self.assertEqual(exact_action(product(q['residual_factors']),5),exact_action(BOUNDARY_WORD,5));self.assertFalse(q['residual_named_closure_complete']);self.assertFalse(q['useful_complete_join_reached']);self.assertFalse(q['public_replay_changed']);self.assertEqual((q['half_factors'],q['negative_factors'],q['sphere_moves'],q['exterior_caps']),(0,0,0,0))
        for s in q['state_sphere_lift_certificates']:self.assertTrue(s['sphere_certificate']['certified']);self.assertEqual(s['chosen_lift'],IDENTITY);self.assertLessEqual(s['score']['max_support_word'],20)
        for x in q['endpoint_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
    def test_long_side_failed_candidate_is_unapplied_not_a_partial_route(self):
        p=self.q['unapplied_rejected_long_gather'];self.assertFalse(p['bounded']);self.assertFalse(p['applied']);self.assertEqual(p['rejected_score']['max_support_word'],23);self.assertEqual(len(p['unapplied_preview_prefix']),1);self.assertTrue(all(s['score']['max_support_word']<=20 for s in self.q['stages']))
        negative,positive=self.r['exact_125_on35_probes'];self.assertEqual((negative['sign'],negative['support_length'],negative['applied']),(-1,12,False));self.assertFalse(negative['exact_class_comparison']['equal']);self.assertIsNotNone(negative['exact_class_comparison']['first_difference']);self.assertEqual((positive['sign'],positive['support_length'],positive['applied']),(1,2,True));self.assertTrue(positive['exact_class_comparison']['equal']);self.assertTrue(all(x['exact_disk_equal'] for x in self.r['actual_positive_normalized_match']))
        for x in (negative,positive):self.assertEqual(exact_action(x['candidate'].word,5),exact_action(x['full_point_pushing'].reconstructed_word,5))
    def test_source_guards_report_reproduction_grid_and_shared_supports(self):
        for bad in (self.source[:-1],(replace(self.source[0],half=True),)+self.source[1:]):
            with self.assertRaises(ValueError):expose_posthalf_third_exterior(bad)
        r,items=pictures();self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),r);rows=[];counts=[]
        for name,title,s in items:
            svg=picture(s,title);self.assertEqual(svg,(ROOT/'docs/proofs/posthalf-third-exterior-comparison'/(name+'.svg')).read_text(encoding='utf-8'));doc=ET.fromstring(svg);counts.append(sum(n.get('class')=='marked-point' for n in doc.iter()));self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()));d={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));d[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            rows.append(d)
        self.assertEqual(counts,[78,78,90,90,90,66]);shared=set(rows[0])&set(rows[-1]);self.assertEqual(len(shared),9);self.assertTrue(all(rows[0][n]==rows[-1][n] for n in shared))


if __name__=='__main__':unittest.main()