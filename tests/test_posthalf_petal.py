import json,unittest
from pathlib import Path
from dataclasses import asdict
from examples.analyze_posthalf_petal import report,multiply
from examples.build_posthalf_petal_comparison import pictures,picture
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action

class PosthalfPetalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_one_actual_curve_changes_and_every_changed_closed_pair_improves(self):
        r=self.r;q=r['route'];self.assertEqual((q['graphical_operations'],q['adjacent_checks']),(1,1));self.assertEqual(q['P13_support_lengths'],(18,8))
        before={f.id:f for f in q['stages'][0]['factors']};after={f.id:f for f in q['factors']};self.assertEqual(set(before),set(after));self.assertTrue(all(before[k]==after[k] for k in before if k!='alternative.P13'))
        self.assertEqual((q['before_score']['max_support_word'],q['after_score']['max_support_word'],q['before_score']['total_support_word'],q['after_score']['total_support_word'],q['before_score']['braid_letters'],q['after_score']['braid_letters']),(18,15,119,109,258,240))
        self.assertEqual((r['before_closed_matrix']['total'],r['after_closed_matrix']['total'],r['before_closed_matrix']['maximum'],r['after_closed_matrix']['maximum']),(862,770,36,34));self.assertEqual(len(r['changed_pairs']),9);self.assertTrue(all(p['delta']<0 and 'alternative.P13' in p['ids'] for p in r['changed_pairs']))
    def test_actual_disk_presentation_full_kernels_and_odd_exterior_are_retained(self):
        q=self.r['route'];self.assertFalse(q['raw_adjacent_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in q['individual_presentation_matches']))
        for c in q['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
        for p in q['endpoint_point_pushing']:self.assertEqual(exact_action(p['factor'].word,5),exact_action(p['split'].reconstructed_word,5))
        self.assertEqual(homology_action(q['factors'][0].word),tuple(tuple(-x for x in row) for row in IDENTITY));self.assertEqual((q['half_factors'],q['sphere_moves'],q['exterior_caps']),(0,0,0));self.assertFalse(q['useful_complete_join_reached'])
    def test_correct_missing_pair_has_a_joint_chart_but_no_actual_supplier(self):
        r=self.r;t=r['correct_cabled_target'];self.assertEqual(t['common_chart'],(-3,-3,-4));self.assertTrue(all(m['exact_disk_equal'] for m in t['actual_root_matches']));self.assertFalse(t['existing_pair_matches']);self.assertFalse(t['applied'])
        self.assertEqual(exact_action(t['required_pair'].word,5),exact_action(t['simple_required_pair'].word,5));self.assertFalse(t['wrong_pair_inner_commutation']['equal']);self.assertTrue(all(g['commutation']['equal'] for g in t['actual_inner_stabilizers']))
        self.assertEqual([d['closed_certificate']['intersection_number'] for d in t['unchanged_triple_supplier_diagnostics']],[4,4]);self.assertEqual([p['support_length'] for p in t['limited_unapplied_root_probes']],[74,74,362,358]);self.assertTrue(all(not p['comparison']['equal'] and not p['applied'] for p in t['limited_unapplied_root_probes']))
        self.assertTrue(all(not x['equal'] for o in r['previous_cabled_candidate']['orders'] for x in o['checks']));self.assertEqual(r['next_two_neighbor_candidate']['closed_pair_certificate']['intersection_number'],2);self.assertFalse(r['next_two_neighbor_candidate']['applied'])
    def test_triangle_exclusions_use_exact_nonzero_integer_witnesses_and_bounds_stay_unknown(self):
        r=self.r
        for key in ('triangle_audits_before','triangle_audits_after'):
            self.assertEqual(len(r[key]),4)
            for t in r[key]:
                self.assertEqual(len(t['orders']),6);self.assertTrue(any(p['certificate']['intersection_number']!=2 for p in t['closed_pairs']))
                for o in t['orders']:
                    self.assertTrue(any(w['left']!=w['right'] for w in o['noncentrality_witnesses']))
                    for w in o['noncentrality_witnesses']:
                        self.assertEqual(w['left'],multiply(w['product_lift'],w['input_lift']));self.assertEqual(w['right'],multiply(w['input_lift'],w['product_lift']))
        self.assertIn('UNKNOWN',r['preliminary_based_action_exhaustion']['status']);self.assertTrue(all(x['score']['max_support_word']==28 and not x['applied'] for x in r['rejected_candidates']));self.assertEqual((r['second_inverse_alternative']['closed_matrix']['total'],r['second_inverse_alternative']['closed_matrix']['maximum']),(818,34));self.assertFalse(r['second_inverse_alternative']['selected'])
    def test_saved_report_and_source_exact_six_point_panels_reproduce(self):
        root=Path(__file__).resolve().parents[1];saved=json.loads((root/'docs/proofs/six-seven-posthalf-petal.json').read_text(encoding='utf-8'));self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),saved)
        self.assertTrue(all(x['value']==3 for x in self.r['incidence_only_pair_ledger']));_,items=pictures();self.assertEqual(len(items),2)
        import xml.etree.ElementTree as ET
        panels=[]
        for name,title,s in items:
            svg=picture(s,title);self.assertEqual((root/'docs/proofs/posthalf-petal-comparison'/(name+'.svg')).read_text(encoding='utf-8'),svg);doc=ET.fromstring(svg)
            self.assertEqual(sum(n.get('class')=='marked-point' for n in doc.iter()),90);self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()));self.assertIn('Highlight = the changed P13 curve.',svg)
            parts={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));parts[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            panels.append(parts)
        self.assertEqual([k for k in panels[0] if panels[0][k]!=panels[1][k]],['alternative.P13'])

if __name__=='__main__':unittest.main()
