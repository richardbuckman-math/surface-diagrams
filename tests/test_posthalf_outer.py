import json,unittest
from dataclasses import asdict,replace
from pathlib import Path
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_outer import report
from examples.build_posthalf_outer_comparison import pictures,picture
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.factorization_explorer import product
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.posthalf_outer import contract_posthalf_daisy


class PosthalfOuterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_four_reached_moves_preserve_shared_curves_and_keep_both_loan_petals(self):
        r=self.r;q=r['route'];self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['internal_adjacent_checks']),(4,1,3));self.assertEqual(len(q['factors']),14);self.assertEqual(len(r['shared_actual_records_unchanged']),11)
        old={f.id:f for f in q['stages'][0]['factors']};new={f.id:f for f in q['factors']};self.assertTrue(all(old[k]==new[k] for k in r['shared_actual_records_unchanged']));self.assertTrue(q['original_P13_unchanged']);self.assertFalse(q['round12_loan_returned']);self.assertEqual([f.id for f in q['remaining_donor_petals']],['outer.loan.1','outer.loan.2'])
        self.assertEqual((q['after_score']['max_support_word'],q['after_score']['total_support_word'],q['after_score']['braid_letters'],r['after_closed_matrix']['total'],r['after_closed_matrix']['maximum']),(15,85,200,524,34));self.assertEqual((r['posthalf_combined_operations'],r['posthalf_combined_adjacent_checks'],r['research_prefix_operation_count_at_checkpoint']),(20,13,63))
    def test_every_named_actual_input_output_and_internal_daisy_move_matches(self):
        q=self.r['route'];patterns=[s for s in q['stages'] if 'named_pattern_witness' in s];self.assertEqual(len(patterns),2)
        for s in patterns:
            w=s['named_pattern_witness'];self.assertTrue(all(m['exact_disk_equal'] for m in w['individual_matches']+w['individual_output_matches']));self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY);self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
        w=patterns[-1]['named_pattern_witness'];self.assertEqual(w['common_chart'],(-1,-1,2,1,2,3,4));self.assertEqual(patterns[-1]['framed_balance_before_minus_after'],(2,1,0,1,1));self.assertEqual(len(w['retained_internal_adjacent_moves']),3)
        for m in w['retained_internal_adjacent_moves']:self.assertFalse(m['disk_word_certificate']['discrepancy'])
        for f,p in zip(w['normalized_actual_inputs'],w['normalized_input_point_pushing']):self.assertEqual(exact_action(f.word,5),exact_action(p.reconstructed_word,5))
    def test_explicit_cyclic_frame_actual_adjacent_moves_full_kernels_and_odd_exterior(self):
        for q in (self.r['route'],self.r['round45_comparison']):
            for s in q['stages']:
                if s['kind']=='disk_cyclic_start':self.assertFalse(s['raw_cyclic_discrepancy'])
            for a in q['actual_adjacent_certificates']:self.assertFalse(a['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in a['individual_presentations']))
            for c in q['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY);self.assertLessEqual(c['score']['max_support_word'],20)
            for p in q['endpoint_point_pushing']:self.assertEqual(exact_action(p['actual'].word,5),exact_action(p['split'].reconstructed_word,5))
            self.assertEqual(homology_action(q['exterior'].word),tuple(tuple(-x for x in row) for row in IDENTITY));self.assertEqual((q['half_factors'],q['negative_factors'],q['sphere_moves'],q['exterior_caps']),(0,0,0,0));self.assertFalse(q['useful_complete_join_reached'])
    def test_45_comparison_uses_matching_other_W_and_rejects_over_bound_carries(self):
        r=self.r;q=r['round45_comparison'];self.assertFalse(q['selected']);self.assertEqual((q['graphical_operations'],q['adjacent_checks']),(3,3));self.assertEqual([x['comparison']['equal'] for x in r['preliminary_spare_matches']],[True,False]);self.assertEqual(q['rejected_direct_V_gather']['rejected_score']['max_support_word'],24);self.assertFalse(q['rejected_direct_V_gather']['applied'])
        w=q['stages'][-1]['named_pattern_witness'];self.assertFalse(w['uses_original_supplier_W']);self.assertEqual(w['consumed_matching_spare_id'],'posthalf.output.1');self.assertFalse(w['internal_raw_cyclic_discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in w['individually_known_output_invariance']))
        self.assertEqual(next(f for f in q['factors'] if f.id=='posthalf.supply.0'),q['original_supplier_W_retained']);self.assertFalse(q['round45_loan_returned_to245']);self.assertEqual([a['score']['max_support_word'] for a in r['rejected_next_comparison_carries']],[26,25]);self.assertTrue(all(not a['applied'] for a in r['rejected_next_comparison_carries']))
        self.assertEqual((q['after_score']['total_support_word'],r['comparison_closed_matrix']['total']),(101,694))
        t=r['next_new15_triangle_target'];self.assertFalse(t['applied']);self.assertFalse(t['necessary_ordered_relation_checked']);self.assertTrue(all(not x['comparison']['equal'] for x in t['new15_comparisons']))
    def test_source_guards_saved_report_and_source_exact_fixed_point_panels(self):
        q=self.r['route'];source=q['stages'][0]['factors']
        for bad in (source[:-1],source[:-1]+(replace(source[-1],half=True),),source[:-1]+(replace(source[-1],id='wrong'),)):
            with self.assertRaises(ValueError):contract_posthalf_daisy(bad)
        root=Path(__file__).resolve().parents[1];saved=json.loads((root/'docs/proofs/six-seven-posthalf-outer.json').read_text(encoding='utf-8'));self.assertEqual(saved,json.loads(json.dumps(self.r,default=asdict)))
        _,items=pictures();parts=[];counts=[]
        for name,title,stage in items:
            svg=picture(stage,title);self.assertEqual(svg,(root/'docs/proofs/posthalf-outer-comparison'/(name+'.svg')).read_text(encoding='utf-8'));doc=ET.fromstring(svg);counts.append(sum(n.get('class')=='marked-point' for n in doc.iter()));self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()))
            rows={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));rows[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            parts.append(rows)
        self.assertEqual(counts,[90,102,84,90]);self.assertTrue(all(parts[0][k]==parts[2][k] for k in self.r['shared_actual_records_unchanged']))


if __name__=='__main__':unittest.main()
