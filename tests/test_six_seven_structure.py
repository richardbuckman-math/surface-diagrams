import json
import unittest
from dataclasses import replace
from surface_diagrams.factorization_explorer import initial_factors, move_factor, global_conjugate_factors,product,export_factors,parse_factors
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import ConjugatedTwist, exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.sphere_actions import sphere_curve_action,sphere_inner_certificate
from surface_diagrams.six_seven_structure import (
    nonseparating_intersection_certificate, six_seven_lattice_certificate,
    sphere_genus_two_lantern,
    sphere_root_half_transport,root_transport_consolidation,six_half_stabilizer_audit,
    root_pair_lantern, root_cluster_lantern_route, SignedResearchFactor,
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

    def test_two_separating_roots_transport_original_f3_to_f9_on_sphere(self):
        certificate = sphere_root_half_transport()
        self.assertTrue(certificate['sphere_certificate']['certified'])
        self.assertFalse(certificate['sphere_certificate']['disk_identity'])
        self.assertEqual(certificate['lift_homology'], IDENTITY)
        source = supported_class(certificate['source'].mapping_class)
        target = supported_class(certificate['target'].mapping_class)
        self.assertEqual(sphere_curve_action(certificate['transport'], source),
                         sphere_curve_action((), target))
        roots = certificate['roots']
        self.assertNotEqual(sphere_curve_action(roots[1].word + roots[0].word, source),
                            sphere_curve_action((), target))

    def test_root_route_records_the_one_sphere_step_and_every_disk_step(self):
        result = root_transport_consolidation()
        stages = result['stages']
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertEqual(sum(row['kind'] == 'sphere_rewrite' for row in stages), 1)
        expected = exact_action(product(initial_factors()))
        for row in stages:
            actual = exact_action(product(row['factors']))
            self.assertEqual(homology_action(product(row['factors'])), IDENTITY)
            if row['kind'] == 'sphere_rewrite':
                self.assertNotEqual(actual, expected)
                self.assertFalse(row['sphere_certificate']['disk_identity'])
                self.assertTrue(row['sphere_certificate']['certified'])
                expected = actual
            else:
                self.assertEqual(actual, expected)
        self.assertEqual(len(stages[-1]['factors']), 14)
        pair = stages[-1]['factors'][2]
        self.assertEqual((pair.points, pair.power, pair.half), (2, 1, False))
        self.assertTrue(result['final_sphere_certificate']['certified'])

    def test_torelli_product_does_not_fix_any_standard_chain_arc(self):
        certificate = six_half_stabilizer_audit()
        self.assertEqual(certificate['lift_homology'], IDENTITY)
        self.assertTrue(certificate['all_standard_chain_arcs_moved'])
        self.assertEqual(len(certificate['arcs']), 5)
        self.assertTrue(certificate['all_original_supports_moved'])
        self.assertEqual(len(certificate['original_supports']), 13)

    def test_cluster_lantern_is_exact_in_disk_with_point_cap_correction(self):
        certificate = root_pair_lantern()
        left, right = certificate['left'], certificate['right']
        self.assertEqual(exact_action(product(left)), exact_action(product(right)))
        self.assertEqual([enclosed_boundaries(f.mapping_class, 6) for f in left],
                         [(2, 5, 6), (3, 4, 6), (2, 3, 4, 5)])
        self.assertEqual([enclosed_boundaries(f.mapping_class, 6) for f in right],
                         [(2, 3, 4, 5, 6), (2, 5), (3, 4)])
        delta = tuple(sum(point in enclosed_boundaries(f.mapping_class, 6) for f in left)
                      - sum(point in enclosed_boundaries(f.mapping_class, 6) for f in right)
                      for point in range(1, 7))
        self.assertEqual(delta, (0, 0, 0, 0, 0, 1))
        dropped = product(left) + inverse_word(product(right[1:]))
        self.assertTrue(sphere_inner_certificate(dropped)['certified'])
        self.assertEqual(homology_action(dropped),
                         tuple(tuple(-x for x in row) for row in IDENTITY))

    def test_lantern_explains_exact_disk_transport_and_checked_squared_relation(self):
        certificate = root_pair_lantern()
        r = certificate['reduced_transport_word']
        source, target = certificate['source'], certificate['target']
        self.assertEqual(exact_action(r + source.word + inverse_word(r)),
                         exact_action(target.word))
        discrepancy = certificate['squared_disk_discrepancy']
        self.assertFalse(certificate['squared_sphere_certificate']['disk_identity'])
        self.assertTrue(certificate['squared_sphere_certificate']['certified'])
        self.assertEqual(homology_action(discrepancy), IDENTITY)
        self.assertFalse(certificate['applied_to_full_factorization'])
        endpoint = root_transport_consolidation()['stages'][-1]['factors']
        for ids, conjugator in zip(certificate['endpoint_pair_ids'],
                                   certificate['endpoint_pair_conjugators']):
            for name, root in zip(ids, certificate['left'][:2]):
                actual = next(f for f in endpoint if f.id == name)
                self.assertEqual(exact_action(actual.word),
                                 exact_action(conjugator + root.word + inverse_word(conjugator)))
        source_index = next(i for i, f in enumerate(endpoint) if f.id == 'F13.2')
        ready = move_factor(endpoint, source_index, 11)
        self.assertEqual([f.id for f in ready[8:12]],
                         ['F10.1', 'F13.1', 'F10.2', 'F13.2'])
        self.assertEqual(exact_action(product(ready)), exact_action(product(endpoint)))

    def test_signed_research_hurwitz_moves_and_positive_workspace_boundary(self):
        inverse = SignedResearchFactor('inverse', (), 2, 4, sign=-1)
        half = SignedResearchFactor('half', (), 1, 2, half=True)
        self.assertEqual(inverse.word, inverse_word(inverse.mapping_class.word))
        seed = (inverse, half)
        for source, target in ((0, 1), (1, 0)):
            moved = move_factor(seed, source, target)
            self.assertEqual(exact_action(product(moved)), exact_action(product(seed)))
            self.assertEqual(next(f for f in moved if f.id == 'inverse').sign, -1)
        with self.assertRaises(ValueError):
            SignedResearchFactor('bad', (), 1, 2, sign=0)
        # A saved research state must not silently enter the positive-only lab.
        with self.assertRaisesRegex(ValueError, 'Saved braid word disagrees'):
            parse_factors(json.loads(json.dumps(export_factors(seed))))

    def test_both_transported_cluster_lanterns_have_complete_scope_certificates(self):
        result = root_cluster_lantern_route()
        stages = result['stages']
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertEqual(len(stages), 8)
        self.assertEqual(sum(stage['kind'] == 'disk_lantern' for stage in stages), 2)
        previous = exact_action(product(stages[0]['factors']))
        for stage in stages:
            word = product(stage['factors'])
            self.assertEqual(homology_action(word), IDENTITY)
            actual = exact_action(word)
            if stage['kind'] == 'sphere_rewrite':
                self.assertNotEqual(actual, previous)
                self.assertTrue(stage['sphere_certificate']['certified'])
                self.assertFalse(stage['sphere_certificate']['disk_identity'])
                self.assertEqual(homology_action(stage['disk_discrepancy']), IDENTITY)
                if 'removed_factors' in stage:
                    self.assertEqual(len(stage['removed_factors']), 2)
                    minus = tuple(tuple(-x for x in row) for row in IDENTITY)
                    for peripheral in stage['removed_factors']:
                        self.assertEqual(homology_action(peripheral.word), minus)
                else:
                    before, after = stage['local_before'][0], stage['local_after'][0]
                    self.assertEqual(sphere_curve_action((), supported_class(before.mapping_class)),
                                     sphere_curve_action((), supported_class(after.mapping_class)))
                    self.assertEqual(after.sign, -1)
            else:
                self.assertEqual(actual, previous)
                if stage['kind'] == 'disk_lantern':
                    self.assertEqual(exact_action(product(stage['local_before'])),
                                     exact_action(product(stage['local_after'])))
                    self.assertEqual([f.sign for f in stage['local_after']], [1, 1, 1, -1])
            previous = actual
        endpoint = stages[-1]['factors']
        self.assertEqual(len(endpoint), 16)
        self.assertEqual([f.id for f in endpoint if f.sign < 0],
                         ['L1.Q.complement', 'L2.Q.complement'])
        self.assertTrue(all(f.points == 2 for f in endpoint if f.sign < 0))
        self.assertTrue(result['final_sphere_certificate']['certified'])
        candidate = result['direct_lantern_candidate']
        self.assertFalse(candidate['fits_standard_pair_lantern'])
        matrix = candidate['algebraic_intersections']
        self.assertEqual([abs(matrix[i][j]) for i, j in ((0, 1), (0, 2), (1, 2))],
                         [1, 3, 3])


if __name__=='__main__':
    unittest.main()
