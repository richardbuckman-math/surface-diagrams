import unittest
from dataclasses import replace
from surface_diagrams.factorization_explorer import initial_factors, move_factor, global_conjugate_factors
from surface_diagrams.hyperelliptic_homology import IDENTITY
from surface_diagrams.mapping_classes import ConjugatedTwist, exact_action
from surface_diagrams.six_seven_structure import (
    nonseparating_intersection_certificate, six_seven_lattice_certificate,
    sphere_genus_two_lantern,
)


class SixSevenStructureTests(unittest.TestCase):
    def test_mod_sixteen_obstruction_survives_both_hurwitz_directions(self):
        seed=initial_factors()
        expected=nonseparating_intersection_certificate(seed)
        self.assertEqual(expected['pairing_gcd'],4)
        self.assertEqual(expected['modulus'],16)
        self.assertEqual(expected['zero_residue_pairs'],())
        self.assertTrue(expected['rules_out_disjoint_original_halves'])
        def labelled(result):
            return {(a,b):result['unoriented_residues'][i][j]
                    for i,a in enumerate(result['ids'])
                    for j,b in enumerate(result['ids'])}
        state=seed
        # F2 across F3 is a nonseparating/nonseparating change; the next
        # move involves a separating curve. Then test the inverse directions.
        for source,target in ((1,2),(3,2),(2,1),(2,3)):
            state=move_factor(state,source,target)
            actual=nonseparating_intersection_certificate(state)
            self.assertEqual(labelled(actual),labelled(expected))
        moved=global_conjugate_factors(seed,(1,-4,2))
        self.assertEqual(labelled(nonseparating_intersection_certificate(moved)),
                         labelled(expected))
        # A three-point central twist commutes with the half-twist braid, but
        # reverses its chosen homology orientation upstairs. The obstruction
        # must not depend on that purely presentational choice.
        half=seed[1]
        reverse=replace(half,conjugator=half.conjugator+ConjugatedTwist((),3,3).word)
        self.assertEqual(exact_action(half.word),exact_action(reverse.word))
        reversed_state=seed[:1]+(reverse,)+seed[2:]
        result=nonseparating_intersection_certificate(reversed_state)
        self.assertNotEqual(result['residues'],expected['residues'])
        self.assertEqual(labelled(result),labelled(expected))

    def test_width_four_lattice_and_pointwise_fixed_complement(self):
        certificate=six_seven_lattice_certificate()
        self.assertEqual(certificate['basis'],((3,2,0,1),(0,-1,1,0)))
        self.assertEqual(certificate['restricted_product'],((1,0),(0,1)))
        self.assertTrue(all(matrix[i][j]%4==int(i==j)
                            for matrix in certificate['restricted_matrices']
                            for i in range(2) for j in range(2)))
        coefficients=certificate['coefficients']
        self.assertTrue(all(abs(p*s-q*r)==1
                            for (p,q),(r,s) in zip(coefficients,coefficients[1:]+coefficients[:1])))

    def test_lantern_scope_and_transported_configuration(self):
        for conjugator in ((),(2,-4,1)):
            certificate=sphere_genus_two_lantern(conjugator)
            self.assertTrue(certificate['sphere_certificate']['certified'])
            self.assertFalse(certificate['sphere_certificate']['disk_identity'])
            self.assertEqual(certificate['lift_homology'],IDENTITY)
            self.assertEqual(len(certificate['left']),3)
            self.assertEqual(len(certificate['right']),2)

    def test_obstruction_does_not_apply_after_introducing_new_halves(self):
        seed=initial_factors()
        with self.assertRaises(ValueError):
            nonseparating_intersection_certificate((replace(seed[0],power=1),)+seed[1:])


if __name__=='__main__':
    unittest.main()
