import json
from dataclasses import asdict, replace
from hashlib import sha256
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from examples.analyze_posthalf_opposite_block import report
from examples.build_posthalf_opposite_block_comparison import pictures,picture
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
ROOT=Path(__file__).resolve().parents[1]

class OppositeBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()

    def test_exact_source_and_full_six_neighbor_direction(self):
        r=self.r;q=r['route']
        self.assertEqual(r['source_sha256'],sha256((ROOT/'docs/proofs'/r['source_file']).read_bytes()).hexdigest())
        self.assertEqual(tuple(q['stages'][0]['factors']),tuple(r['source_factors']))
        self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['peak_support_word']),(17,17,12))
        self.assertEqual(q['crossed_neighbors'],('cyclic135.supply.2','reflected.exterior','hybrid.first.1','hybrid.first.2','reflected.output.1','posthalf.exterior'))
        b={f.id:f for f in q['stages'][13]['factors']}
        self.assertTrue(all(b[f.id]==f for f in q['actual_ordered_actors']))
        for x in q['full_block_conjugation_matches']:
            self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['raw_target'].word,5))

    def test_mixed_curve_tradeoffs_and_independent_closed_comparison(self):
        r=self.r
        self.assertEqual([(x['old_support'],x['opposite_support']) for x in r['actual_curve_comparisons']],[(10,6),(12,8),(6,4),(4,12)])
        self.assertTrue(all(not x['exact_old_vs_opposite']['equal'] for x in r['actual_curve_comparisons']))
        self.assertEqual(r['route']['stages'][16]['score'],dict(max_support_word=12,total_support_word=49,braid_letters=134))
        self.assertEqual((r['new_late_closed_matrix']['total'],r['new_late_closed_matrix']['maximum']),(20,2))
        self.assertTrue(r['block_product_identity']['faithful_B5_equality']['equal'])
        self.assertFalse(r['adopted'])

    def test_all_raw_crossings_named_inputs_outputs_and_kernels(self):
        q=self.r['route']
        self.assertTrue(all(p['bounded'] for p in q['preapplication_previews']))
        for x in q['actual_adjacent_certificates']:
            self.assertEqual(x['raw_move']['disk_word_certificate']['discrepancy'],())
            self.assertTrue(all(m['exact_disk_equal'] for m in x['individual_presentations']))
        named=[s for s in q['stages'] if 'named_pattern_witness' in s]
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
        for x in q['state_sphere_lift_certificates']:
            self.assertTrue(x['sphere_certificate']['certified'])
            self.assertEqual(x['chosen_lift'],IDENTITY)
            self.assertLessEqual(x['score']['max_support_word'],12)
        cycle=named[-1]['named_pattern_witness']['internal_cyclic_certificate']
        self.assertEqual(cycle['raw_cyclic_discrepancy'],())
        self.assertTrue(all(x['exact_disk_equal'] for x in cycle['independently_known_output_invariance']))
        for s in q['stages']:
            if s['kind']=='disk_cyclic_start':self.assertEqual(s['raw_cyclic_discrepancy'],())

    def test_four_visible_odd_units_and_unchanged_terminal_join(self):
        r=self.r;q=r['route'];p=r['terminal_plan']
        minus=tuple(tuple(-v for v in row) for row in IDENTITY)
        self.assertEqual(len(q['factors']),4)
        for f in q['factors']:
            self.assertEqual((f.points,f.power,f.half),(5,1,False))
            self.assertEqual(homology_action(f.word),minus)
        end={f.id:f for f in q['factors']}
        self.assertTrue(all(end[f.id]==f for f in q['retained_three_exteriors']))
        self.assertTrue(all(x['only_id_changed'] for x in p['id_only_alignment']))
        self.assertEqual(p['combine']['raw_free_word_discrepancy'],())
        self.assertEqual(p['full_cap_discrepancy_word'],p['combine']['local_after'][0].word)
        self.assertFalse(p['combine_applied']);self.assertFalse(p['cap_applied'])
        self.assertEqual((r['posthalf_combined_operations'],r['posthalf_combined_external_checks'],r['complete_source_plan_operations']),(74,55,119))

    def test_saved_exact_report_and_unnumbered_source_exact_panels(self):
        saved,items=pictures()
        self.assertEqual(saved,json.loads(json.dumps(self.r,default=asdict)))
        counts=[]
        for name,title,stage in items:
            svg=picture(stage,title)
            self.assertEqual(svg,(ROOT/'docs/proofs/posthalf-opposite-block-comparison'/(name+'.svg')).read_text(encoding='utf-8'))
            doc=ET.fromstring(svg)
            dots=[n for n in doc.iter() if n.get('class')=='marked-point']
            counts.append(len(dots))
            self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()))
            for row in doc:
                if row.get('data-factor'):
                    v=next(n for n in row if n.tag.endswith('svg'))
                    scale=float(v.get('width'))/float(v.get('viewBox').split()[2])
                    dots=[n for n in v.iter() if n.get('class')=='marked-point']
                    self.assertEqual(len(dots),6)
                    for dot in dots:self.assertAlmostEqual(float(dot.get('r'))*scale,1.68)
                    xs=sorted(float(n.get('cx')) for n in dots)
                    for a,b in zip(xs,xs[1:]):self.assertAlmostEqual((b-a)*scale,24.0)
        self.assertEqual(counts,[66,48,48,24])
if __name__=='__main__':unittest.main()
