import json
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_split_block import report
from examples.build_posthalf_split_block_comparison import pictures,picture
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
ROOT=Path(__file__).resolve().parents[1]

class SplitBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()

    def test_same_source_complete_prepared_route_and_peak(self):
        r=self.r;q=r['route']
        self.assertEqual(r['source_sha256'],sha256((ROOT/'docs/proofs'/r['source_file']).read_bytes()).hexdigest())
        self.assertEqual(tuple(q['stages'][0]['factors']),tuple(r['source_factors']))
        self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['peak_support_word']),(18,18,8))
        self.assertEqual((r['unprepared_comparison']['graphical_operations'],r['unprepared_comparison']['adjacent_checks'],r['unprepared_peak']['max_support_word']),(16,16,12))
        self.assertEqual(r['chosen_peak'],dict(max_support_word=8,total_support_word=50,braid_letters=130))
        self.assertEqual((r['posthalf_combined_operations'],r['posthalf_combined_external_checks'],r['complete_source_plan_operations']),(75,56,120))
        self.assertFalse(r['adopted']);self.assertFalse(r['public_replay_changed'])

    def test_full_split_actions_and_actual_preparation_donor_accounting(self):
        q=self.r['route']
        self.assertEqual(q['left_crossed_neighbors'],('cyclic135.supply.2','reflected.exterior','hybrid.first.1','hybrid.first.2'))
        self.assertEqual(q['right_crossed_neighbors'],('posthalf.exterior','reflected.output.1'))
        self.assertTrue(q['prepared_product_matches_original']['exact_disk_equal'])
        self.assertEqual(q['restored_right_literal'],(False,True))
        self.assertTrue(all(x['exact_disk_equal'] for x in q['restored_right_individual_matches']))
        for x in q['full_block_conjugation_matches']:
            self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['raw_target'].word,5))
        self.assertEqual(q['stages'][-2]['factors'],self.r['unprepared_comparison']['stages'][-2]['factors'])

    def test_scoped_forward_rejection_and_actual_inverse_preparation(self):
        a,b=self.r['preparation_comparisons']
        self.assertEqual((a['name'],a['actor_supports'],a['first_crossing_support'],a['final_support']),('FORWARD',(6,4),28,4))
        self.assertTrue(a['rejected_before_application']);self.assertFalse(a['selected'])
        self.assertEqual((b['name'],b['actor_supports'],b['first_crossing_support'],b['final_support']),('INVERSE',(2,2),6,4))
        self.assertTrue(b['selected']);self.assertFalse(b['rejected_before_application'])
        for prep in (a,b):
            self.assertTrue(prep['full_ordered_product_match']['equal'])
            self.assertEqual(prep['raw_preparation']['disk_word_certificate']['discrepancy'],())
            self.assertTrue(all(x['equal'] for x in prep['preparation_individual_matches']))
            for x in prep['complete_point_pushing']:
                self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))

    def test_every_raw_external_crossing_and_main_atomic_certificate(self):
        for key,limit in (('route',8),('unprepared_comparison',12)):
            q=self.r[key]
            self.assertTrue(all(p['bounded'] for p in q['preapplication_previews']))
            for c in q['actual_adjacent_certificates']:
                self.assertEqual(c['raw_move']['disk_word_certificate']['discrepancy'],())
                self.assertTrue(all(m['exact_disk_equal'] for m in c['individual_presentations']))
            for s in q['stages']:
                if s['kind']=='disk_cyclic_start':self.assertEqual(s['raw_cyclic_discrepancy'],())
            for c in q['state_sphere_lift_certificates']:
                self.assertTrue(c['sphere_certificate']['certified'])
                self.assertEqual(c['chosen_lift'],IDENTITY)
                self.assertLessEqual(c['score']['max_support_word'],limit)

    def test_all_named_inputs_outputs_internal_moves_balances_and_kernels(self):
        for key in ('route','unprepared_comparison'):
            named=[s for s in self.r[key]['stages'] if 'named_pattern_witness' in s]
            self.assertEqual(len(named),2)
            for s in named:
                w=s['named_pattern_witness']
                self.assertTrue(all(m['exact_disk_equal'] for m in w['individual_matches']+w['individual_output_matches']))
                self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
                self.assertEqual(len(s['framed_balance_before_minus_after']),5)
                self.assertTrue(w['sphere_certificate']['certified'])
                self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
                for x in w['complete_actual_and_normalized_point_pushing']:
                    self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
            internal=named[-1]['named_pattern_witness']['retained_internal_interchanges']
            self.assertEqual(len(internal),6)
            self.assertTrue(all(x['disk_word_certificate']['discrepancy']==() for x in internal))

    def test_exact_mixed_classes_closed_pairs_and_four_unit_terminal_join(self):
        r=self.r
        self.assertEqual([x['support_lengths'] for x in r['actual_curve_comparisons']],[(2,10,6,6),(4,12,8,8),(2,6,4,4),(6,4,12,4)])
        self.assertTrue(all(x['split_vs_opposite']['equal'] for x in r['actual_curve_comparisons'][:3]))
        self.assertTrue(r['actual_curve_comparisons'][-1]['split_vs_old']['equal'])
        self.assertEqual(r['old_to_split_closed_pair_changes'],())
        self.assertTrue(r['closed_outer_id_alignment']['only_id_changed'])
        self.assertEqual(r['research_prefix_operations_at_four_exteriors'],118)
        self.assertEqual((r['chosen_late_closed_matrix']['total'],r['chosen_late_closed_matrix']['maximum']),(20,2))
        q=r['route'];p=r['terminal_plan'];end={f.id:f for f in q['factors']}
        self.assertTrue(all(end[f.id]==f for f in q['retained_three_exteriors']))
        minus=tuple(tuple(-v for v in row) for row in IDENTITY)
        self.assertEqual(len(q['factors']),4)
        for f in q['factors']:
            self.assertEqual((f.points,f.power,f.half),(5,1,False));self.assertEqual(homology_action(f.word),minus)
        self.assertTrue(all(x['only_id_changed'] for x in p['id_only_alignment']))
        self.assertEqual(p['combine']['raw_free_word_discrepancy'],())
        self.assertEqual(p['full_cap_discrepancy_word'],p['combine']['local_after'][0].word)
        self.assertFalse(p['combine_applied']);self.assertFalse(p['cap_applied'])

    def test_saved_report_and_six_exact_unnumbered_panels(self):
        saved,items=pictures();self.assertEqual(saved,json.loads(json.dumps(self.r,default=asdict)))
        counts=[]
        for name,title,stage in items:
            svg=picture(stage,title)
            self.assertEqual(svg,(ROOT/'docs/proofs/posthalf-split-block-comparison'/(name+'.svg')).read_text(encoding='utf-8'))
            doc=ET.fromstring(svg);dots=[n for n in doc.iter() if n.get('class')=='marked-point'];counts.append(len(dots))
            self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()))
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'));scale=float(v.get('width'))/float(v.get('viewBox').split()[2])
                    dots=[n for n in v.iter() if n.get('class')=='marked-point'];self.assertEqual(len(dots),6)
                    for dot in dots:self.assertAlmostEqual(float(dot.get('r'))*scale,1.68)
                    xs=sorted(float(n.get('cx')) for n in dots)
                    for a,b in zip(xs,xs[1:]):self.assertAlmostEqual((b-a)*scale,24.0)
        self.assertEqual(counts,[66,66,48,48,48,24])
if __name__=='__main__':unittest.main()
