import json
from pathlib import Path
from dataclasses import asdict,replace
import unittest
from examples.analyze_one_unit_half_lantern import report
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.one_unit_half_lantern import audit_one_unit_half_lantern

class OneUnitHalfLanternTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.route=report();cls.source=cls.route['stages'][0]['factors']
  cls.root=Path(__file__).resolve().parents[1]
 def test_every_reached_state_and_neighbor_is_positive_disk_sphere_and_lift_exact(self):
  r=self.route;self.assertEqual((r['graphical_operations'],r['adjacent_checks']),(4,3))
  peak=0
  for s in r['stages']:
   for a in (s,)+s.get('atomic_steps',()):
    fs=a['factors'];self.assertTrue(all(f.power>0 for f in fs))
    self.assertEqual(exact_action(product(fs),5),exact_action(BOUNDARY_WORD*4,5))
    self.assertEqual(homology_action(product(fs)),IDENTITY)
    peak=max(peak,max(len(supported_class(f.mapping_class,5)) for f in fs))
  self.assertEqual(peak,11);self.assertEqual(r['sphere_move_count'],0)
  for c in r['state_sphere_lift_certificates']:
   self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
  for i,s in enumerate(r['stages'][1:],1):
   if s['kind']=='disk_cyclic_start':
    g=s['frame'];self.assertEqual(reduce_word(g+product(r['stages'][i-1]['factors'])+inverse_word(g)),reduce_word(product(s['factors'])))
 def test_each_actual_target_input_matches_the_joint_chart_but_the_target_is_unapplied(self):
  t=self.route['target'];self.assertEqual(t['common_chart'],(-4,-4,-3,-1,2,1))
  self.assertEqual(t['local_after'][0],Factor('one.unit.target.R124',(-4,-4,-3),1,3))
  for m in t['individual_matches']:
   self.assertTrue(m['exact_disk_equal']);self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
  self.assertEqual(exact_action(product(t['local_before']),5),exact_action(product(t['local_after']),5))
  self.assertEqual(t['chosen_lift_discrepancy'],IDENTITY);self.assertFalse(t['applied']);self.assertTrue(t['requires_gathering'])
  self.assertNotEqual(tuple(f.id for f in self.route['ordered_obstruction']['actual_selected_factors']),('F6','F11','one.unit.Q1','one.unit.Q2'))
 def test_noncentrality_witnesses_exclude_only_selected_factor_disk_routes(self):
  o=self.route['ordered_obstruction'];self.assertEqual(len(o['cyclic_orders']),4)
  self.assertTrue(o['selected_only_disk_hurwitz_and_common_frame_excluded'])
  target_root=self.route['target']['local_after'][0]
  for f in o['actual_selected_factors']:
   self.assertEqual(exact_action(target_root.word+f.word,5),exact_action(f.word+target_root.word,5))
  for c in o['cyclic_orders']:
   w=c['witness'];a=c['product_word'];b=w['factor'].word
   self.assertEqual(exact_action(a+b,5),w['left_images']);self.assertEqual(exact_action(b+a,5),w['right_images'])
   self.assertNotEqual(w['left_images'],w['right_images'])
   i=w['first_different_meridian']-1;self.assertNotEqual(w['left_images'][i],w['right_images'][i])
  self.assertIn('Outside interactions and sphere changes are NOT excluded',o['scope'])
 def test_all_point_pushing_kernels_and_actual_donor_matches_are_retained(self):
  t=self.route['target']
  for entry in t['point_pushing_splits']:
   self.assertEqual(exact_action(entry['split'].reconstructed_word,5),exact_action(entry['factor'].word,5))
  o=self.route['ordered_obstruction'];self.assertEqual(exact_action(o['actual_product_split'].reconstructed_word,5),exact_action(product(o['actual_selected_factors']),5))
  d=self.route['donor'];self.assertEqual(exact_action(d['actual_outer'].word,5),exact_action(d['canonical_outer'].word,5))
  self.assertEqual(exact_action(d['terms'][0].word,5),exact_action(product(t['local_after']),5));self.assertFalse(d['applied']);self.assertTrue(all(not m['existing_unit_matches'] for m in d['existing_petal_matches']))
 def test_parent_rose_derivation_is_exact_and_framed_hole_half_lift_is_not_assumed(self):
  f=self.route['target']['framing_source'];self.assertEqual(len(f['retained_hurwitz_checks']),2)
  for m in f['retained_hurwitz_checks']:
   self.assertEqual(exact_action(product(m['local_before']),5),exact_action(product(m['local_after']),5))
  self.assertEqual(exact_action(product(f['rose_terms']),5),exact_action(product(f['derived_terms']),5))
  self.assertEqual(f['parent_pc_rose_balance_before_minus_after'],(1,1,0,1,0))
  self.assertFalse(f['half_twist_boundary_lift_asserted'])
 def test_saved_audit_reproduces_exactly_without_changing_the_public_proof(self):
  p=self.root/'docs/proofs/six-seven-one-unit-half-lantern.json'
  self.assertEqual(json.loads(json.dumps(self.route,default=asdict)),json.loads(p.read_text(encoding='utf-8')))
  self.assertFalse(self.route['public_replay_changed']);self.assertEqual(self.route['complete_proof_steps'],99)
  c=json.loads((self.root/'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
  self.assertEqual(c['named_full_route']['summary']['graphical_steps'],90)
  self.assertEqual(self.route['after_score'],dict(max_support_word=11,total_support_word=91,braid_letters=192))
 def test_wrong_source_is_rejected(self):
  for wrong in (self.source[:-1],(replace(self.source[0],id='wrong'),)+self.source[1:]):
   with self.assertRaises(ValueError):audit_one_unit_half_lantern(wrong)

if __name__=='__main__':unittest.main()
