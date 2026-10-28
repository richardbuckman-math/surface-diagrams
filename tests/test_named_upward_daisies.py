from pathlib import Path
from dataclasses import replace,asdict
import json,unittest
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.named_upward_daisies import close_upward_daisies,shorten_named_upward_daisies
from surface_diagrams.named_expanded_loan import shorten_expanded_loan_return
from surface_diagrams.named_unaligned_daisies import shorten_named_daisy_closure
from surface_diagrams.named_cyclic_start import shorten_named_cyclic_start
from surface_diagrams.named_disk_frames import shorten_named_disk_frames
from surface_diagrams.early_alternative_transport import transport_alternative_roots
from surface_diagrams.early_alternative_exterior import expose_second_alternative_exterior
from surface_diagrams.early_alternative_closure import close_alternative_boundary

class NamedUpwardDaisyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
  cls.saved=json.loads((cls.folder/'certificate.json').read_text(encoding='utf-8'))
  dec=lambda f:Factor(**dict(f,conjugator=tuple(f['conjugator'])))
  fs=tuple(dec(f) for f in cls.saved['early_boundary']['chart']['factors'])
  a=transport_alternative_roots(fs);b=expose_second_alternative_exterior(a['factors']);c=close_alternative_boundary(b['factors'])
  old=shorten_named_disk_frames(a['stages']+b['stages'][1:]+c['stages'][1:]);old=shorten_named_cyclic_start(old['stages']);old=shorten_named_daisy_closure(old['stages']);cls.old=shorten_expanded_loan_return(old['stages'])
  cls.r=shorten_named_upward_daisies(cls.old['stages']);cls.direct=cls.r['upward_closure_certificate']
 def test_one_operation_and_two_external_checks_are_removed(self):
  r=self.r;d=self.direct
  self.assertEqual((r['previous_whole_named_steps'],r['whole_named_steps'],r['graphical_steps']),(91,90,71))
  self.assertEqual((r['previous_remaining_steps'],r['replacement_steps']),(15,14))
  self.assertEqual((r['previous_adjacent_checks'],r['adjacent_checks']),(110,108))
  self.assertEqual((d['graphical_steps'],d['adjacent_checks'],d['internal_named_adjacent_checks']),(14,19,12))
  self.assertEqual(r['stages'][:58],self.old['stages'][:58]);self.assertEqual(r['actual_peak_support_word'],20)
  self.assertEqual(d['factors'],tuple(Factor(f.id,(),1,5) for f in d['factors']))
 def test_all_new_states_and_atomic_neighbors_are_positive_exact_and_bounded(self):
  peak=0;expected=exact_action(BOUNDARY_WORD*4,5);n=0
  for s in self.direct['stages']:
   for a in (s,)+s.get('atomic_steps',()):
    n+=1;fs=a['factors'];self.assertTrue(all(f.power>0 and not f.half and f.points!=3 for f in fs))
    self.assertEqual(exact_action(product(fs),5),expected);self.assertEqual(homology_action(product(fs)),IDENTITY)
    peak=max(peak,max(len(supported_class(f.mapping_class,5)) for f in fs))
  self.assertEqual(peak,18);self.assertEqual(peak,self.direct['actual_peak_support_word']);self.assertEqual(n,34)
  self.assertEqual(n,len(self.direct['state_sphere_lift_certificates']))
  for c in self.direct['state_sphere_lift_certificates']:self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
  self.assertEqual((self.direct['sphere_moves'],self.direct['exterior_caps'],self.direct['temporary_three_point_factors']),(0,0,0))
 def test_the_frame_is_actual_positive_T45_and_inverse_outer_has_no_reorder(self):
  stages=self.direct['stages'];self.assertEqual(stages[1]['frame'],(4,4))
  for a,b in zip(stages[1]['local_before'],stages[1]['local_after']):
   self.assertEqual(exact_action((4,4)+a.word+(-4,-4),5),exact_action(b.word,5))
  s=stages[3];self.assertTrue(s['inverse_hurwitz_transport']);self.assertEqual(s['adjacent_moves'],3)
  self.assertEqual([a['transported_before'].id for a in s['atomic_steps']],['alternative.residual.O1234']*3)
  self.assertEqual(stages[4]['factors'][3].id,'alternative.second.I35')
 def test_upward_transport_leaves_the_second_outer_unchanged(self):
  stages=self.direct['stages'];start=next(f for f in stages[5]['factors'] if f.id=='alternative.returned.N')
  for s in stages[6:12]:
   actual=next(f for f in s['factors'] if f.id==start.id);self.assertEqual(exact_action(actual.word,5),exact_action(start.word,5))
  moving=stages[7];self.assertEqual(moving['adjacent_moves'],6)
  for a in moving['atomic_steps']:
   self.assertGreater(a['source'],a['target']);self.assertEqual(reduce_word(product(a['local_before'])),reduce_word(product(a['local_after'])))
 def test_explicit_new_cuts_have_free_word_conjugations(self):
  cuts=[]
  for before,s in zip(self.direct['stages'],self.direct['stages'][1:]):
   if s['kind']=='disk_cyclic_start':
    cuts.append(s);g=s['frame'];self.assertEqual(reduce_word(g+product(before['factors'])+inverse_word(g)),reduce_word(product(s['factors'])))
  self.assertEqual(len(cuts),2)
 def test_every_actual_named_input_and_all_kernels_are_retained(self):
  patterns=[s for s in self.direct['stages'] if s['kind'] in ('disk_pc_rose','disk_pc_daisy')]
  self.assertEqual([len(s['local_before']) for s in patterns],[6,5,5]);self.assertEqual([len(s['named_pattern_witness']['retained_interchanges']) for s in patterns],[1,4,7])
  for s in patterns:
   w=s['named_pattern_witness']
   for m in w['individual_matches']:self.assertTrue(m['exact_disk_equal']);self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
   self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
   balance=tuple(sum(f.power for f in s['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in s['local_after'] if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
   self.assertEqual(s['framed_balance_before_minus_after'],balance)
   if s['kind']=='disk_pc_daisy':
    self.assertEqual(len(w['petal_point_pushing']),4)
    for p in w['petal_point_pushing']:self.assertFalse(p.shadow_word)
  second=patterns[-1]['named_pattern_witness'];cyc=second['internal_cyclic_start'];self.assertEqual(cyc['shift'],3)
  self.assertEqual(reduce_word(cyc['frame']+product(cyc['local_before'])+inverse_word(cyc['frame'])),reduce_word(product(cyc['local_after'])))
  self.assertEqual([f.points for f in patterns[-1]['local_before']],[2,2,4,2,2])
 def test_current_saved_proof_is85_with_four_explicit_sphere_moves(self):
  metadata={k:v for k,v in self.r.items() if k not in ('stages','factors')}
  self.assertEqual(json.loads(json.dumps(metadata,default=asdict)),self.saved['named_upward_daisy_shortening'])
  s=self.saved['named_full_route']['summary'];self.assertEqual((s['graphical_steps'],s['sphere_moves'],s['action_only_boundary_recognitions']),(85,4,0));self.assertEqual(s['route_parts'],[17,66,1,1]);self.assertFalse(s['complete_under_twenty_derivation'])
  d=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'));self.assertEqual(len(d['routes']['namedfull']),86)
 def test_changed_sources_are_rejected(self):
  with self.assertRaises(ValueError):shorten_named_upward_daisies(self.old['stages'][:-1])
  source=self.direct['stages'][0]['factors']
  with self.assertRaises(ValueError):close_upward_daisies(source[:-1])
  wrong=list(source);wrong[6]=replace(wrong[6],power=2)
  with self.assertRaises(ValueError):close_upward_daisies(wrong)
