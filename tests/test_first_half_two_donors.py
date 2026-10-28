from dataclasses import asdict
from pathlib import Path
import json
import unittest
from examples.analyze_first_half_two_donors import report
from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.hyperelliptic_homology import IDENTITY
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.alternative_thirty_audit import pure_linking_certificate
from surface_diagrams.factorization_explorer import Factor


class FirstHalfTwoDonorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()

    def test_two_actual_donor_expansions_are_positive_bounded_and_disk_exact(self):
        r=self.r;self.assertEqual((r['graphical_operations'],r['adjacent_checks']),(3,7))
        self.assertEqual(r['after_score'],dict(max_support_word=19,total_support_word=130,braid_letters=266))
        initial={f.id:f for f in r['stages'][0]['factors']}
        retained=[a for s in r['stages'] for a in (s,)+tuple(s.get('atomic_steps',()))]
        self.assertEqual(len(retained),11)
        for s,c in zip(retained,r['state_sphere_lift_certificates']):
            fs=s['factors'];self.assertTrue(all(f.power>0 for f in fs));self.assertEqual(sum(f.half for f in fs),4)
            self.assertEqual(exact_action(product(fs),5),exact_action(BOUNDARY_WORD*4,5))
            self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
            for f in fs:
                if f.id in ('F3','F9'):self.assertEqual(f,initial[f.id])
        self.assertEqual(len(r['stages'][-1]['factors']),22)
        for d in r['donors']:
            self.assertTrue(d['applied_to_audit']);self.assertFalse(d['applied_to_public_replay'])
            m=d['actual_Q14_match'][0]
            self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))

    def test_selected_only_obstruction_has_full_meridian_witnesses(self):
        o=self.r['selected_only_order_obstruction'];self.assertTrue(o['excluded'])
        self.assertEqual(tuple(f.id for f in o['selected']),('two.outer.3','F3','two.root.2','F9'))
        for row in o['cyclic_orders']:
            w=row['witness'];word=product(row['factors']);factor=w['factor']
            self.assertEqual(exact_action(word+factor.word,5),w['left_images'])
            self.assertEqual(exact_action(factor.word+word,5),w['right_images'])
            self.assertNotEqual(w['left_images'],w['right_images'])
            j=w['first_different_meridian']-1;self.assertNotEqual(w['left_images'][j],w['right_images'][j])
        t=self.r['half_lantern_target'];a,b,q2=t['actual_inputs'];q=o['selected'][0]
        self.assertEqual(exact_action(a.word+b.word+q.word+q.word,5),exact_action(t['root'].word,5))
        for f in (a,b,q):
            self.assertEqual(exact_action(t['root'].word+f.word,5),exact_action(f.word+t['root'].word,5))
        self.assertIn('NOT excluded',o['scope']);self.assertFalse(t['applied'])
        self.assertFalse(t['framed_hole_half_twist_convention_asserted'])

    def test_new_joint_lantern_chart_matches_every_input_and_output(self):
        t=self.r['next_larger_lantern'];g=t['common_chart']
        for actual,canonical in zip(t['actual_inputs'],t['canonical_inputs']):
            self.assertEqual(exact_action(actual.word,5),exact_action(g+canonical.word+inverse_word(g),5))
        for actual,canonical in zip(t['actual_outputs'],t['canonical_outputs']):
            self.assertEqual(exact_action(actual.word,5),exact_action(g+canonical.word+inverse_word(g),5))
        self.assertEqual(exact_action(product(t['actual_inputs']),5),exact_action(product(t['actual_outputs']),5))
        self.assertTrue(t['sphere_certificate']['certified']);self.assertEqual(t['chosen_lift_discrepancy'],IDENTITY)
        self.assertEqual(t['root_donor_intersection']['intersection_number'],2)
        self.assertFalse(t['new_outer_is_source_outer']);self.assertFalse(t['original_outer_commutes_target_root'])
        self.assertFalse(t['applied']);self.assertTrue(t['requires_half_lantern_gathering']);self.assertFalse(t['requires_actual_P23']);self.assertTrue(t['requires_restored_S1'])

    def test_specific_missing_petal_failures_are_exact_and_scoped(self):
        t=self.r['next_larger_lantern'];wanted=t['actual_inputs'][2]
        self.assertGreater(len(t['canonical_supplier_comparisons']),10)
        for p in t['canonical_supplier_comparisons']:
            self.assertFalse(p['exact_match']);self.assertNotEqual(exact_action(p['petal'].word,5),exact_action(wanted.word,5))
        self.assertEqual(len(t['specific_F6_transports']),4)
        for p in t['specific_F6_transports']:
            self.assertFalse(p['applied']);self.assertFalse(p['exact_match'])
            self.assertNotEqual(exact_action(p['transported'].word,5),exact_action(wanted.word,5))

    def test_actual_positive_half_drag_supplies_P23_and_preserves_the_target_halves(self):
        t=self.r['outside_petal_transport'];self.assertTrue(t['reached'])
        self.assertFalse(t['applied_to_public_replay'])
        self.assertTrue(t['round12_source_match'])
        for match in t['target_match']+t['original_target_half_matches']:
            self.assertEqual(exact_action(match['actual'].word,5),exact_action(match['pattern'].word,5))
        self.assertEqual(self.r['stages'][-1]['adjacent_moves'],7)
        self.assertTrue(all(m['exact_disk_equal'] for m in self.r['next_larger_lantern']['actual_P23_supplied']))

    def test_coupled_target_is_individually_named_but_current_seven_order_is_obstructed(self):
        t=self.r['coupled_half_lantern_target'];g=t['common_chart']
        self.assertEqual([f.power for f in t['actual_inputs']],[1,1,2,1,1,1])
        self.assertEqual(sum(f.half for f in t['actual_inputs']),2)
        for a,b in zip(t['actual_inputs'],t['canonical_inputs']):
            self.assertEqual(exact_action(a.word,5),exact_action(g+b.word+inverse_word(g),5))
        self.assertEqual(exact_action(product(t['actual_inputs']),5),exact_action(t['actual_output'].word,5))
        self.assertTrue(t['sphere_certificate']['certified']);self.assertEqual(t['chosen_lift_discrepancy'],IDENTITY)
        self.assertEqual(len(t['half_parent_retained_moves']),2)
        self.assertFalse(t['framed_hole_half_twist_convention_asserted'])
        seven=t['actual_seven_instances'];self.assertEqual(len(seven),7)
        word=product(seven);w=t['actual_order_witness'];f=w['factor']
        self.assertEqual(exact_action(word+f.word,5),w['left_images'])
        self.assertEqual(exact_action(f.word+word,5),w['right_images'])
        self.assertNotEqual(w['left_images'],w['right_images'])
        self.assertFalse(t['actual_prefix_square_split']);self.assertFalse(t['applied']);self.assertTrue(t['requires_gathering'])
        self.assertIn('spare12',t['scope'])

    def test_every_nonabelian_kernel_reconstructs_the_actual_disk_braid(self):
        for x in self.r['complete_point_pushing']:
            self.assertEqual(exact_action(x['factor'].word,5),exact_action(x['split'].reconstructed_word,5))
        self.assertEqual(exact_action(product(self.r['selected_only_order_obstruction']['selected']),5),
                         exact_action(self.r['selected_product_split'].reconstructed_word,5))

    def test_isolated_spare12_block_cannot_be_four_point_outer_plus_positive_pair(self):
        ids=('two.outer.3','alternative.T12.square','two.root.0','F3','two.root.1','two.root.2','F9')
        selected=tuple(f for f in self.r['stages'][-1]['factors'] if f.id in ids)
        actual=pure_linking_certificate(product(selected),5)
        self.assertTrue(actual['pure']);self.assertEqual(actual['off_diagonal_spectrum'],((0,5),(1,3),(2,2)))
        outer=Factor('round.D4',(),1,4)
        inside=pure_linking_certificate(outer.word+Factor('inside12',(),1,2).word,5)
        outside=pure_linking_certificate(outer.word+Factor('outside45',(),4,2).word,5)
        self.assertEqual(inside['off_diagonal_spectrum'],((0,4),(1,5),(2,1)))
        self.assertEqual(outside['off_diagonal_spectrum'],((0,3),(1,7)))
        self.assertNotEqual(actual['off_diagonal_spectrum'],inside['off_diagonal_spectrum'])
        self.assertNotEqual(actual['off_diagonal_spectrum'],outside['off_diagonal_spectrum'])

    def test_saved_audit_is_exact_and_does_not_claim_a_public_shortening(self):
        path=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-first-half-two-donors.json'
        self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),json.loads(path.read_text(encoding='utf-8')))
        self.assertFalse(self.r['public_graphical_payloads_changed']);self.assertFalse(self.r['complete_shorter_derivation'])
        self.assertEqual((self.r['sphere_moves'],self.r['exterior_caps']),(0,0))


if __name__=='__main__':unittest.main()
