import json,unittest
from pathlib import Path
from dataclasses import asdict
from examples.analyze_fixed_half_meeting import report
from examples.build_fixed_half_meeting_comparison import pictures,picture
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY

class FixedHalfMeetingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_both_actual_halves_stay_fixed_and_all_retained_states_are_positive_bounded(self):
        r=self.r;start={f.id:f for f in r['stages'][0]['factors']};meeting=r['stages'][2]['factors']
        self.assertEqual([(f.id,f) for f in meeting if f.half],[(k,start[k]) for k in ('F6','F11')])
        self.assertEqual(len(meeting),17);self.assertEqual(r['new_half_factors'],0);self.assertEqual(r['sphere_moves'],0)
        for entry in r['retained_state_certificates']:
            c=entry['certificate'];self.assertLessEqual(c['score']['maximum'],20);self.assertTrue(c['exact_B5_boundary_fourth_power']);self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
            self.assertTrue(all(f.power>0 for f in entry['factors']))
    def test_independent_carries_have_literal_two_order_equality_and_free_local_certificates(self):
        r=self.r;w=r['independent_carries'];self.assertEqual(w['first_interval'],(7,12));self.assertEqual(w['second_interval'],(13,14));self.assertEqual(w['left_then_right'],w['right_then_left']);self.assertTrue(w['literal_two_order_equality'])
        for steps in w['reverse_atomic_steps']:
            for a in steps:self.assertFalse(a['disk_word_certificate']['discrepancy'])
        self.assertEqual((r['original_local_moves'],r['candidate_local_moves'],r['original_adjacent_checks'],r['candidate_adjacent_checks']),(2,4,6,11))
    def test_complete_join_keeps_combine_and_raw_transport_certificates_separate(self):
        r=self.r;j=r['complete_join'];self.assertTrue(j['combine_disk_equality']['equal']);self.assertFalse(j['raw_transport_free_discrepancy']);self.assertEqual(r['stages'][-1]['factors'],j['target']);self.assertFalse(any(f.half for f in j['target']))
        self.assertTrue(all(m['exact_B5']['equal'] for m in j['individual_matches']))
        self.assertEqual(exact_action(product(j['raw']),5),exact_action(product(j['target']),5))
        for entries in r['neighborhood_kernel_splits'].values():
            for e in entries:self.assertEqual(exact_action(e['closed_neighborhood'].word,5),exact_action(e['split'].reconstructed_word,5))
    def test_half_present_geometry_improves_only_before_the_old_endpoint_is_restored(self):
        r=self.r;a,b=r['original_meeting_matrix'],r['candidate_meeting_matrix'];self.assertEqual((a['total'],a['maximum'],b['total'],b['maximum']),(1094,48,936,36))
        self.assertEqual((r['fixed_meeting_cut_measurements'][0]['score']['maximum'],r['fixed_meeting_cut_measurements'][5]['score']['maximum']),(17,18))
        self.assertEqual(max(s['closed_total'] for s in r['original_half_trajectory']),1094);self.assertEqual(max(s['closed_total'] for s in r['candidate_half_trajectory']),936)
        self.assertEqual(len(r['fixed_meeting_cut_measurements']),7);self.assertFalse(r['public_replay_changed'])
    def test_saved_report_and_all_four_source_exact_support_panels_reproduce(self):
        root=Path(__file__).resolve().parents[1];saved=json.loads((root/'docs/proofs/six-seven-fixed-half-meeting.json').read_text(encoding='utf-8'));self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),saved)
        _,items=pictures();self.assertEqual(len(items),4)
        import xml.etree.ElementTree as ET
        for name,title,s in items:
            svg=picture(s,title);self.assertEqual((root/'docs/proofs/fixed-half-meeting-comparison'/(name+'.svg')).read_text(encoding='utf-8'),svg)
            document=ET.fromstring(svg);groups=[g for g in document.iter() if g.get('data-factor')]
            self.assertEqual([g.get('data-factor') for g in groups],[f['id'] for f in s['factors']]);self.assertEqual(sum(n.get('class')=='marked-point' for n in document.iter()),6*len(groups));self.assertFalse(any(n.get('class')=='marked-point-label' for n in document.iter()))

if __name__=='__main__':unittest.main()
