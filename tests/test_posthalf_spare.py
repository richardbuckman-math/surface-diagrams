import json,unittest
from dataclasses import asdict,replace
from pathlib import Path
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_spare import report
from examples.build_posthalf_spare_comparison import pictures,picture
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.posthalf_spare import gather_posthalf_spare


class PosthalfSpareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_selected_actual_F10_only_improves_all_changed_closed_counts(self):
        r=self.r;q=r['route'];self.assertEqual((q['graphical_operations'],q['adjacent_checks']),(1,1));self.assertEqual(r['F10_support_lengths'],(13,7))
        before={f.id:f for f in q['stages'][0]['factors']};after={f.id:f for f in q['factors']};self.assertTrue(all(before[k]==after[k] for k in before if k!='F10.2'));self.assertNotEqual(before['F10.2'],after['F10.2'])
        self.assertEqual((q['before_score']['max_support_word'],q['after_score']['max_support_word'],q['before_score']['total_support_word'],q['after_score']['total_support_word'],q['before_score']['braid_letters'],q['after_score']['braid_letters']),(15,15,109,103,240,232))
        self.assertEqual((r['before_closed_matrix']['total'],r['selected_closed_matrix']['total'],r['selected_closed_matrix']['maximum']),(770,700,34));self.assertEqual(len(r['selected_changed_pairs']),11);self.assertTrue(all(p['delta']<0 and 'F10.2' in p['ids'] for p in r['selected_changed_pairs']))
    def test_complete_gather_is_reached_but_unselected_and_spare_is_fixed(self):
        r=self.r;q=r['complete_gather_alternative'];self.assertFalse(q['selected']);self.assertEqual((q['graphical_operations'],q['adjacent_checks']),(1,2));self.assertEqual(q['stages'][1]['atomic_steps'][0]['factors'],r['route']['factors'])
        moving=next(f for f in q['stages'][0]['factors'] if f.id=='posthalf.output.1');self.assertEqual(next(f for f in q['factors'] if f.id==moving.id),moving)
        self.assertEqual((q['after_score']['total_support_word'],q['after_score']['braid_letters'],r['complete_gather_closed_matrix']['total']),(107,218,764));self.assertEqual(sum(p['delta']<0 for p in r['complete_gather_changed_pairs']),11);self.assertEqual(sum(p['delta']>0 for p in r['complete_gather_changed_pairs']),10)
        names=[f.id for f in q['factors']];self.assertEqual(names[names.index('alternative.P13')+1],'posthalf.output.1')
    def test_raw_moves_all_presentations_sphere_lifts_and_nonabelian_splits(self):
        for q in (self.r['route'],self.r['complete_gather_alternative']):
            for a in q['actual_adjacent_certificates']:
                self.assertFalse(a['raw_move']['disk_word_certificate']['discrepancy']);self.assertTrue(all(m['exact_disk_equal'] for m in a['individual_presentations']))
            for c in q['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY);self.assertLessEqual(c['score']['max_support_word'],20)
            for p in q['endpoint_point_pushing']:self.assertEqual(exact_action(p['factor'].word,5),exact_action(p['split'].reconstructed_word,5))
            self.assertEqual(homology_action(q['factors'][0].word),tuple(tuple(-x for x in row) for row in IDENTITY));self.assertEqual((q['half_factors'],q['negative_factors'],q['sphere_moves'],q['exterior_caps']),(0,0,0,0));self.assertFalse(q['useful_complete_join_reached'])
    def test_round45_donor_is_exact_and_still_target_only(self):
        t=self.r['new_round45_donor_target'];self.assertEqual(t['common_chart'],(-1,-1,2));self.assertFalse(t['applied']);self.assertTrue(t['requires_bounded_supply_gather_and_useful_join'])
        for key in ('individually_matched_parent','round45_match','current_first_two_supplier_matches'):self.assertTrue(all(m['exact_disk_equal'] for m in t[key]))
        self.assertTrue(t['sphere_certificate']['certified']);self.assertEqual(t['chosen_lift'],IDENTITY);self.assertEqual(t['signed_pc_balance'],(0,-1,0,-1,-1))
        for p in t['complete_point_pushing']:self.assertEqual(exact_action(p['actual'].word,5),exact_action(p['split'].reconstructed_word,5))
    def test_source_guards_report_and_every_other_support_svg(self):
        r=self.r;q=r['route'];fs=q['stages'][0]['factors']
        for bad in (fs[:-1],fs[:-1]+(replace(fs[-1],half=True),),fs[:-1]+(replace(fs[-1],id='wrong'),)):
            with self.assertRaises(ValueError):gather_posthalf_spare(bad)
        root=Path(__file__).resolve().parents[1];saved=json.loads((root/'docs/proofs/six-seven-posthalf-spare.json').read_text(encoding='utf-8'));self.assertEqual(saved,json.loads(json.dumps(r,default=asdict)))
        _,items=pictures();parts=[]
        for name,title,stage in items:
            svg=picture(stage,title);self.assertEqual(svg,(root/'docs/proofs/posthalf-spare-comparison'/(name+'.svg')).read_text(encoding='utf-8'));doc=ET.fromstring(svg)
            self.assertEqual(sum(n.get('class')=='marked-point' for n in doc.iter()),90);self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()))
            rows={}
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));rows[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            parts.append(rows)
        self.assertEqual([k for k in parts[0] if parts[0][k]!=parts[1][k]],['F10.2']);self.assertEqual(set(k for k in parts[0] if parts[0][k]!=parts[2][k]),{'F10.2','posthalf.supply.1'})


if __name__=='__main__':unittest.main()
