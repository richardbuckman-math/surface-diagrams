import json
from pathlib import Path
from dataclasses import replace
import unittest
from surface_diagrams.early_alternative_transport import transport_alternative_roots
from surface_diagrams.early_alternative_exterior import expose_second_alternative_exterior
from surface_diagrams.early_alternative_closure import close_alternative_boundary
from surface_diagrams.named_disk_frames import shorten_named_disk_frames
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD

class NamedDiskFrameTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
  cls.saved=json.loads((cls.folder/'certificate.json').read_text(encoding='utf-8'))
  fs=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in cls.saved['early_boundary']['chart']['factors'])
  a=transport_alternative_roots(fs);b=expose_second_alternative_exterior(a['factors']);c=close_alternative_boundary(b['factors'])
  cls.source=a['stages']+b['stages'][1:]+c['stages'][1:];cls.route=shorten_named_disk_frames(cls.source)
 def test_two_actual_operations_removed_without_changing_the_terminal_exteriors(self):
  r=self.route
  self.assertEqual((len(self.source)-1,r['graphical_steps'],r['operations_removed'],r['whole_named_steps']),(82,80,2,99))
  self.assertEqual(r['factors'],self.source[-1]['factors'])
  self.assertEqual(sum(s['kind']=='global_conjugation' for s in self.source),5)
  self.assertEqual(sum(s['kind']=='global_conjugation' for s in r['stages']),3)
  self.assertEqual(r['stages'][26]['frame'],(4,))
  for m in r['omitted_frame_source_presentations']:
   self.assertEqual(m['before'].id,m['after'].id);self.assertEqual(exact_action(m['before'].word,5),exact_action(m['after'].word,5))
 def test_all_states_and_retained_neighbors_are_positive_bounded_disk_and_lift_exact(self):
  peak=0;expected=exact_action(BOUNDARY_WORD*4,5)
  for s in self.route['stages']:
   for a in (s,)+s.get('atomic_steps',()):
    fs=a['factors'];self.assertTrue(all(f.power>0 for f in fs))
    self.assertEqual(exact_action(product(fs),5),expected);self.assertEqual(homology_action(product(fs)),IDENTITY)
    peak=max(peak,max(len(supported_class(f.mapping_class,5)) for f in fs))
  self.assertEqual(peak,20);self.assertEqual(self.route['adjacent_checks'],117)
  self.assertFalse(any('sphere' in s['kind'] for s in self.route['stages']))
 def test_transported_named_patterns_keep_actual_matches_and_original_witnesses(self):
  count=0
  for s in self.route['stages']:
   if 'common_disk_transport' not in s:continue
   h=s['common_disk_transport'];old=s['source_stage']
   for a,b in zip(old['factors'],s['factors']):self.assertEqual(exact_action(h+a.word+inverse_word(h),5),exact_action(b.word,5))
   if 'named_pattern_witness' in s:
    count+=1;w=s['named_pattern_witness'];self.assertIn('source_witness',w)
    for m in w['individual_matches']:self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
   if 'framed_balance_before_minus_after' in s:
    wanted=tuple(sum(f.power for f in s['local_before'] if i in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in s['local_after'] if i in enclosed_boundaries(f.mapping_class,5)) for i in range(1,6))
    self.assertEqual(s['framed_balance_before_minus_after'],wanted)
   for a in s.get('atomic_steps',()):
    self.assertIn('source_atomic_certificate',a)
    self.assertEqual(exact_action(product(a['local_before']),5),exact_action(product(a['local_after']),5))
  self.assertEqual(count,2)
 def test_cyclic_starts_remain_exact_common_conjugations(self):
  for i,s in enumerate(self.route['stages'][1:],1):
   before=product(self.route['stages'][i-1]['factors']);after=product(s['factors'])
   if s['kind'] in ('global_conjugation','disk_cyclic_start'):
    g=s['frame'];before=g+before+inverse_word(g)
   self.assertEqual(exact_action(before,5),exact_action(after,5))
 def test_public_complete_route_has_82_steps_four_explicit_sphere_moves_and_no_action_recognition(self):
  r=self.saved['named_full_route'];self.assertEqual(r['summary']['route_parts'],[17,63,1,1]);self.assertEqual(r['summary']['graphical_steps'],82)
  self.assertEqual(r['summary']['sphere_moves'],4);self.assertEqual(r['summary']['action_only_boundary_recognitions'],0)
  d=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'))
  self.assertEqual(len(d['routes']['namedfull']),83)
  for s,t in zip(r['stages'][17:-2],d['routes']['namedfull'][17:-2]):
   for f,j in zip(s['factors'],t['factors']):
    f=Factor(**dict(f,conjugator=tuple(f['conjugator'])));self.assertEqual(exact_action(f.word,5),exact_action(d['rows'][j]['word'],5));self.assertFalse(d['rows'][j]['sphere_rechart'])
 def test_source_validation_and_original_records_are_preserved(self):
  with self.assertRaises(ValueError):shorten_named_disk_frames(self.source[:-1])
  self.assertEqual(tuple(self.source[26]['frame']),(3,4,4));self.assertEqual(tuple(self.source[30]['frame']),(-4,-3))
  self.assertEqual(tuple(self.source[71]['frame']),(-4,-3,-2,-1,-1))

if __name__=='__main__':unittest.main()
