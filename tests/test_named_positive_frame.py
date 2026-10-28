from pathlib import Path
from dataclasses import asdict
import json,unittest
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.named_positive_frame import merge_positive_T45_frame
from surface_diagrams.named_upward_daisies import shorten_named_upward_daisies
from surface_diagrams.named_expanded_loan import shorten_expanded_loan_return
from surface_diagrams.named_unaligned_daisies import shorten_named_daisy_closure
from surface_diagrams.named_cyclic_start import shorten_named_cyclic_start
from surface_diagrams.named_disk_frames import shorten_named_disk_frames
from surface_diagrams.early_alternative_transport import transport_alternative_roots
from surface_diagrams.early_alternative_exterior import expose_second_alternative_exterior
from surface_diagrams.early_alternative_closure import close_alternative_boundary

class NamedPositiveFrameTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
  cls.saved=json.loads((cls.folder/'certificate.json').read_text(encoding='utf-8'))
  fs=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in cls.saved['early_boundary']['chart']['factors'])
  a=transport_alternative_roots(fs);b=expose_second_alternative_exterior(a['factors']);c=close_alternative_boundary(b['factors'])
  r=shorten_named_disk_frames(a['stages']+b['stages'][1:]+c['stages'][1:]);r=shorten_named_cyclic_start(r['stages']);r=shorten_named_daisy_closure(r['stages']);r=shorten_expanded_loan_return(r['stages']);cls.old=shorten_named_upward_daisies(r['stages']);cls.r=merge_positive_T45_frame(cls.old['stages'])
 def test_one_frame_is_removed_with_literal_prefix_rejoin_and_suffix(self):
  r=self.r;old=self.old['stages']
  self.assertEqual((r['previous_whole_named_steps'],r['whole_named_steps'],r['graphical_steps']),(90,89,70))
  self.assertEqual((r['adjacent_checks'],r['previous_adjacent_checks']),(108,108))
  self.assertEqual(r['stages'][:50],old[:50]);self.assertEqual(r['stages'][58:],old[59:]);self.assertEqual(r['stages'][57]['factors'],old[58]['factors'])
  self.assertTrue(r['literal_rejoin']);self.assertEqual(r['factors'],old[-1]['factors'])
 def test_composed_frame_has_the_original_input_and_transports_every_actual_factor(self):
  r=self.r;old=self.old['stages'];self.assertEqual(r['composed_frame'],(4,4,2,3,4,-2,-1))
  first=r['stages'][50];self.assertEqual(first['local_before'],old[49]['factors']);self.assertEqual(first['frame'],r['composed_frame'])
  for i,s in enumerate(r['stages'][50:58],50):
   self.assertEqual(s['source_stage'],old[i])
   for m in s['transported_presentations']:
    self.assertTrue(m['exact_disk_equal']);self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
  for before,after in zip(first['local_before'],first['local_after']):self.assertEqual(exact_action(first['frame']+before.word+inverse_word(first['frame']),5),exact_action(after.word,5))
 def test_all14_changed_states_are_positive_exact_and_support_bounded(self):
  n=0;peak=0;expected=exact_action(BOUNDARY_WORD*4,5)
  for s in self.r['stages'][50:58]:
   for a in (s,)+s.get('atomic_steps',()):
    n+=1;fs=a['factors'];self.assertTrue(all(not f.half and f.power>0 for f in fs))
    self.assertEqual(exact_action(product(fs),5),expected);self.assertEqual(homology_action(product(fs)),IDENTITY)
    peak=max(peak,max(len(supported_class(f.mapping_class,5)) for f in fs))
  self.assertEqual((n,peak),(14,18));self.assertEqual(self.r['changed_peak_support_word'],18);self.assertEqual(self.r['actual_peak_support_word'],20)
  self.assertEqual(len(self.r['changed_state_sphere_lift_certificates']),14)
  for c in self.r['changed_state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
  self.assertEqual((self.r['sphere_moves'],self.r['exterior_caps'],self.r['action_only_boundary_recognitions']),(0,0,0))
 def test_raw_cyclic_conjugations_are_separate_from_normalized_presentations(self):
  cuts=[s for s in self.r['stages'][50:58] if s['kind']=='disk_cyclic_start'];self.assertEqual(len(cuts),2)
  for s in cuts:
   c=s['raw_cyclic_certificate'];self.assertTrue(c['exact_free_word_conjugation'])
   self.assertEqual(reduce_word(c['frame']+product(c['local_before'])+inverse_word(c['frame'])),reduce_word(product(c['local_after'])))
   for m in c['individual_after_presentations']:self.assertTrue(m['exact_disk_equal'])
 def test_all_six_adjacent_raw_checks_and_actual_presentations_are_retained(self):
  atoms=[a for s in self.r['stages'][50:58] for a in s.get('atomic_steps',())];self.assertEqual(len(atoms),6)
  for a in atoms:
   self.assertTrue(a['exact_raw_free_word_equality']);self.assertEqual(reduce_word(product(a['raw_local_before'])),reduce_word(product(a['raw_local_after'])))
   for m in a['transported_presentations']:self.assertTrue(m['exact_disk_equal'])
 def test_actual_daisy_lantern_full_kernels_lifts_and_framed_balances(self):
  daisy=self.r['stages'][51];lantern=self.r['stages'][57]
  self.assertEqual(len(daisy['named_pattern_witness']['outer_match']),1);self.assertEqual(len(daisy['named_pattern_witness']['individual_matches']),4)
  w=lantern['named_pattern_witness'];self.assertEqual(w['source_witness'],self.old['stages'][57]['named_pattern_witness'])
  self.assertEqual(len(w['individual_matches']),3);self.assertEqual(len(w['output_presentation_matches']),3)
  for a,s,e in zip(w['normalized_actual'],w['normalized_actual_splits'],w['canonical_splits']):
   self.assertEqual(exact_action(s.reconstructed_word,5),exact_action(a.word,5));self.assertEqual(s.kernel_loop,e.kernel_loop);self.assertEqual(exact_action(s.shadow_word,4),exact_action(e.shadow_word,4))
  for stage in (daisy,lantern):
   witness=stage['named_pattern_witness']
   for m in witness['individual_matches']:self.assertTrue(m['exact_disk_equal']);self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
   self.assertTrue(witness['sphere_certificate']['certified']);self.assertEqual(witness['chosen_lift_discrepancy'],IDENTITY)
   balance=tuple(sum(f.power for f in stage['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in stage['local_after'] if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
   self.assertEqual(stage['framed_balance_before_minus_after'],balance)
 def test_saved_public_proof_is85_with_four_explicit_sphere_moves(self):
  data={k:v for k,v in self.r.items() if k not in ('stages','factors')}
  self.assertEqual(json.loads(json.dumps(data,default=asdict)),self.saved['named_positive_frame_shortening'])
  s=self.saved['named_full_route']['summary'];self.assertEqual((s['graphical_steps'],s['sphere_moves'],s['action_only_boundary_recognitions']),(85,4,0));self.assertEqual(s['route_parts'],[17,66,1,1]);self.assertFalse(s['complete_under_twenty_derivation'])
  d=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'));self.assertEqual(len(d['routes']['namedfull']),86)
 def test_changed_source_frames_are_rejected(self):
  with self.assertRaises(ValueError):merge_positive_T45_frame(self.old['stages'][:-1])
  bad=list(self.old['stages']);bad[58]=dict(bad[58],frame=(-4,-4))
  with self.assertRaises(ValueError):merge_positive_T45_frame(bad)
  bad=list(self.old['stages']);bad[50]=dict(bad[50],frame=(2,3,4))
  with self.assertRaises(ValueError):merge_positive_T45_frame(bad)
