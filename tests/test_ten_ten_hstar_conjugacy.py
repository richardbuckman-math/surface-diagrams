import json,unittest
from pathlib import Path
from dataclasses import asdict,replace
from hashlib import sha256
from surface_diagrams.factorization_explorer import product
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.point_pushing import split_fixed_last_strand
from examples.analyze_ten_ten_hstar_conjugacy import report,SOURCE,PIN,TARGET,TARGET_PIN,OUTPUT

ROOT=Path(__file__).resolve().parents[1]

class TenTenHstarConjugacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()

    def test_immutable_pins_and_entire_certificate_reproduce(self):
        self.assertEqual(sha256((ROOT/SOURCE).read_bytes()).hexdigest(),PIN)
        self.assertEqual(sha256((ROOT/TARGET).read_bytes()).hexdigest(),TARGET_PIN)
        self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),json.loads((ROOT/OUTPUT).read_bytes()))

    def test_every_group_actor_is_a_literal_actual_source_record(self):
        r=self.r;source=r['source_factors'];plan=r['source_group_plan']
        self.assertEqual(r['source_half_position'],2);self.assertEqual(r['source_half'],source[2])
        self.assertEqual(tuple((x['source_position'],x['sign']) for x in plan),((18,1),(19,1),(2,1),(19,-1),(18,-1),(6,-1),(5,-1),(4,-1),(3,-1)))
        for x in plan:self.assertEqual(x['actual_factor'],source[x['source_position']]);self.assertEqual(x['id'],x['actual_factor'].id)
        w=reduce_word(tuple(y for x in plan for y in (x['actual_factor'].word if x['sign']>0 else inverse_word(x['actual_factor'].word))))
        self.assertEqual(w,r['source_group_conjugator']);self.assertEqual(len(w),92)
        self.assertEqual(r['group_factor_occurrences'],9)
        self.assertNotIn('four_three_C.7',tuple(x['id'] for x in plan))

    def test_braid_relation_and_boundary_correction_prove_the_conjugacy(self):
        r=self.r;a=r['source_half'].word;c=r['reference_C7'].word;M=r['actual_M_word'];P=r['actual_P_word'];D=r['embedded_boundary'].word
        self.assertEqual(exact_action(a+c+a,6),exact_action(c+a+c,6))
        self.assertNotEqual(reduce_word(a+c+a+inverse_word(c+a+c)),())
        self.assertEqual(exact_action(P+M+c,6),exact_action(D,6))
        self.assertEqual(exact_action(D+a,6),exact_action(a+D,6))
        self.assertEqual(exact_action(r['source_group_conjugator'],6),exact_action(M+a+c+inverse_word(D),6))
        self.assertEqual(exact_action(M+c+inverse_word(M),6),exact_action(r['target_Hstar'].word,6))
        self.assertEqual(len(r['full_faithful_B6_equalities']),7)
        for q in r['full_faithful_B6_equalities']:
            self.assertEqual(exact_action(q['left_word'],6),exact_action(q['right_word'],6))

    def test_exact_existing_B7_conjugation_matches_the_bounded_target_class(self):
        r=self.r;g=r['source_group_conjugator'];a=r['source_half'];h=r['target_Hstar']
        raw=reduce_word(g+a.word+inverse_word(g));self.assertEqual(len(raw),189)
        self.assertEqual(exact_action(raw,6),exact_action(h.word,6))
        hypothetical=replace(a,conjugator=reduce_word(g+a.conjugator))
        self.assertEqual(hypothetical.word,r['hypothetical_conjugated_half'].word)
        self.assertTrue(hypothetical.half);self.assertEqual(hypothetical.power,1)
        self.assertEqual(supported_class(hypothetical.mapping_class,6),r['exact_endpoint_support'])
        self.assertEqual(r['exact_endpoint_support'],r['exact_target_support']);self.assertEqual(len(r['exact_endpoint_support']),18)

    def test_full_nonabelian_discrepancy_kernel_shadow_and_reconstruction(self):
        r=self.r;d=r['full_disk_discrepancy'];p=r['full_discrepancy_point_pushing']
        self.assertEqual(d,reduce_word(r['hypothetical_conjugated_half'].word+inverse_word(r['target_Hstar'].word)))
        split=split_fixed_last_strand(d,6);self.assertEqual(split,p['split']);self.assertEqual(split.kernel_loop,())
        self.assertEqual(exact_action(split.shadow_word,5),tuple((i,) for i in range(1,6)))
        self.assertEqual(exact_action(split.reconstructed_word,6),exact_action(d,6))
        embedded=r['embedded_B5_discrepancy_point_pushing']['split']
        self.assertEqual(embedded.kernel_loop,());self.assertEqual(exact_action(embedded.shadow_word,4),tuple((i,) for i in range(1,5)))
        self.assertEqual(exact_action(embedded.reconstructed_word,5),exact_action(embedded.source_word,5))
        inapplicable=0
        for q in r['all_actual_and_reference_word_stabilizers_or_full_actions']:
            self.assertTrue(all(abs(x)>=2 for x in q['B6_word']))
            shifted=((1,),)+tuple(tuple((1 if x>0 else -1)*(abs(x)+1) for x in row) for row in q['B5_images'])
            self.assertEqual(q['B6_images'],shifted)
            for key,n in (('B6_stabilizer_or_full_action',6),('B5_stabilizer_or_full_action',5)):
                s=q[key]
                if not s['applicable']:
                    inapplicable+=1;self.assertNotIn('split',s)
                    self.assertEqual(s['full_faithful_images'],exact_action(s['source_word'],n))
                else:self.assertEqual(exact_action(s['split'].reconstructed_word,n),exact_action(s['source_word'],n))
        self.assertGreater(inapplicable,0)

    def test_separate_sphere_characters_full_sphere_action_and_chosen_lift(self):
        r=self.r;c=r['necessary_sphere_character'];s=r['full_sphere_certificate']
        self.assertEqual(len(c['rectangle_characters']),30);self.assertFalse(c['nonidentity_sphere_proved'])
        self.assertTrue(s['certified']);self.assertEqual(len(s['arc_pairs']),5)
        self.assertEqual(s['reference_classes'],s['image_classes'])
        self.assertEqual(homology_action(r['full_disk_discrepancy']),IDENTITY)
        self.assertEqual(r['chosen_lift_discrepancy'],IDENTITY)

    def test_unsupported_single_slot_replacement_does_not_close(self):
        r=self.r;q=r['hypothetical_single_slot_countercheck'];before=r['source_factors'];after=q['factors']
        self.assertEqual(len(after),20);self.assertEqual(before[:2],after[:2]);self.assertEqual(before[3:],after[3:])
        self.assertEqual(after[2],replace(r['target_Hstar'],id=before[2].id))
        self.assertEqual(homology_action(product(after)),q['full_Sp4_product']);self.assertNotEqual(q['full_Sp4_product'],IDENTITY)
        self.assertFalse(q['applied'])

    def test_conjugacy_is_complete_but_no_supplier_or_fibration_equivalence_is_claimed(self):
        r=self.r;self.assertTrue(r['exact_source_B7_G_conjugacy_proved']);self.assertTrue(r['exact_faithful_disk_conjugacy_proved'])
        self.assertEqual(r['actual_source_moves'],0);self.assertEqual(r['actual_source_factor_changes'],0)
        for k in ('source_ancestry_physically_supplied','bounded_Hurwitz_supplier_reached','seven_factor_gather_reached',
                  'residual_thirteen_closure_proved','reverse_fibration_equivalence_proved','preferred_proof_changed','adopted'):self.assertFalse(r[k])

if __name__=='__main__':unittest.main()
