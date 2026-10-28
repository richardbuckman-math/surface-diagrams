from dataclasses import asdict
from itertools import permutations
from pathlib import Path
import json,unittest
from examples.analyze_first_half_ledgers import report
from surface_diagrams.alternative_thirty_audit import pure_linking_certificate
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.linking_ledgers import positive_linking_ledgers
from surface_diagrams.mapping_classes import exact_action,VerificationLimitError


class FirstHalfLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()

    def test_full_matrix_excludes_three_records_and_retains_exactly_two_four_support_targets(self):
        c=self.r['positive_ledger_certificate']
        self.assertEqual(c['minimum_distinct_supports'],4);self.assertEqual(len(c['ledgers']),2)
        self.assertTrue(c['exhaustive_within_bound']);self.assertFalse(c['geometric_match_asserted'])
        self.assertEqual(tuple(s for s in c['candidate_supports'] if len(s)==3),((1,2,3),(2,3,4)))
        self.assertTrue(all(len(s)<=3 for s in c['candidate_supports']))
        for ledger in c['ledgers']:
            actual=[[0]*5 for _ in range(5)]
            for support,power in ledger:
                for i in support:
                    for j in support:
                        if i!=j:actual[i-1][j-1]+=power
            self.assertEqual(tuple(map(tuple,actual)),c['linking_matrix'])
        self.assertEqual(positive_linking_ledgers(c['linking_matrix'],max_distinct_supports=3)['ledgers'],())
        self.assertTrue(self.r['three_record_full_twist_endform_excluded'])

    def test_all120_global_label_permutations_have_the_same_obstruction_and_permuted_targets(self):
        c=self.r['positive_ledger_certificate'];matrix=c['linking_matrix']
        for perm in permutations(range(5)):
            changed=tuple(tuple(matrix[perm[i]][perm[j]] for j in range(5)) for i in range(5))
            inverse={old+1:new+1 for new,old in enumerate(perm)}
            expected={frozenset((tuple(sorted(inverse[x] for x in support)),power) for support,power in ledger) for ledger in c['ledgers']}
            actual=positive_linking_ledgers(changed)
            self.assertEqual(actual['minimum_distinct_supports'],4)
            self.assertEqual({frozenset(ledger) for ledger in actual['ledgers']},expected)

    def test_spectrum_alone_does_not_imply_the_stronger_labeled_graph_exclusion(self):
        root123=Factor('a',(),1,3);root234=Factor('b',(),2,3);pair12=Factor('c',(),1,2)
        c=pure_linking_certificate(root123.word+root234.word+pair12.word,5)
        self.assertEqual(c['off_diagonal_spectrum'],self.r['full_labeled_linking']['off_diagonal_spectrum'])
        result=positive_linking_ledgers(c['linking_matrix'],max_distinct_supports=3)
        self.assertTrue(result['ledgers']);self.assertEqual(result['minimum_distinct_supports'],3)
        a=set((1,2));b=set((3,4));self.assertFalse(a&b)
        doubled={tuple((i+1,j+1)) for i in range(5) for j in range(i+1,5) if c['linking_matrix'][i][j]==2}
        x,y=tuple(doubled);self.assertTrue(set(x)&set(y))

    def test_all24_fixed_actual_curve_orders_retain_exact_nonabelian_failure_witnesses(self):
        t=self.r['unchanged_four_record_probe'];source=exact_action(product(self.r['selected_factors']),5)
        self.assertEqual(len(t['orders']),24);self.assertTrue(t['all24_orders_fail']);self.assertFalse(t['applied'])
        for row in t['orders']:
            actual=exact_action(product(tuple(t['candidates'][i] for i in row['order'])),5)
            i=row['first_different_meridian']-1
            self.assertEqual(row['source_image'],source[i]);self.assertEqual(row['candidate_image'],actual[i])
            self.assertNotEqual(source[i],actual[i]);self.assertFalse(row['exact_match'])

    def test_full_kernels_and_shadows_reconstruct_without_forgetting_a_strand(self):
        for row in self.r['individual_point_pushing']:
            self.assertEqual(exact_action(row['factor'].word,5),exact_action(row['split'].reconstructed_word,5))
        self.assertEqual(exact_action(product(self.r['selected_factors']),5),exact_action(self.r['complete_product_point_pushing'].reconstructed_word,5))

    def test_powers_invalid_inputs_and_exhaustion_keep_their_exact_scope(self):
        c=pure_linking_certificate(Factor('root',(),1,3,2).word,3)
        self.assertEqual(positive_linking_ledgers(c['linking_matrix'],max_distinct_supports=1)['ledgers'],((((1,2,3),2),),))
        with self.assertRaises(VerificationLimitError):positive_linking_ledgers(self.r['full_labeled_linking']['linking_matrix'],max_work=1)
        for bad in (((0,1),(0,0)),((1,0),(0,0)),((0,-1),(-1,0)),((0,True),(True,0))):
            with self.assertRaises(ValueError):positive_linking_ledgers(bad)
        for bad in (False,0,-1):
            with self.assertRaises(ValueError):positive_linking_ledgers(((0,1),(1,0)),max_distinct_supports=bad)

    def test_saved_report_keeps_public_route_and_all_optional_scopes_unchanged(self):
        p=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-first-half-ledgers.json'
        self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),json.loads(p.read_text(encoding='utf-8')))
        self.assertFalse(self.r['public_proof_or_payload_changed']);self.assertEqual(self.r['complete_named_steps'],82)
        self.assertFalse(self.r['reached_new_transport']);self.assertFalse(self.r['complete_shorter_derivation'])
        self.assertEqual((self.r['sphere_moves'],self.r['exterior_caps']),(0,0))
        self.assertIn('Outside interactions',self.r['scope']);self.assertIn('sphere changes',self.r['scope'])


if __name__=='__main__':unittest.main()
