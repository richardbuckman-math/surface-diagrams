import json,unittest
from dataclasses import asdict,replace
from pathlib import Path
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_cyclic_rose import report
from examples.build_posthalf_cyclic_rose_comparison import pictures,picture
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.posthalf_cyclic_rose import contract_posthalf_cyclic_rose


class PosthalfCyclicRoseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_three_actual_moves_keep_donor_petals_and_distinct15_accounting(self):
        r=self.r;q=r['route'];self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['named_substitutions']),(3,1,2));self.assertEqual(len(q['factors']),14);self.assertEqual([f.id for f in q['remaining_345_donor_petals']],['cyclic135.supply.2','cyclic135.supply.0']);self.assertEqual(q['consumed_matching15_id'],'posthalf.supply.0');self.assertEqual(q['retained_other15_id'],'outer.loan.1');self.assertFalse(q['round345_loan_returned'])
        before={f.id:f for f in q['stages'][0]['factors']};after={f.id:f for f in q['factors']};shared=set(before)&set(after);self.assertEqual(len(shared),11);self.assertTrue(all(before[n]==after[n] for n in shared));self.assertEqual((q['after_score']['max_support_word'],q['after_score']['total_support_word'],q['after_score']['braid_letters'],r['after_closed_matrix']['total'],r['after_closed_matrix']['maximum']),(9,65,146,320,20));self.assertEqual((r['posthalf_combined_operations'],r['posthalf_combined_adjacent_checks'],r['research_prefix_operation_count_at_checkpoint']),(38,28,81))
    def test_full_common_chart_cyclic_words_actual_matches_and_signed_balances(self):
        patterns=[s for s in self.r['route']['stages'] if 'named_pattern_witness' in s];self.assertEqual(len(patterns),2)
        for s in patterns:
            w=s['named_pattern_witness'];self.assertTrue(all(x['exact_disk_equal'] for x in w['individual_matches']+w['individual_output_matches']));c=w['internal_cyclic_certificate'];self.assertFalse(c['raw_cyclic_discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in c['independently_known_output_invariance']));self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY);self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
        self.assertEqual(patterns[-1]['named_pattern_witness']['common_chart'],(-1,-1,-3,-2,1,2,3));self.assertEqual(patterns[0]['framed_balance_before_minus_after'],(0,0,-1,-1,-1));self.assertEqual(patterns[-1]['framed_balance_before_minus_after'],(1,0,1,0,1))
    def test_complete_raw_disk_sphere_lift_and_nonabelian_endpoint_checks(self):
        q=self.r['route']
        for a in q['actual_adjacent_certificates']:self.assertFalse(a['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in a['individual_presentations']))
        for c in q['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY);self.assertLessEqual(c['score']['max_support_word'],20)
        for p in q['endpoint_point_pushing']:self.assertEqual(exact_action(p['actual'].word,5),exact_action(p['split'].reconstructed_word,5))
        self.assertEqual(homology_action(q['exterior'].word),tuple(tuple(-x for x in row) for row in IDENTITY));self.assertEqual((q['half_factors'],q['negative_factors'],q['sphere_moves'],q['exterior_caps']),(0,0,0,0));self.assertFalse(q['useful_complete_join_reached'])
    def test_order_gaps_are_exact_and_target_first_root_remains_unapplied(self):
        r=self.r
        for q in (r['original_round_cluster_order_gap'],r['new_R123_25_R135_order_gap']):
            witnesses=q.get('noncentrality_witnesses',q.get('actual_noncentrality_witnesses'));self.assertTrue(any(x['left']!=x['right'] for x in witnesses));self.assertFalse(q['applied'])
        q=r['new_R123_25_R135_order_gap'];self.assertEqual(q['common_chart'],(-3,-3,2,-4));self.assertTrue(all(x['exact_disk_equal'] for x in q['individual_curve_matches']));self.assertTrue(all(not x for x in q['internal_raw_discrepancies']));self.assertFalse(q['needed_internal_raw_discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in q['needed_individual_matches']));self.assertEqual(exact_action(product(q['needed_actual_order']),5),exact_action(product(q['correct_outputs']),5));self.assertFalse(r['next_outside_target']['inverse_block_test_performed'])
    def test_unselected_S1_tradeoff_and_scoped_failed_probes_are_not_hidden(self):
        r=self.r;q=r['unselected_S1_interchange'];self.assertFalse(q['route']['selected']);self.assertEqual((q['route']['graphical_operations'],q['closed_matrix']['total'],q['closed_matrix']['maximum']),(1,334,18));self.assertEqual(sum(x['delta']<0 for x in q['changed_pairs']),5);self.assertEqual(sum(x['delta']>0 for x in q['changed_pairs']),1);self.assertTrue(all(not x['applied'] and not x['comparison']['equal'] for x in r['failed_new_round_petal_preconditioners']));self.assertEqual([x['support_length'] for x in r['failed_source_root_preconditioners']],[11,67]);self.assertEqual(r['rejected12_donor_preconditioner']['score']['max_support_word'],35);self.assertFalse(r['rejected12_donor_preconditioner']['applied'])
    def test_report_source_guards_and_unchanged_source_exact_supports(self):
        r=self.r;root=Path(__file__).resolve().parents[1];self.assertEqual(json.loads((root/'docs/proofs/six-seven-posthalf-cyclic-rose.json').read_text()),json.loads(json.dumps(r,default=asdict)));fs=r['route']['stages'][0]['factors']
        for bad in (fs[:-1],fs[:8]+(replace(fs[8],half=True),)+fs[9:]):
            with self.assertRaises(ValueError):contract_posthalf_cyclic_rose(bad)
        _,items=pictures();rows=[];counts=[]
        for name,title,stage in items:
            svg=picture(stage,title);self.assertEqual(svg,(root/'docs/proofs/posthalf-cyclic-rose-comparison'/(name+'.svg')).read_text());doc=ET.fromstring(svg);counts.append(sum(n.get('class')=='marked-point' for n in doc.iter()));self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()));d={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));d[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            rows.append(d)
        self.assertEqual(counts,[84,96,96,84]);self.assertEqual(len(set(rows[0])&set(rows[-1])),11);self.assertTrue(all(rows[0][n]==rows[-1][n] for n in set(rows[0])&set(rows[-1])))


if __name__=='__main__':unittest.main()
