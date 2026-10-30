import json
from copy import deepcopy
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from examples.analyze_preferred_late45 import report
from examples.build_preferred_late45_comparison import pictures,picture
from surface_diagrams.clarity_derivation import preferred_clarity_source,refine_sphere_moves,parallel_rounds,factor_from_data
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.six_seven_structure import research_hurwitz_move
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'docs/proofs/six-seven-fifty-blocks'

class PreferredLate45Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=report();cls.raw=json.loads((FOLDER/'certificate.json').read_bytes())
        cls.meeting=json.loads((FOLDER.parent/'six-seven-fixed-half-meeting.json').read_bytes())
        cls.saved=json.loads((FOLDER.parent/'six-seven-preferred-late45.json').read_bytes())
        cls.active=preferred_clarity_source(cls.raw,cls.meeting,cls.saved)
        cls.refined=refine_sphere_moves(cls.active['stages'],cls.raw['early_boundary']['chart']['factor_certificates'])
        cls.rounds=parallel_rounds(cls.refined['stages'])

    def test_actual_loan_return_and_only_two_changed_source_curves(self):
        r=self.r;q=r['route']
        self.assertEqual((q['graphical_operations'],q['adjacent_checks'],q['named_substitutions']),(8,14,3))
        self.assertTrue(q['returned_parent_literal']);self.assertEqual(q['internal_power'],-1)
        self.assertEqual(set(q['changed_source_ids']),{'alternative.P24','direct.E2'})
        self.assertEqual(len(q['actual_loan_crossed_neighbors']),10)
        self.assertEqual(q['actual_round45_loan'].conjugator,())
        changes=[x for x in r['source_record_comparisons'] if not x['literal_equal']]
        self.assertEqual([(x['before_support'],x['after_support']) for x in changes],[(6,2),(4,2)])
        self.assertEqual(sum(x['literal_equal'] for x in r['source_record_comparisons']),6)
        self.assertEqual(r['changed_closed_pairs'],())
        self.assertEqual((r['before_closed_matrix']['total'],r['before_closed_matrix']['maximum']),(20,2))
        self.assertEqual((r['after_closed_matrix']['total'],r['after_closed_matrix']['maximum']),(20,2))

    def test_all_three_derived_donor_charts_and_explicit_temporary_cost(self):
        r=self.r
        self.assertEqual([(v['internal_power'],v['peak']['max_support_word'],v['peak']['total_support_word']) for v in r['variant_peaks']],[(0,7,42),(-1,6,42),(-2,6,48)])
        self.assertTrue(all(v['late_literal_join'] for v in r['variant_peaks']))
        self.assertEqual(r['chosen_peak_rows'],11)
        self.assertEqual(r['chosen_peak'],dict(max_support_word=6,total_support_word=42,braid_letters=110))
        self.assertEqual(r['route']['stages'][7]['score'],dict(max_support_word=5,total_support_word=27,braid_letters=88))
        self.assertEqual((r['old_closure_operations'],r['old_closure_adjacent_checks']),(3,2))

    def test_every_actual_crossing_and_named_input_output_keeps_full_witnesses(self):
        for q in (self.r['route'],self.r['unselected_original_chart'],self.r['unselected_inverse_full_chart']):
            self.assertTrue(all(p['bounded'] for p in q['preapplication_previews']))
            for c in q['actual_adjacent_certificates']:
                self.assertEqual(c['raw_move']['disk_word_certificate']['discrepancy'],())
                self.assertTrue(all(x['exact_disk_equal'] for x in c['individual_presentations']))
            for s in q['stages']:
                if s['kind']=='disk_cyclic_start':self.assertEqual(s['raw_cyclic_discrepancy'],())
                if 'named_pattern_witness' not in s:continue
                w=s['named_pattern_witness']
                self.assertTrue(all(x['exact_disk_equal'] for x in w['individual_matches']+w['individual_output_matches']))
                self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
                self.assertEqual(len(s['framed_balance_before_minus_after']),5)
                self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
                for x in w['complete_actual_and_normalized_point_pushing']:
                    self.assertEqual(exact_action(x['actual'].word,5),exact_action(x['split'].reconstructed_word,5))
        q=self.r['route'];self.assertTrue(all(not f.half and f.power==1 for s in q['stages'] for f in s['factors']))
        self.assertTrue(all(x['score']['max_support_word']<=6 and x['chosen_lift']==IDENTITY and x['sphere_certificate']['certified'] for x in q['state_sphere_lift_certificates']))

    def test_source_wrapper_literal_joins_actual_combine_and_historical_flags(self):
        a=self.active['late45_adoption'];r=self.r
        self.assertTrue(a['adopted']);self.assertFalse(self.saved['adopted'])
        self.assertEqual((a['previous_source_operations'],a['source_operations']),(85,90))
        self.assertEqual((a['previous_interval'],a['current_interval']),((80,83),(80,88)))
        self.assertEqual((a['previous_local_moves'],a['current_local_moves'],a['previous_adjacent_checks'],a['current_adjacent_checks']),(3,8,2,14))
        self.assertTrue(a['literal_input_join']);self.assertTrue(a['literal_fourth_power_join'])
        self.assertEqual(a['raw_actual_four_unit_combine_discrepancy'],())
        self.assertEqual(a['full_cap_discrepancy_word'],self.active['stages'][-2]['factors'][0].word)
        self.assertEqual(a['source_sha256'],sha256((FOLDER.parent/'six-seven-preferred-late45.json').read_bytes()).hexdigest())
        self.assertFalse(r['terminal_plan']['combine_applied']);self.assertFalse(r['terminal_plan']['cap_applied'])
        self.assertTrue(all(x['only_id_changed'] for x in r['terminal_plan']['id_only_ancestry_alignment']))
        minus=tuple(tuple(-x for x in row) for row in IDENTITY)
        self.assertTrue(all(homology_action(f.word)==minus and f.points==5 and f.power==1 for f in r['route']['factors']))

    def test_refinement_keeps_thirteen_full_words_and_correct_parallel_inputs(self):
        q=self.refined;self.assertEqual((q['source_operations'],q['clarified_moves'],len(self.rounds),q['sphere_redraw_moves']),(90,106,75,13))
        old=json.loads((FOLDER/'clarity-half-meeting-certificate.json').read_bytes())
        self.assertEqual([list(s['disk_discrepancy']) for s in q['stages'] if s['kind']=='sphere_redraw'],[s['disk_discrepancy'] for s in old['stages'] if s['kind']=='sphere_redraw'])
        first=next(g for g in self.rounds if any(q['stages'][c['move_index']].get('source_witness_ref')=='six-seven-preferred-late45.json:route.stages.1' for c in g['cards']))
        self.assertEqual(first['move_count'],1)
        returning=next(g for g in self.rounds if any(q['stages'][c['move_index']].get('source_witness_ref')=='six-seven-preferred-late45.json:route.stages.5' for c in g['cards']))
        self.assertEqual(returning['move_count'],2);self.assertTrue(returning['simultaneous'])
        self.assertTrue(all(c['before']==returning['before'] for c in returning['cards']))
        self.assertTrue(all(w['literal_two_order_equality'] for w in returning['independence_witnesses']))
        lantern=next(s for s in q['stages'] if s['kind']=='disk_lantern')
        self.assertEqual(len(lantern['individual_named_matches']),3)
        bad=deepcopy(self.active['stages']);bad[13]['factors']=research_hurwitz_move(bad[13]['factors'],0,1)['factors']
        with self.assertRaisesRegex(ValueError,'individual input match'):
            refine_sphere_moves(bad,self.raw['early_boundary']['chart']['factor_certificates'])

    def test_report_flags_cannot_substitute_for_actual_recomputed_state_checks(self):
        bad=deepcopy(self.saved);bad['route']['stages'][3]['atomic_steps'][0]['target']+=1
        with self.assertRaises(ValueError):preferred_clarity_source(self.raw,self.meeting,bad)
        bad=deepcopy(self.saved);bad['route']['stages'][5]['factors'][0]['power']+=1
        with self.assertRaises(ValueError):preferred_clarity_source(self.raw,self.meeting,bad)
        bad=deepcopy(self.saved);bad['terminal_plan']['combine']['local_before'][0]['power']+=1
        with self.assertRaises(ValueError):preferred_clarity_source(self.raw,self.meeting,bad)
        bad=deepcopy(self.saved);bad['terminal_plan']['full_cap_discrepancy_word'].pop()
        with self.assertRaises(ValueError):preferred_clarity_source(self.raw,self.meeting,bad)

    def test_previous_101_71_edition_is_exactly_pinned_and_reproducible(self):
        pins={'clarity-half-meeting-certificate.json':'b7d253b9044695f5653b91f11c14cf0e8d2ec5be4c35e1a5a816ec789a9d513b','display-half-meeting.json':'0010fce9eeef3e1d20af49e0bc34f5401879b2c3411205211bf39470e3ece030','six-seven-named-half-meeting.pdf':'d2ed78a6910762ef6db95e3dcb4c6c196b21cce76535f5eb4ae8764cf59f95a0'}
        for name,h in pins.items():self.assertEqual(sha256((FOLDER/name).read_bytes()).hexdigest(),h)
        manifest=json.loads((FOLDER/'clarity-half-meeting-archive.json').read_bytes())
        for f in manifest['files']:self.assertEqual(sha256((FOLDER/f['archive']).read_bytes()).hexdigest(),f['sha256'])
        old=preferred_clarity_source(self.raw,self.meeting);ref=refine_sphere_moves(old['stages'],self.raw['early_boundary']['chart']['factor_certificates'])
        saved=json.loads((FOLDER/'clarity-half-meeting-certificate.json').read_bytes())
        self.assertEqual(json.loads(json.dumps(ref['stages'],default=asdict)),saved['stages'])
        self.assertEqual((len(old['stages'])-1,ref['clarified_moves'],len(parallel_rounds(ref['stages']))),(85,101,71))
        old_display=json.loads((FOLDER/'display-half-meeting.json').read_bytes());current=json.loads((FOLDER/'display-clear.json').read_bytes())
        self.assertEqual(current['routes']['clearfull'][:66],old_display['routes']['clearfull'][:66])
        html=(FOLDER/'half-meeting.html').read_text(encoding='utf-8')
        self.assertIn('display-half-meeting.json',html);self.assertNotIn('display-clear.json',html)

    def test_saved_report_and_six_exact_unnumbered_panels(self):
        r,items=pictures();self.assertEqual(r,json.loads(json.dumps(self.r,default=asdict)))
        counts=[];rows=[]
        for name,title,stage in items:
            svg=picture(stage,title);self.assertEqual(svg,(ROOT/'docs/proofs/preferred-late45-comparison'/(name+'.svg')).read_text(encoding='utf-8'))
            doc=ET.fromstring(svg);points=[n for n in doc.iter() if n.get('class')=='marked-point'];counts.append(len(points))
            self.assertFalse(any(n.get('class')=='marked-point-label' for n in doc.iter()))
            extracted={}
            for row in doc:
                if not row.get('data-factor'):continue
                v=next(n for n in row if n.tag.endswith('svg'));scale=float(v.get('width'))/float(v.get('viewBox').split()[2])
                dots=[n for n in v.iter() if n.get('class')=='marked-point'];self.assertEqual(len(dots),6)
                for dot in dots:self.assertAlmostEqual(float(dot.get('r'))*scale,1.68)
                xs=sorted(float(n.get('cx')) for n in dots)
                for a,b in zip(xs,xs[1:]):self.assertAlmostEqual((b-a)*scale,24.0)
                extracted[row.get('data-factor')]=(v.get('viewBox'),v.get('width'),v.get('height'),tuple(ET.tostring(x) for x in v))
            rows.append(extracted)
        self.assertEqual(counts,[48,66,66,48,48,24])
        unchanged={x['id'] for x in self.r['source_record_comparisons'] if x['literal_equal']}
        self.assertEqual(len(unchanged),6)
        self.assertTrue(all(rows[0][n]==rows[3][n] for n in unchanged))
if __name__=='__main__':unittest.main()
