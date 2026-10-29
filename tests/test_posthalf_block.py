import json,unittest
from dataclasses import asdict,replace
from pathlib import Path
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_block import report
from examples.build_posthalf_block_comparison import pictures,picture
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.posthalf_block import transport_posthalf_loan_block


class PosthalfBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_same_records_four_curves_shorten_every_changed_closed_pair_decreases(self):
        r=self.r;q=r['route'];self.assertEqual((q['graphical_operations'],q['adjacent_checks']),(15,14));self.assertEqual((q['after_score']['max_support_word'],q['after_score']['total_support_word'],q['after_score']['braid_letters']),(9,67,152));self.assertEqual(len(q['factors']),14)
        self.assertEqual([(x['before'],x['after']) for x in r['changed_support_lengths']],[(9,3),(15,9),(8,4),(8,6)]);self.assertEqual((r['before_closed_matrix']['total'],r['after_closed_matrix']['total'],r['after_closed_matrix']['maximum']),(524,346,20));self.assertEqual(len(r['changed_pairs']),28);self.assertTrue(all(x['delta']<0 for x in r['changed_pairs']))
        before={f.id:f for f in q['stages'][0]['factors']};after={f.id:f for f in q['factors']};self.assertEqual(set(before),set(after));self.assertTrue(all(before[n]==after[n] for n in before if n not in q['changed_record_ids']));self.assertTrue(q['loan_records_restored_literally']);self.assertTrue(all(x['exact_disk_equal'] for x in q['matching15_copies']));self.assertIn('outer.loan.1',after);self.assertIn('posthalf.supply.0',after)
    def test_two_extra_actual_moves_lower_transient_closed_peaks_with_exact_endpoint_matches(self):
        r=self.r;metrics=r['trajectory_comparisons'];self.assertEqual([(metrics[n]['peak_closed_sum'],metrics[n]['peak_closed_pair'],metrics[n]['peak_support_word']) for n in ('direct','forward','inverse')],[(536,52,17),(552,48,17),(532,46,17)])
        self.assertEqual((r['direct_comparison']['graphical_operations'],r['direct_comparison']['adjacent_checks']),(13,12));self.assertEqual(r['forward_comparison']['graphical_operations'],15)
        for j in r['endpoint_presentation_joins']:
            self.assertTrue(all(x['exact_disk_equal'] for x in j['individual_matches']))
            if j['route']!='inverse':self.assertFalse(j['literal_before_presentation_match']);self.assertEqual([x['id'] for x in j['different_presentations']],['alternative.P13'])
        self.assertGreater(metrics['inverse']['peak_closed_pair'],r['before_closed_matrix']['maximum'])
    def test_raw_cyclic_adjacent_presentations_full_kernels_and_odd_exterior_remain(self):
        for q in (self.r['route'],self.r['direct_comparison'],self.r['forward_comparison']):
            for s in q['stages']:
                if s['kind']=='disk_cyclic_start':self.assertFalse(s['raw_cyclic_discrepancy'])
            for a in q['actual_adjacent_certificates']:self.assertFalse(a['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(x['exact_disk_equal'] for x in a['individual_presentations']))
            for c in q['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY);self.assertLessEqual(c['score']['max_support_word'],20)
            for p in q['endpoint_point_pushing']:self.assertEqual(exact_action(p['actual'].word,5),exact_action(p['split'].reconstructed_word,5))
            self.assertEqual(homology_action(q['exterior'].word),tuple(tuple(-x for x in row) for row in IDENTITY));self.assertFalse(q['useful_complete_join_reached'])
    def test_round35_supplier_is_exact_but_unexpanded_and_old13_source_is_literal(self):
        r=self.r;q=r['exact35_supplier'];self.assertFalse(q['applied']);self.assertTrue(all(x['exact_disk_equal'] for x in q['required_match']));self.assertEqual((q['actual_parent'].conjugator,q['actual_parent'].first,q['actual_parent'].points),((),3,3));self.assertTrue(q['sphere_certificate']['certified']);self.assertEqual(q['chosen_lift'],IDENTITY);self.assertEqual(q['signed_pc_balance'],(0,0,-1,-1,-1));self.assertTrue(r['unchanged13_supplier_reference']['source_record_literal']);self.assertFalse(r['remaining_R135_target']['existing_root_matches']);self.assertTrue(all(not x for x in r['remaining_R135_target']['existing_petal_matches']))
    def test_failed_probes_and_next_extension_are_not_applied_routes(self):
        r=self.r;self.assertEqual([x['support_length'] for x in r['failed_new25_probes']],[14,16]);self.assertTrue(all(not x['comparison']['equal'] and not x['applied'] for x in r['failed_new25_probes']));self.assertEqual([x['support_length'] for x in r['failed_required13_preconditioners']],[33,33,59,71]);self.assertTrue(all(not x['applied'] for x in r['failed_required13_preconditioners']));self.assertEqual(r['rejected_next_block_extension']['score']['max_support_word'],40);self.assertFalse(r['rejected_next_block_extension']['applied']);self.assertTrue(r['block12_stabilizer']['block_commutation']['equal']);self.assertFalse(r['block12_stabilizer']['wrong35_commutation']['equal']);self.assertTrue(r['block12_stabilizer']['required35_commutation']['equal'])
    def test_saved_report_source_guards_and_unchanged_support_svgs(self):
        r=self.r;root=Path(__file__).resolve().parents[1];self.assertEqual(json.loads((root/'docs/proofs/six-seven-posthalf-block.json').read_text()),json.loads(json.dumps(r,default=asdict)));fs=r['route']['stages'][0]['factors']
        for bad in (fs[:-1],fs[:2]+(replace(fs[2],half=True),)+fs[3:]):
            with self.assertRaises(ValueError):transport_posthalf_loan_block(bad)
        with self.assertRaises(ValueError):transport_posthalf_loan_block(fs,preparation='scan')
        _,items=pictures();rows=[]
        for name,title,stage in items:
            svg=picture(stage,title);self.assertEqual(svg,(root/'docs/proofs/posthalf-block-comparison'/(name+'.svg')).read_text());doc=ET.fromstring(svg);self.assertEqual(sum(n.get('class')=='marked-point' for n in doc.iter()),84);self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()));d={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));d[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            rows.append(d)
        self.assertEqual(set(n for n in rows[0] if rows[0][n]!=rows[-1][n]),set(r['route']['changed_record_ids']))


if __name__=='__main__':unittest.main()
