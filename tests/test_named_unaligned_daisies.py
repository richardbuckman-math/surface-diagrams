from pathlib import Path
import json,unittest
from surface_diagrams.early_alternative_transport import transport_alternative_roots
from surface_diagrams.early_alternative_exterior import expose_second_alternative_exterior
from surface_diagrams.early_alternative_closure import close_alternative_boundary
from surface_diagrams.named_disk_frames import shorten_named_disk_frames
from surface_diagrams.named_cyclic_start import shorten_named_cyclic_start
from surface_diagrams.named_unaligned_daisies import close_unaligned_daisies,shorten_named_daisy_closure
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD

class NamedUnalignedDaisyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
  cls.saved=json.loads((cls.folder/'certificate.json').read_text(encoding='utf-8'))
  fs=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in cls.saved['early_boundary']['chart']['factors'])
  a=transport_alternative_roots(fs);b=expose_second_alternative_exterior(a['factors']);c=close_alternative_boundary(b['factors'])
  framed=shorten_named_disk_frames(a['stages']+b['stages'][1:]+c['stages'][1:])
  cls.old=shorten_named_cyclic_start(framed['stages']);cls.r=shorten_named_daisy_closure(cls.old['stages'])
  cls.direct=cls.r['direct_closure_certificate']
 def test_six_real_operations_are_bypassed_and_the_four_exteriors_are_kept(self):
  r=self.r;d=self.direct
  self.assertEqual((r['previous_whole_named_steps'],r['whole_named_steps'],r['operations_removed']),(98,92,6))
  self.assertEqual((r['graphical_steps'],r['previous_remaining_steps'],r['replacement_steps']),(73,17,11))
  self.assertEqual(r['stages'][:63],self.old['stages'][:63])
  self.assertFalse(d['outer_alignment_performed']);self.assertFalse(d['four_point_square_created'])
  self.assertFalse(any(s['kind']=='disk_combine' for s in d['stages']))
  self.assertEqual(d['common_frame'],(-4,-3,-2))
  self.assertEqual(len(r['factors']),4)
  for f in r['factors']:self.assertEqual(f,Factor(f.id,(),1,5))
 def test_every_direct_state_and_neighbor_is_positive_exact_and_bounded(self):
  peak=0;expected=exact_action(BOUNDARY_WORD*4,5)
  for s in self.direct['stages']:
   for a in (s,)+s.get('atomic_steps',()):
    fs=a['factors'];self.assertTrue(all(not f.half and f.power>0 for f in fs))
    self.assertEqual(exact_action(product(fs),5),expected);self.assertEqual(homology_action(product(fs)),IDENTITY)
    self.assertTrue(all(f.power==1 for f in fs if f.points==4))
    peak=max(peak,max(len(supported_class(f.mapping_class,5)) for f in fs))
  self.assertEqual((peak,self.direct['actual_peak_support_word']),(16,16))
  self.assertEqual(self.r['actual_peak_support_word'],20)
  for c in self.direct['state_sphere_lift_certificates']:
   self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
  self.assertEqual((self.direct['sphere_moves'],self.direct['exterior_caps']),(0,0))
 def test_both_daisies_match_each_actual_input_with_every_internal_check_retained(self):
  stages=[s for s in self.direct['stages'] if s['kind']=='disk_pc_daisy'];self.assertEqual(len(stages),2)
  for s,count in zip(stages,(4,7)):
   w=s['named_pattern_witness'];self.assertEqual(len(w['retained_interchanges']),count)
   self.assertEqual(len(w['individual_matches']),5)
   for m in w['individual_matches']:
    self.assertTrue(m['exact_disk_equal']);self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
   for m in w['retained_interchanges']:
    self.assertEqual(exact_action(product(m['local_before']),5),exact_action(product(m['local_after']),5))
   self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
   self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
   wanted=tuple(sum(f.power for f in s['local_before'] if i in enclosed_boundaries(f.mapping_class,5))-1 for i in range(1,6))
   self.assertEqual(s['framed_balance_before_minus_after'],wanted)
  self.assertEqual(stages[0]['local_before'][0].conjugator,())
  self.assertNotEqual(stages[1]['local_before'][0].conjugator,())
 def test_second_daisy_retains_full_nonabelian_loops_not_only_point_sets(self):
  s=self.direct['stages'][-1];w=s['named_pattern_witness'];splits=w['petal_point_pushing']
  self.assertEqual(tuple(k.kernel_loop for k in splits),((1,),(1,-4,-3,-4,-3,4,3,4,3,4,-1),(1,-4,-3,-4,3,4,3,4,-1),(1,2,-1)))
  for f,k in zip(w['normalized_actual'][1:],splits):
   self.assertEqual(k.shadow_word,());self.assertEqual(exact_action(f.word,5),exact_action(k.reconstructed_word,5))
 def test_each_ordered_transition_and_cyclic_start_is_an_explicit_disk_certificate(self):
  for i,s in enumerate(self.direct['stages'][1:],1):
   before=product(self.direct['stages'][i-1]['factors']);after=product(s['factors'])
   if s['kind'] in ('disk_cyclic_start','global_conjugation'):
    before=s['frame']+before+inverse_word(s['frame'])
   self.assertEqual(exact_action(before,5),exact_action(after,5))
   if s['kind']=='disk_cyclic_start':self.assertEqual(reduce_word(before),reduce_word(after))
 def test_current_public_proof_has79_operations_four_sphere_moves_and_no_action_recognition(self):
  summary=self.saved['named_full_route']['summary']
  self.assertEqual((summary['graphical_steps'],summary['mathematical_steps_saved']),(79,3))
  self.assertEqual(summary['route_parts'],[14,63,1,1]);self.assertEqual(summary['sphere_moves'],4)
  self.assertEqual((summary['equivariant_frame_operations_removed'],summary['historical_frame_component_operations_removed'],summary['raw_closure_operations_removed']),(1,2,9))
  self.assertEqual(summary['action_only_boundary_recognitions'],0);self.assertFalse(summary['complete_under_twenty_derivation'])
  shown=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'))
  self.assertEqual(len(shown['routes']['namedfull']),80);self.assertEqual(len(shown['routes']['earlyaltclosed']),24)
 def test_bad_sources_are_rejected(self):
  with self.assertRaises(ValueError):shorten_named_daisy_closure(self.old['stages'][:-1])
  with self.assertRaises(ValueError):close_unaligned_daisies(self.direct['stages'][0]['factors'][:-1])
