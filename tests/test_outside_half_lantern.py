from dataclasses import asdict,replace
from pathlib import Path
import json
import unittest
from examples.analyze_outside_half_lantern import report
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.outside_half_lantern import reach_outside_half_lantern

class OutsideHalfLanternTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=report();cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
 def test_every_retained_state_is_bounded_positive_disk_sphere_and_lift_exact(self):
  for key,steps,peak in (('preferred',11,13),('original_chart',10,19)):
   r=self.r[key];self.assertEqual((r['graphical_operations'],r['adjacent_checks']),(steps,16))
   maximum=0
   for s in r['stages']:
    for a in (s,)+s.get('atomic_steps',()):
     fs=a['factors'];self.assertTrue(all(f.power>0 for f in fs))
     self.assertEqual(exact_action(product(fs),5),exact_action(BOUNDARY_WORD*4,5))
     self.assertEqual(homology_action(product(fs)),IDENTITY)
     maximum=max(maximum,max(len(supported_class(f.mapping_class,5)) for f in fs))
   self.assertEqual((maximum,r['peak_support_word']),(peak,peak))
   for c in r['state_sphere_lift_certificates']:
    self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
   self.assertEqual(r['sphere_moves'],0);self.assertEqual(r['exterior_caps'],0)
 def test_both_original_halves_are_absorbed_without_introducing_any_auxiliary_half(self):
  for key in ('preferred','original_chart'):
   r=self.r[key]
   for s in r['stages'][:-1]:self.assertEqual({f.id for f in s['factors'] if f.half},{'F6','F11'})
   self.assertFalse(any(f.half for f in r['factors']));self.assertEqual(len(r['factors']),17)
   w=r['stages'][-1]['named_pattern_witness']
   self.assertEqual(tuple(f.id for f in r['stages'][-1]['local_before']),('F6','F11','outside.Q.square'))
   self.assertEqual(w['supplied_square_ancestry'],('one.unit.Q2','outside.rose.0'))
   self.assertEqual(w['unselected_preconditioner'],'one.unit.Q1')
   self.assertTrue(w['applied']);self.assertFalse(w['requires_gathering'])
   self.assertEqual(r['half_twists_introduced'],0)
 def test_actual_ordered_local_relation_matches_each_canonical_input(self):
  for key in ('preferred','original_chart'):
   s=self.r[key]['stages'][-1];w=s['named_pattern_witness']
   for m in w['individual_matches']:
    self.assertTrue(m['exact_disk_equal']);self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
   self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
   wrong=s['local_before'][1:2]+s['local_before'][:1]+s['local_before'][2:]
   self.assertNotEqual(exact_action(product(wrong),5),exact_action(product(s['local_after']),5))
   self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
   self.assertFalse(w['half_twist_framed_boundary_lift_asserted'])
   wanted=tuple(sum(f.power for f in w['parent_pc_rose'] if i in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in s['local_after'] if i in enclosed_boundaries(f.mapping_class,5)) for i in range(1,6))
   self.assertEqual(w['parent_framing_balance'],wanted)
 def test_outside_donor_is_an_actual_round_root_with_an_individually_matched_unit(self):
  s=self.r['preferred']['stages'][4]
  self.assertEqual(s['local_before'],(Factor('alternative.R2',(),1,3),))
  self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
  match=s['named_pattern_witness']['supplied_unit_match'][0]
  self.assertEqual(match['actual'].id,'outside.rose.0');self.assertEqual(match['pattern'].id,'one.unit.Q2')
  self.assertEqual(exact_action(match['actual'].word,5),exact_action(match['pattern'].word,5))
  self.assertEqual(s['framed_balance_before_minus_after'],(-1,-1,-1,0,0))
 def test_cyclic_starts_and_common_frame_are_actual_ordered_conjugations(self):
  for key in ('preferred','original_chart'):
   r=self.r[key];cycles=0
   for i,s in enumerate(r['stages'][1:],1):
    if s['kind']=='disk_cyclic_start':
     cycles+=1;g=s['frame']
     self.assertEqual(reduce_word(g+product(r['stages'][i-1]['factors'])+inverse_word(g)),reduce_word(product(s['factors'])))
    if s['kind']=='global_conjugation':
     for a,b in zip(s['local_before'],s['local_after']):self.assertEqual(exact_action(s['frame']+a.word+inverse_word(s['frame']),5),exact_action(b.word,5))
   self.assertEqual(cycles,2)
 def test_endpoint_nonabelian_kernels_and_chart_equivalence_are_retained(self):
  for key in ('preferred','original_chart'):
   for k in self.r[key]['endpoint_point_pushing']:
    self.assertEqual(exact_action(k['factor'].word,5),exact_action(k['split'].reconstructed_word,5))
  for key in ('preferred','original_chart'):
   t=self.r[key]['next_rose_return'];self.assertFalse(t['applied']);self.assertTrue(t['requires_transport'])
   for m in t['actual_Q1_middle_match']+t['unit_donor_match']+t['restore_individual_matches']:
    self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
   self.assertEqual(exact_action(t['actual_new_root'].word,5),exact_action(product(t['internal_rose']),5))
  h=(3,4,4)
  for a,b in zip(self.r['original_chart']['factors'],self.r['preferred']['factors']):
   self.assertEqual(a.id,b.id);self.assertEqual(exact_action(h+a.word+inverse_word(h),5),exact_action(b.word,5))
  self.assertEqual(self.r['preferred']['curve_intersections'],dict(maximum=46,total=878,pairs=136))
  self.assertEqual(self.r['preferred']['curve_intersections'],self.r['original_chart']['curve_intersections'])
 def test_saved_report_is_exact_and_no_complete_shortening_is_claimed(self):
  p=self.folder.parent/'six-seven-outside-half-lantern.json'
  self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),json.loads(p.read_text(encoding='utf-8')))
  r=self.r['preferred'];self.assertEqual(r['after_score'],dict(max_support_word=13,total_support_word=117,braid_letters=174))
  self.assertEqual((r['working_prefix_operations'],self.r['original_chart']['working_prefix_operations']),(50,49))
  self.assertFalse(r['complete_shorter_derivation']);self.assertFalse(self.r['public_graphical_payloads_changed'])
  c=json.loads((self.folder/'certificate.json').read_text(encoding='utf-8'))
  self.assertEqual(c['named_full_route']['summary']['graphical_steps'],82)
 def test_bad_sources_and_nonboolean_chart_options_are_rejected(self):
  fs=self.r['preferred']['stages'][0]['factors']
  for bad in (fs[:-1],(replace(fs[0],id='wrong'),)+fs[1:]):
   with self.assertRaises(ValueError):reach_outside_half_lantern(bad)
  for option in (0,1,None,'yes'):
   with self.assertRaises(ValueError):reach_outside_half_lantern(fs,round_chart=option)

if __name__=='__main__':unittest.main()
