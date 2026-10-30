import json,re,unittest
from pathlib import Path
from dataclasses import asdict
from hashlib import sha256
from copy import deepcopy
import xml.etree.ElementTree as ET
from surface_diagrams.small_fibration_derivations import (all_derivations,source_factors,cable_pure_word,source_panel)
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.braid_actions import reduce_word,inverse_word
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.sphere_actions import sphere_supported_class
from surface_diagrams._fibration_source_records import SOURCE_RECORDS
from examples.analyze_fibration_derivations import reports
ROOT=Path(__file__).resolve().parents[1]

class SmallFibrationDerivationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rs=all_derivations()
    def test_all_three_actual_types_close_in_separate_sphere_and_chosen_lift_checks(self):
        for slug,r in self.rs.items():
            self.assertTrue(r['complete']);self.assertTrue(r['terminal_sphere_certificate']['certified'])
            self.assertEqual(r['terminal_chosen_lift'],IDENTITY)
            self.assertEqual(r['profile'],tuple(map(int,slug.split('-'))))
            self.assertTrue(all(f.power>0 for s in r['stages'] for f in s['factors']))
        self.assertEqual([len(r['factors']) for r in self.rs.values()],[8,7,20])
    def test_six_two_actual_block_rotation_and_eight_raw_crossings(self):
        r=self.rs['6-2'];self.assertEqual((r['operations'],r['adjacent_checks']),(5,8))
        self.assertTrue(r['stages'][1]['actual_rotation_match']['exact_disk_equal'])
        self.assertTrue(all(x['exact_disk_equal'] for x in r['stages'][1]['actual_block_exchange_matches']))
        self.assertEqual(r['local_peak']['maximum'],9)
        self.assertTrue(all(x['exact_disk_equal'] for x in r['source_individual_matches']))
    def test_four_three_retains_and_cancels_identical_positive_compensation_on_both_sides(self):
        r=self.rs['4-3'];self.assertEqual((r['operations'],r['adjacent_checks']),(15,15))
        cancels=[s for s in r['stages'] if s['kind']=='cancel_common_compensation'];self.assertEqual(len(cancels),1)
        c=cancels[0];self.assertEqual(c['common_prefix'][0].power,4)
        self.assertEqual(exact_action(product(c['before_factors']),5),exact_action(product(c['before_target']),5))
        self.assertEqual(exact_action(product(c['factors']),5),exact_action(product(c['after_target']),5))
        self.assertFalse(any(s['kind']=='sphere_redraw' for s in r['stages']))
        for s in r['stages']:
            if 'new positive correction' in s['title']:
                self.assertTrue(all(not f.half for a in s['atomic_steps'] for f in a['raw_move']['local_before']))
        self.assertTrue(all(x['exact_disk_equal'] for x in r['source_individual_matches']))
    def test_named_cabled_daisy_is_derived_from_complete_canonical_daisy_and_explicit_parallel_copy(self):
        w=self.rs['4-3']['stages'][1]['full_named_cabled_daisy_proof']
        self.assertEqual(len(w['retained_three_internal_hurwitz']),3)
        self.assertTrue(all(not a['disk_word_certificate']['discrepancy'] for a in w['retained_three_internal_hurwitz']))
        self.assertTrue(all(x['exact_disk_equal'] for x in w['all_four_source_petal_matches']))
        self.assertTrue(all(x['exact_disk_equal'] for x in w['individually_known_pair_corrections']))
        self.assertTrue(w['outer_correction']['exact_disk_equal'])
        q=cable_pure_word(Factor('D4',(),1,4).word,4,4)
        self.assertEqual(q['final_labels'],(1,2,3,4))
        with self.assertRaises(ValueError):cable_pure_word((3,),4,4)
        inverse=cable_pure_word(inverse_word(Factor('D4',(),1,4).word),4,4)
        self.assertEqual(exact_action(inverse['word'],5),exact_action(inverse_word(q['word']),5))
    def test_ten_ten_uses_original_exact_blocks_and_preserves_failed_drawing_edits_separately(self):
        r=self.rs['10-10'];self.assertEqual((r['operations'],r['listed_operations'],r['adjacent_checks']),(11,13,24))
        self.assertTrue(all(x['exact_disk_equal'] for x in r['source_block_certificates']))
        bad=r['excluded_reviewed_drawing_data'];self.assertFalse(bad['adopted']);self.assertNotEqual(bad['homology'],IDENTITY)
        self.assertNotEqual(bad['source_start'],r['stages'][0]['factors'])
        self.assertEqual([x['position'] for x in bad['individual_original_vs_edited_comparisons'] if not x['equal']],[6,13,19,20])
        self.assertTrue(r['unrelated_dictation_seed_unchanged'])
        self.assertEqual(r['local_peak']['maximum'],16)
    def test_three_parallel_rotations_share_one_input_and_have_literal_two_order_witnesses(self):
        s=self.rs['10-10']['stages'][1];self.assertEqual(s['move_count'],3)
        self.assertTrue(all(c['before']==s['input_factors'] for c in s['parallel_cards']))
        self.assertEqual(len(s['independence_witnesses']),3)
        for w in s['independence_witnesses']:
            self.assertTrue(w['literal_two_order_equality']);self.assertEqual(w['left_then_right'],w['right_then_left'])
    def test_sphere_redraw_only_retains_actual_curve_identity_power_and_full_context(self):
        r=self.rs['10-10'];i=next(i for i,s in enumerate(r['stages']) if s['kind']=='sphere_redraw');s=r['stages'][i]
        a,b=s['local_before'][0],s['local_after'][0]
        self.assertEqual((a.id,a.power,a.half),(b.id,b.power,b.half))
        self.assertEqual(sphere_supported_class(a.mapping_class),sphere_supported_class(b.mapping_class))
        full=reduce_word(product(r['stages'][i-1]['factors'])+inverse_word(product(s['factors'])))
        self.assertEqual(full,s['full_disk_discrepancy']);self.assertTrue(s['full_context_sphere_certificate']['certified'])
        self.assertNotEqual(exact_action(a.word,6),exact_action(b.word,6))
        self.assertEqual(homology_action(full),IDENTITY)
        self.assertEqual(r['stages'][i+1]['kind'],'disk_named_substitution')
        old={f.id:f for f in r['stages'][i-1]['factors']};new={f.id:f for f in r['factors']};outside=set(old)-{a.id,r['stages'][i-1]['factors'][14].id}
        self.assertEqual(len(outside),17);self.assertTrue(all(old[k]==new[k] for k in outside))
        w=r['stages'][i+1]['full_named_cabled_half_lantern_proof']
        self.assertEqual(w['raw_cyclic_discrepancy'],());self.assertEqual(w['explicit_internal_hurwitz']['disk_word_certificate']['discrepancy'],())
        self.assertTrue(all(x['exact_disk_equal'] for x in w['every_source_output_match']))
    def test_embedding_keeps_actual_five_point_target_and_does_not_assume_B6_centrality(self):
        s=next(s for s in self.rs['10-10']['stages'] if s['kind']=='construction_embedding')
        self.assertEqual((s['source_points'],s['target_points'],s['offset']),(5,6,1))
        self.assertEqual((s['target'][0].first,s['target'][0].points,s['target'][0].power),(2,5,6))
        target=product(s['target']);self.assertNotEqual(exact_action((1,)+target,6),exact_action(target+(1,),6))
    def test_every_external_raw_crossing_is_reconstructed_and_bounded_before_application(self):
        for r in self.rs.values():
            for s in r['stages']:
                for a in s.get('atomic_steps',()):
                    raw=a['raw_move'];self.assertEqual(raw['disk_word_certificate']['discrepancy'],())
                    self.assertEqual(reduce_word(product(raw['local_before'])+inverse_word(product(raw['local_after']))),())
                    self.assertTrue(a['individual_presentation']['exact_disk_equal']);self.assertTrue(a['bounded_before_application'])
                    self.assertLessEqual(a['raw_support_score']['maximum'],20)
                    self.assertLessEqual(a['score']['maximum'],20)
    def test_full_kernels_are_retained_and_moving_last_halves_are_never_deleted(self):
        skipped=0;applicable=0
        for r in self.rs.values():
            for s in r['stages']:
                for w in s.get('local_kernels',())+s.get('every_actual_factor_kernel',()):
                    if w['applicable']:
                        applicable+=1;self.assertTrue(w['reconstructed']['exact_disk_equal'])
                        self.assertEqual(exact_action(w['source_word'],w['strands']),exact_action(w['split'].reconstructed_word,w['strands']))
                    else:skipped+=1;self.assertIn('last strand moves',w['reason'])
        self.assertGreater(skipped,0);self.assertGreater(applicable,0)
    def test_copied_sources_and_generated_native_records_are_exact_and_portable(self):
        folder=ROOT/'docs/proofs/fibration-sources/planar-mcg-2026-10-30';m=json.loads((folder/'provenance.json').read_bytes())
        self.assertIsNone(m['source_commit'])
        for x in m['files']:self.assertEqual(sha256((folder/x['archive_relative_path']).read_bytes()).hexdigest(),x['sha256'])
        self.assertEqual(json.loads((folder/'factor-records.json').read_bytes()),SOURCE_RECORDS)
        for slug,r in reports():self.assertEqual(json.loads(json.dumps(r,default=asdict)),json.loads((ROOT/'docs/proofs/fibration-derivations'/(slug+'.json')).read_bytes()))
    def test_all_three_viewers_keep_six_unnumbered_support_points_and_exact_connected_braids(self):
        for slug in self.rs:
            p=json.loads((ROOT/'docs/proofs/fibration-derivations'/(slug+'.display.json')).read_bytes())
            self.assertEqual(len(p['states']),self.rs[slug]['operations']+1)
            for row in p['rows']:
                doc=ET.fromstring(p['supports'][row['support']]);dots=[x for x in doc.iter() if x.get('class')=='marked-point']
                self.assertEqual(len(dots),6);self.assertFalse(any(x.get('class')=='marked-point-label' for x in doc.iter()))
                scale=float(doc.get('width'))/float(doc.get('viewBox').split()[2]);xs=sorted(float(x.get('cx')) for x in dots)
                for a,b in zip(xs,xs[1:]):self.assertAlmostEqual((b-a)*scale,24,places=4)
                for x in dots:self.assertAlmostEqual(float(x.get('r'))*scale,1.68,places=4)
                b=p['braids'][row['braid']];self.assertIn('data-word="'+' '.join(map(str,row['word']))+'"',b)
                self.assertEqual(int(re.search(r'height="(\d+)"',b).group(1)),row['height'])
    def test_older_dictation_stays_a_distinct_nonclosing_twenty_factor_seed(self):
        from surface_diagrams.ten_ten import transcription_certificate,TEN_TEN_FACTORS
        self.assertEqual(len(TEN_TEN_FACTORS),20);self.assertFalse(transcription_certificate()['homology_identity'])
        self.assertNotEqual(product(TEN_TEN_FACTORS),product(self.rs['10-10']['factors']))

if __name__=='__main__':unittest.main()
