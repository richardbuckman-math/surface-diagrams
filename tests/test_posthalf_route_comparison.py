import json,unittest
from pathlib import Path
from dataclasses import asdict
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_route_comparison import report
from examples.build_posthalf_route_comparison import pictures,picture
from surface_diagrams.mapping_classes import exact_action
ROOT=Path(__file__).resolve().parents[1]

class PosthalfRouteComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_common_complete_endpoints_and_immutable_joins(self):
        r=self.r;self.assertTrue(r['common_input']['literal_complete_factor_tuple_equal']);self.assertTrue(r['literal_terminal_join_after_id_only_alignment']);self.assertEqual(len(r['literal_research_joins']),10);self.assertTrue(all(x['literal_complete_factor_tuple_equal'] for x in r['literal_research_joins']));self.assertTrue(all(x['only_id_changed'] and x['individual_exact_disk_equal'] for x in r['terminal_id_ancestry_alignment']));self.assertFalse(r['adopted']);self.assertFalse(r['public_replay_changed']);self.assertFalse(r['alternative_parallel_count_claimed'])
    def test_complete_tail_metrics_include_atomic_states_without_dominance_claim(self):
        a=self.r['route_metrics']['preferred'];b=self.r['route_metrics']['alternative'];self.assertEqual((a['operations'],b['operations'],a['external_adjacent_checks'],b['external_adjacent_checks']),(40,61,67,41));pa=a['main_and_external_atomic']['peaks'];pb=b['main_and_external_atomic']['peaks'];self.assertEqual((pa['factor_rows']['value'],pb['factor_rows']['value'],pa['max_support_word']['value'],pb['max_support_word']['value'],pa['total_support_word']['value'],pb['total_support_word']['value'],pa['braid_letters']['value'],pb['braid_letters']['value']),(18,19,18,18,147,132,258,290));self.assertIn('NOT a claim of fewer total atomic',b['scope'])
    def test_fixed_first_reach_panels_keep_every_full_kernel_and_closed_pair(self):
        ps=self.r['panels'];self.assertEqual([p['visible_standard_unit_exteriors'] for p in ps],[1,1,2,2,3,3]);self.assertTrue(all(p['first_milestone_reach_verified'] for p in ps));self.assertEqual([(p['closed_matrix']['total'],p['closed_matrix']['maximum']) for p in ps],[(1536,74),(862,36),(472,36),(240,14),(20,2),(118,14)]);self.assertEqual(sum(len(p['closed_matrix']['pairs']) for p in ps),519)
        for p in ps:
            self.assertTrue(all(not f.half for f in p['stage']['factors']))
            for x in p['full_point_pushing']:self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
    def test_report_and_svg_reproduce_fixed_unnumbered_grid(self):
        r,items=pictures();self.assertEqual(r,json.loads(json.dumps(self.r,default=asdict)));counts=[]
        for name,title,s in items:
            svg=picture(s,title);self.assertEqual(svg,(ROOT/'docs/proofs/posthalf-route-comparison'/(name+'.svg')).read_text(encoding='utf-8'));doc=ET.fromstring(svg);counts.append(sum(n.get('class')=='marked-point' for n in doc.iter()));self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()))
        self.assertEqual(counts,[96,90,96,84,48,66])

if __name__=='__main__':unittest.main()