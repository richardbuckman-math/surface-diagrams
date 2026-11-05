import json,unittest
from pathlib import Path
from dataclasses import replace,asdict
from hashlib import sha256
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.braid_actions import reduce_word
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.ten_ten_summand_audit import monodromy_homology_audit,necessary_two_interchange_target,published_nakamura_homology_comparison
from examples.analyze_ten_ten_summand import report,SOURCE,PIN
ROOT=Path(__file__).resolve().parents[1]

class TenTenSummandAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report();cls.fs=cls.r['factors']
    def test_exact_source_and_report_are_reproducible_without_replaying_derivation(self):
        self.assertEqual(sha256((ROOT/SOURCE).read_bytes()).hexdigest(),PIN)
        self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),json.loads((ROOT/'docs/proofs/ten-ten-fiber-sum-audit.json').read_bytes()))
    def test_no_literal_seven_factor_block_can_pass_the_integral_necessary_test(self):
        self.assertEqual(len(self.r['literal_four_half_tests']),210)
        self.assertFalse(self.r['literal_passing']);self.assertEqual(self.r['literal_seven_subword_count'],25200)
        self.assertTrue(all(x['matrix']!=IDENTITY for x in self.r['literal_four_half_tests']))
        self.assertTrue(self.r['all_separating_homology_identity'])
    def test_saturated_quotient_and_fixed_vector_are_actual_integral_data(self):
        self.assertEqual(self.r['monodromy_coinvariants'],dict(lattice_rank=3,free_rank=1,torsion=()))
        self.assertEqual(self.r['primitive_common_fixed_vector'],(0,-1,1,0))
        v=self.r['primitive_common_fixed_vector']
        for f in self.fs:
            m=homology_action(f.word);self.assertEqual(tuple(sum(m[i][j]*v[j] for j in range(4)) for i in range(4)),v)
    def test_widths_survive_actual_hurwitz_moves_and_global_changes_of_chart(self):
        expected={x['id']:x['width'] for x in self.r['half_records']}
        changed=research_hurwitz_move(self.fs,11,10)['factors']
        variants=[changed]+[tuple(replace(f,conjugator=reduce_word(g+f.conjugator)) for f in self.fs) for g in ((1,),(-4,),(1,2,-3))]
        for state in variants:
            a=monodromy_homology_audit(state);self.assertEqual({x['id']:x['width'] for x in a['half_records']},expected)
        self.assertEqual(sorted(expected.values()),[1]*7+[4,9,16])
        self.assertEqual(self.r['total_quotient_width'],36)
    def test_mod_twelve_is_only_a_necessary_test_and_forces_the_width_nine_cycle(self):
        self.assertEqual(len(self.r['modular_passing']),35)
        widths={x['id']:x['width'] for x in self.r['half_records']}
        for x in self.r['modular_passing']:
            self.assertEqual(sorted(widths[i] for i in x['ids']),[1,1,1,9])
        target=necessary_two_interchange_target(self.r)
        self.assertEqual(target['matrix'],IDENTITY);self.assertFalse(target['full_genus_two_identity_established'])
        self.assertFalse(self.r['split_found']);self.assertFalse(self.r['indecomposable_proved'])
    def test_actual_quotient_matrices_have_complete_integral_parabolic_conjugators(self):
        q=self.r['quotient_parabolics'];self.assertEqual(q['full_product'],((1,0),(0,1)))
        self.assertEqual(q['pairing'],1);self.assertEqual(q['modulus'],12)
        self.assertEqual([x['width'] for x in q['records']],[x['width'] for x in self.r['half_records']])
        for r in q['records']:
            a=r['conjugator'];self.assertEqual(a[0][0]*a[1][1]-a[0][1]*a[1][0],1)
    def test_failed_geometry_prefixes_are_never_counted_as_reached_routes(self):
        self.assertEqual([x['failure']['raw_score']['maximum'] for x in self.r['rejected_previews']],[27,28,46])
        for x in self.r['rejected_previews']:
            self.assertFalse(x['applied']);self.assertFalse(x['selected_route_reached']);self.assertTrue(x['rejected_before_application'])
            self.assertEqual(x['failure']['raw_move']['disk_word_certificate']['discrepancy'],())
            for q in x['prefix_preview_only']:self.assertTrue(q['individual_presentation_match']['exact_disk_equal'])
        self.assertEqual(self.r['applied_moves'],0)
    def test_published_comparison_distinguishes_monodromies_without_a_section_claim(self):
        self.assertEqual(published_nakamura_homology_comparison()['quotient'],dict(lattice_rank=4,free_rank=0,torsion=()))
        self.assertFalse(self.r['whole_H1_or_fundamental_group_claimed'])
        with self.assertRaises(ValueError):monodromy_homology_audit(self.fs[:-1])

if __name__=='__main__':unittest.main()
