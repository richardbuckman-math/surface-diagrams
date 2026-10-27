from pathlib import Path
from dataclasses import replace
import json,unittest
from surface_diagrams.early_alternative_transport import transport_alternative_roots
from surface_diagrams.early_alternative_exterior import expose_second_alternative_exterior
from surface_diagrams.early_alternative_closure import close_alternative_boundary
from surface_diagrams.named_disk_frames import shorten_named_disk_frames
from surface_diagrams.named_cyclic_start import shorten_named_cyclic_start
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.puncture_boundary import BOUNDARY_WORD

class NamedCyclicStartTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
  cls.saved=json.loads((cls.folder/'certificate.json').read_text(encoding='utf-8'))
  fs=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in cls.saved['early_boundary']['chart']['factors'])
  a=transport_alternative_roots(fs);b=expose_second_alternative_exterior(a['factors']);c=close_alternative_boundary(b['factors'])
  cls.old=shorten_named_disk_frames(a['stages']+b['stages'][1:]+c['stages'][1:])
  cls.r=shorten_named_cyclic_start(cls.old['stages'])
 def test_actual_commutation_is_bypassed_and_all_neighbor_checks_remain(self):
  r=self.r
  self.assertEqual((r['previous_disk_steps'],r['graphical_steps'],r['operations_removed'],r['whole_named_steps']),(80,79,1,98))
  self.assertEqual(r['adjacent_checks'],self.old['adjacent_checks']);self.assertEqual(r['adjacent_checks'],117)
  self.assertFalse(any(s['title']=='Commute the recovered round square to the top' for s in r['stages']))
  interval=r['replacement_interval'];self.assertEqual(len(interval)-1,8)
  self.assertEqual(interval[2]['adjacent_moves'],3)
  crossed=[a['local_before'][0].id if a['local_before'][1].id=='alternative.T12.square' else a['local_before'][1].id for a in interval[2]['atomic_steps']]
  self.assertIn('alternative.O1234',crossed)
 def test_new_cut_keeps_outer_at_bottom_then_literally_rejoins(self):
  old=self.old['stages'];r=self.r;interval=r['replacement_interval']
  self.assertEqual(interval[1]['factors'][-2].id,'alternative.O1234')
  for s in interval[2:7]:self.assertEqual(s['factors'][-1].id,'alternative.O1234')
  self.assertEqual(r['stages'][:23],old[:23]);self.assertEqual(r['stages'][31:],old[32:])
  self.assertEqual(interval[-1]['factors'],old[31]['factors'])
  self.assertEqual(r['factors'],self.old['factors'])
  for m in r['rejoin_individual_presentations']:
   self.assertEqual(m['actual'].id,m['pattern'].id);self.assertTrue(m['exact_disk_equal'])
   self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
 def test_all_states_and_atomic_moves_are_positive_exact_and_bounded(self):
  peak=0;expected=exact_action(BOUNDARY_WORD*4,5)
  for s in self.r['stages']:
   for a in (s,)+s.get('atomic_steps',()):
    fs=a['factors'];self.assertTrue(all(f.power>0 for f in fs));self.assertEqual(exact_action(product(fs),5),expected)
    self.assertEqual(homology_action(product(fs)),IDENTITY)
    peak=max(peak,max(len(supported_class(f.mapping_class,5)) for f in fs))
  self.assertEqual((peak,self.r['extension_peak_support_word']),(20,17))
  self.assertEqual(self.r['sphere_moves'],0)
 def test_new_cyclic_starts_are_explicit_conjugations_not_centrality_assumptions(self):
  interval=self.r['replacement_interval']
  for i,s in enumerate(interval[1:],1):
   before=product(interval[i-1]['factors']);after=product(s['factors'])
   if s['kind'] in ('disk_cyclic_start','global_conjugation'):
    before=s['frame']+before+inverse_word(s['frame'])
   self.assertEqual(exact_action(before,5),exact_action(after,5))
   if s['kind']=='disk_cyclic_start':
    after=product(s.get('cyclic_before_disk_presentations',s['factors']))
    self.assertEqual(reduce_word(before),reduce_word(after))
  self.assertEqual(interval[1]['frame'],inverse_word(product(interval[0]['factors'][:2])))
 def test_actual_daisy_and_original_local_proof_survive_the_cut_change(self):
  s=self.r['replacement_interval'][7];old=self.old['stages'][30]
  self.assertEqual(s['source_stage'],old);self.assertEqual(s['local_after'],old['local_after'])
  m=s['actual_donor_match'];self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
  self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
 def test_public_proof_has_89_steps_four_visible_sphere_moves_and_no_action_only_recognition(self):
  r=self.saved['named_full_route'];summary=r['summary']
  self.assertEqual((summary['graphical_steps'],summary['mathematical_steps_saved']),(89,1))
  self.assertEqual(summary['route_parts'],[17,70,1,1]);self.assertEqual(summary['sphere_moves'],4)
  self.assertEqual(summary['action_only_boundary_recognitions'],0)
  d=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'))
  self.assertEqual(len(d['routes']['namedfull']),90)
  self.assertFalse(summary['complete_under_twenty_derivation'])
 def test_wrong_source_is_rejected(self):
  with self.assertRaises(ValueError):shorten_named_cyclic_start(self.old['stages'][:-1])
  bad=list(self.old['stages']);bad[23]=dict(bad[23],title='not the source commute')
  with self.assertRaises(ValueError):shorten_named_cyclic_start(bad)
