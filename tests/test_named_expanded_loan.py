from pathlib import Path
from dataclasses import replace,asdict
import json,unittest
from surface_diagrams.early_alternative_transport import transport_alternative_roots
from surface_diagrams.early_alternative_exterior import expose_second_alternative_exterior
from surface_diagrams.early_alternative_closure import close_alternative_boundary
from surface_diagrams.named_disk_frames import shorten_named_disk_frames
from surface_diagrams.named_cyclic_start import shorten_named_cyclic_start
from surface_diagrams.named_unaligned_daisies import shorten_named_daisy_closure
from surface_diagrams.named_expanded_loan import return_expanded_loan,shorten_expanded_loan_return
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD

class NamedExpandedLoanTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
  cls.saved=json.loads((cls.folder/'certificate.json').read_text(encoding='utf-8'))
  fs=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in cls.saved['early_boundary']['chart']['factors'])
  a=transport_alternative_roots(fs);b=expose_second_alternative_exterior(a['factors']);c=close_alternative_boundary(b['factors'])
  framed=shorten_named_disk_frames(a['stages']+b['stages'][1:]+c['stages'][1:])
  cyclic=shorten_named_cyclic_start(framed['stages']);cls.old=shorten_named_daisy_closure(cyclic['stages'])
  cls.r=shorten_expanded_loan_return(cls.old['stages']);cls.direct=cls.r['replacement_certificate']
 def test_one_operation_is_removed_with_a_literal_join_and_one_more_adjacent_check(self):
  r=self.r
  self.assertEqual((r['previous_whole_named_steps'],r['whole_named_steps'],r['operations_removed']),(92,91,1))
  self.assertEqual((r['previous_interval_steps'],r['replacement_steps'],r['graphical_steps']),(7,6,72))
  self.assertEqual((r['previous_adjacent_checks'],r['adjacent_checks']),(109,110))
  self.assertEqual(r['stages'][:58],self.old['stages'][:58]);self.assertEqual(r['stages'][64:],self.old['stages'][65:])
  self.assertEqual(self.direct['factors'],self.old['stages'][64]['factors']);self.assertTrue(r['literal_rejoin'])
 def test_no_temporary_three_point_factor_is_created_and_every_retained_state_is_exact(self):
  peak=0;expected=exact_action(BOUNDARY_WORD*4,5);count=0
  for s in self.direct['stages']:
   for a in (s,)+s.get('atomic_steps',()):
    count+=1;fs=a['factors'];self.assertTrue(all(not f.half and f.power>0 and f.points!=3 for f in fs))
    self.assertEqual(exact_action(product(fs),5),expected);self.assertEqual(homology_action(product(fs)),IDENTITY)
    peak=max(peak,max(len(supported_class(f.mapping_class,5)) for f in fs))
  self.assertEqual((peak,self.direct['actual_peak_support_word'],self.r['actual_peak_support_word']),(20,20,20))
  self.assertEqual(count,len(self.direct['state_sphere_lift_certificates']))
  for c in self.direct['state_sphere_lift_certificates']:
   self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
  self.assertEqual((self.direct['sphere_moves'],self.direct['exterior_caps'],self.direct['temporary_three_point_factors']),(0,0,0))
 def test_inverse_drag_moves_one_outer_ancestry_while_conjugating_it(self):
  s=self.direct['stages'][3];self.assertTrue(s['inverse_hurwitz_transport'])
  self.assertEqual(s['moving_factor'],'alternative.residual.O1234');self.assertEqual(s['adjacent_moves'],3)
  changed=0
  for atom in s['atomic_steps']:
   a,b=atom['transported_before'],atom['transported_after'];self.assertEqual(a.id,b.id)
   self.assertEqual((a.points,b.points),(4,4));self.assertEqual(atom['target'],atom['source']+1)
   self.assertEqual(reduce_word(product(atom['local_before'])),reduce_word(product(atom['local_after'])))
   fixed=next(f for f in atom['local_before'] if f.id!=a.id)
   after=next(f for f in atom['local_after'] if f.id==fixed.id)
   self.assertEqual(exact_action(fixed.word,5),exact_action(after.word,5))
   changed+=exact_action(a.word,5)!=exact_action(b.word,5)
  self.assertGreater(changed,0)
 def test_six_actual_pairs_match_the_nested_pc_rose_in_one_outer_chart(self):
  s=self.direct['stages'][5];w=s['named_pattern_witness'];t=w['template']
  self.assertEqual(len(s['local_before']),6);self.assertTrue(all(f.points==2 for f in s['local_before']))
  self.assertEqual(t['inner_chart'],(1,-2,-2));self.assertTrue(t['inner_outer_preserved'])
  inner=t['parent_daisy'][0];g=t['inner_chart']
  self.assertEqual(exact_action(g+inner.word+inverse_word(g),5),exact_action(inner.word,5))
  self.assertEqual(exact_action(product(t['expanded']),5),exact_action(t['outer'].word,5))
  self.assertEqual(len(w['individual_matches']),6)
  for m in w['individual_matches']+w['output_presentation_match']:
   self.assertTrue(m['exact_disk_equal']);self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
  self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
  wanted=tuple(sum(f.power for f in s['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-int(j in enclosed_boundaries(s['local_after'][0].mapping_class,5)) for j in range(1,6))
  self.assertEqual(s['framed_balance_before_minus_after'],wanted);self.assertEqual(wanted,(2,0,2,2,2))
 def test_a_single_matching_inner_petal_does_not_substitute_for_the_full_chart(self):
  s=self.direct['stages'][5];w=s['named_pattern_witness'];t=w['template'];outer=w['common_chart']
  wrong=tuple(replace(f,conjugator=reduce_word(outer+(1,)+f.conjugator)) for f in t['canonical_inner_rose'])
  matches=[exact_action(a.word,5)==exact_action(b.word,5) for a,b in zip(s['local_before'][:3],wrong)]
  self.assertEqual(matches,[False,False,True])
 def test_the_delayed_frame_is_an_actual_conjugation(self):
  s=self.direct['stages'][6];self.assertEqual(s['frame'],(-4,-3,-2))
  for a,b in zip(s['local_before'],s['local_after']):
   self.assertEqual(a.id,b.id);self.assertEqual(exact_action(s['frame']+a.word+inverse_word(s['frame']),5),exact_action(b.word,5))
 def test_saved_certificate_and_public_proof_counts_are_exact(self):
  saved=self.saved['named_expanded_loan_shortening'];metadata={k:v for k,v in self.r.items() if k not in ('stages','factors')}
  self.assertEqual(json.loads(json.dumps(metadata,default=asdict)),saved)
  summary=self.saved['named_full_route']['summary'];self.assertEqual((summary['graphical_steps'],summary['mathematical_steps_saved']),(90,1))
  self.assertEqual(summary['route_parts'],[17,71,1,1]);self.assertEqual(summary['sphere_moves'],4);self.assertEqual(summary['action_only_boundary_recognitions'],0)
  d=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'));self.assertEqual(len(d['routes']['namedfull']),91)
  inverse=[s for s in d['routes']['namedfull'] if s.get('inverse_hurwitz_transport')];self.assertEqual(len(inverse),1)
  self.assertIn('ONE INVERSE DISK HURWITZ TRANSPORT',(self.folder/'index.html').read_text(encoding='utf-8'))
 def test_bad_sources_are_rejected(self):
  with self.assertRaises(ValueError):shorten_expanded_loan_return(self.old['stages'][:-1])
  source=self.direct['stages'][0]['factors']
  with self.assertRaises(ValueError):return_expanded_loan(source[:-1])
  with self.assertRaises(ValueError):return_expanded_loan((replace(source[0],half=True),)+source[1:])
