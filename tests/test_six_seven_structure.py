import json
import unittest
from dataclasses import replace
from surface_diagrams.factorization_explorer import initial_factors, move_factor, global_conjugate_factors,product,export_factors,parse_factors,import_factors
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
    three_root_half_transport, three_root_transport_consolidation,
    f2_f7_cluster_lantern, three_root_prefix_lantern,
    three_root_lantern_reduction, three_root_residual_lantern,
    three_root_half_lantern_compression,
    three_root_petal_exchange,
    research_hurwitz_move, three_root_cross_petal_lantern,
    three_root_cross_cluster_lantern,
    three_root_tail_cluster_lantern,
    three_root_tail_fixedness_audit,
)


class SixSevenStructureTests(unittest.TestCase):
    def test_tail_cluster_retains_the_inverse_and_the_unit_deck_sign(self):
        result = three_root_tail_cluster_lantern()
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertFalse(result['final_all_factors_positive'])
        self.assertEqual(result['inner_clusters'], ((3, 6), (5,), (4,)))
        self.assertTrue(result['complement_unit_sphere_certificate']['certified'])
        self.assertEqual(result['complement_unit_lift_homology'],
                         tuple(tuple(-x for x in row) for row in IDENTITY))
        self.assertEqual(homology_action(result['complement_unit_disk_discrepancy']),
                         result['complement_unit_lift_homology'])
        previous = None
        for stage in result['stages']:
            state = stage['factors']
            self.assertEqual(homology_action(product(state)), IDENTITY)
            if stage['kind'] == 'disk_hurwitz':
                self.assertEqual(stage['disk_word_certificate']['discrepancy'], ())
                self.assertEqual(previous[stage['source']], state[stage['target']])
            elif stage['kind'].startswith('disk_'):
                self.assertEqual(exact_action(product(stage['local_before'])),
                                 exact_action(product(stage['local_after'])))
            elif stage['kind'] == 'sphere_rewrite':
                self.assertTrue(stage['sphere_certificate']['certified'])
                self.assertEqual(homology_action(stage['disk_discrepancy']), IDENTITY)
            previous = state
        self.assertEqual(len(previous), 15)
        self.assertEqual(tuple(f.id for f in previous if f.sign < 0), ('tail.inverse.Q45',))
        self.assertEqual(previous[0].id, 'tail.P12.square')
        self.assertEqual(previous[0].power, 2)
        self.assertEqual(len(result['direct_cancellation_attempts']), 8)
        self.assertTrue(all(not a['matches'] for a in result['direct_cancellation_attempts']))
        self.assertTrue(result['final_sphere_certificate']['certified'])
        # Dropping the red inverse row changes the closed lift.
        self.assertNotEqual(homology_action(product(tuple(f for f in previous if f.sign > 0))), IDENTITY)
        audit = three_root_tail_fixedness_audit(result)
        self.assertEqual(len(audit['samples']), 4)
        self.assertEqual(len(audit['disk_moves']), 6)
        self.assertTrue(all(not row['certificate']['fixed'] for row in audit['samples']))
        self.assertTrue(all(move['disk_word_certificate']['discrepancy'] == ()
                            for move in audit['disk_moves']))
        bounded = audit['samples'][2]
        self.assertEqual(len(bounded['certificate']['chart_class']), 4846)
        self.assertEqual(bounded['certificate']['first_noncommuting_syllable'], (-3,-1))
        # Full image expansion cannot decide this within the existing bound;
        # the normal-form calculation gives an exact negative certificate.
        from surface_diagrams.mapping_classes import VerificationLimitError
        with self.assertRaises(VerificationLimitError):
            sphere_curve_action(replace(bounded['c12'],power=1).word, bounded['source_class'])

    def test_cross_cluster_lantern_cancels_the_actual_pair_and_combines_its_petal(self):
        result = three_root_cross_cluster_lantern()
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertTrue(result['final_all_factors_positive'])
        self.assertEqual(result['inner_clusters'], ((3, 5), (4,), (6,)))
        self.assertEqual(result['remaining_odd_root_ids'], ('cross.C4.unused',))
        self.assertNotIn('final_lefschetz_counts', result)
        sphere_steps = []
        previous = None
        for stage in result['stages']:
            state = stage['factors']
            self.assertEqual(homology_action(product(state)), IDENTITY)
            if stage['kind'] == 'disk_hurwitz':
                self.assertEqual(stage['disk_word_certificate']['discrepancy'], ())
                self.assertEqual(previous[stage['source']], state[stage['target']])
            elif stage['kind'].startswith('disk_'):
                self.assertEqual(exact_action(product(stage['local_before'])),
                                 exact_action(product(stage['local_after'])))
            elif stage['kind'] == 'sphere_rewrite':
                sphere_steps.append(stage)
                self.assertTrue(stage['sphere_certificate']['certified'])
                self.assertEqual(homology_action(stage['disk_discrepancy']), IDENTITY)
            previous = state
        self.assertEqual(len(sphere_steps), 2)
        loop_witness = sphere_steps[0]['disk_nonidentity_witness']
        self.assertNotEqual(loop_witness['reference'], loop_witness['image'])
        self.assertEqual(loop_witness['image'], supported_class(
            ConjugatedTwist(sphere_steps[0]['disk_discrepancy'], 2, 2)))
        self.assertEqual(sphere_steps[1]['disk_nonidentity_witness']['exponent_sum'], 10)
        cancellation = next(s for s in result['stages'] if s['kind'] == 'disk_cancel')
        self.assertEqual(tuple(f.sign for f in cancellation['local_before']), (-1, 1))
        self.assertEqual(cancellation['local_before'][1].id, 'new.P34')
        self.assertEqual(len(previous), 14)
        self.assertEqual(sum(f.points == 3 and f.power == 2 for f in previous), 2)
        self.assertEqual(previous[1].id, 'cross.P35.square')
        self.assertEqual(previous[1].power, 2)
        self.assertTrue(result['final_sphere_certificate']['certified'])

    def test_research_hurwitz_uses_an_exact_freely_reduced_word_certificate(self):
        seed = (SignedResearchFactor('positive', (2,), 1, 2, half=True),
                SignedResearchFactor('negative', (-1,), 2, 2, sign=-1))
        for source, target in ((0, 1), (1, 0)):
            result = research_hurwitz_move(seed, source, target)
            self.assertEqual(result['factors'][target], seed[source])
            self.assertEqual(result['disk_word_certificate'],
                             dict(method='free reduction', discrepancy=()))
            self.assertEqual(exact_action(product(seed)), exact_action(product(result['factors'])))
            restored = research_hurwitz_move(result['factors'], target, source)
            self.assertEqual(exact_action(product(restored['factors'])), exact_action(product(seed)))
        for source, target in ((0, 0), (-1, 0), (0, 2), (True, 0)):
            with self.assertRaises(ValueError):
                research_hurwitz_move(seed, source, target)

    def test_cross_stage_petals_have_a_geometric_inverse_pc_lantern(self):
        result = three_root_cross_petal_lantern()
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertTrue(result['final_all_factors_positive'])
        self.assertEqual(result['remaining_odd_root_ids'], ('cross.rose.root',))
        self.assertNotIn('final_lefschetz_counts', result)
        previous = None
        from surface_diagrams.braid_actions import reduce_word
        for stage in result['stages']:
            state = stage['factors']
            if stage['kind'] == 'disk_hurwitz':
                self.assertEqual(stage['disk_word_certificate']['discrepancy'], ())
                self.assertEqual(reduce_word(product(stage['local_before']) +
                                 inverse_word(product(stage['local_after']))), ())
                self.assertEqual(previous[stage['source']], state[stage['target']])
            self.assertEqual(homology_action(product(state)), IDENTITY)
            previous = state
        last = result['stages'][-1]
        self.assertEqual(tuple(f.id for f in last['local_before']),
                         ('prefix.P45', 'residual.P34', 'C5.rose.1.1'))
        self.assertEqual(enclosed_boundaries(previous[0].mapping_class, 6), (3, 4, 5))
        self.assertEqual(last['exact_sphere_supports'], tuple(sphere_curve_action(
            (), supported_class(f.mapping_class)) for f in last['pc_rose_model']))
        self.assertEqual(exact_action(product(last['pc_rose_model'])),
                         exact_action(product(last['local_after'])))
        self.assertTrue(last['sphere_certificate']['certified'])
        self.assertEqual(homology_action(last['disk_discrepancy']), IDENTITY)
        witness = last['disk_nonidentity_witness']
        self.assertNotEqual(witness['reference'], witness['image'])
        self.assertEqual(witness['image'], supported_class(
            ConjugatedTwist(last['disk_discrepancy'], 1, 2)))
        self.assertTrue(result['final_sphere_certificate']['certified'])
        self.assertEqual(len(previous), 15)
        self.assertEqual(sum(f.points == 3 and f.power % 2 for f in previous), 1)

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

    def test_three_roots_transport_original_f2_to_f7_in_the_disk(self):
        result = three_root_half_transport()
        self.assertEqual([f.id for f in result['roots']],
                         ['F8.root', 'F10.root', 'F1.root'])
        self.assertEqual(exact_action(result['transported'].word),
                         exact_action(result['target'].word))
        self.assertTrue(result['sphere_certificate']['disk_identity'])
        self.assertEqual(result['lift_homology'], IDENTITY)
        self.assertEqual(result['intermediate'].conjugator, (-3, -5))
        self.assertEqual(result['intermediate'].first, 4)

    def test_second_original_pair_route_is_disk_exact_and_lab_importable(self):
        result = three_root_transport_consolidation()
        self.assertTrue(result['all_steps_exact_in_disk'])
        self.assertFalse(result['complete_structural_derivation_found'])
        expected = exact_action(product(initial_factors()))
        for stage in result['stages']:
            self.assertTrue(stage['kind'] == 'start' or stage['kind'].startswith('disk_'))
            self.assertEqual(exact_action(product(stage['factors'])), expected)
            self.assertEqual(homology_action(product(stage['factors'])), IDENTITY)
            document = json.loads(json.dumps(export_factors(stage['factors'])))
            self.assertEqual(parse_factors(document), stage['factors'])
        endpoint = result['stages'][-1]['factors']
        self.assertEqual(len(endpoint), 15)
        pair = next(f for f in endpoint if f.id == 'F2+F7.disk')
        self.assertFalse(pair.half)
        self.assertEqual((pair.points, pair.power), (2, 1))
        self.assertEqual(import_factors(json.loads(json.dumps(export_factors(endpoint)))), endpoint)
        audit = result['algebraically_disjoint_pair']
        self.assertEqual(audit['algebraic_intersection'], 0)
        self.assertFalse(audit['sphere_support_fixed'])
        self.assertNotEqual(audit['original_curve'], audit['image_curve'])
        # C1 started before F2; applying it there is essential to this replay.
        shift = next(stage for stage in result['stages']
                     if stage.get('source') == 1 and stage.get('target') == 2)
        source = next(f for f in shift['factors'] if f.id == 'F2')
        self.assertEqual(exact_action(source.word),
                         exact_action(three_root_half_transport()['intermediate'].word))

    def test_second_cluster_lantern_and_complementary_root_keep_the_deck_sign(self):
        result = f2_f7_cluster_lantern()
        self.assertEqual(exact_action(product(result['left'])), exact_action(product(result['right'])))
        self.assertEqual([enclosed_boundaries(f.mapping_class, 6) for f in result['left']],
                         [(3, 4, 5), (2, 5, 6), (2, 3, 4, 6)])
        self.assertEqual([enclosed_boundaries(f.mapping_class, 6) for f in result['right']],
                         [(2, 3, 4, 5, 6), (3, 4), (2, 6)])
        delta = tuple(sum(point in enclosed_boundaries(f.mapping_class, 6) for f in result['left'])
                      - sum(point in enclosed_boundaries(f.mapping_class, 6) for f in result['right'])
                      for point in range(1, 7))
        self.assertEqual(delta, (0, 0, 0, 0, 1, 0))
        self.assertTrue(result['root_sphere_certificate']['certified'])
        self.assertFalse(result['root_sphere_certificate']['disk_identity'])
        self.assertEqual(result['root_lift_homology'], tuple(tuple(-x for x in row) for row in IDENTITY))
        self.assertTrue(result['squared_sphere_certificate']['certified'])
        self.assertEqual(homology_action(result['squared_disk_discrepancy']), IDENTITY)
        endpoint = {f.id: f for f in three_root_transport_consolidation()['stages'][-1]['factors']}
        g = result['endpoint_pair_conjugator']
        for name, root in zip(result['endpoint_pair_ids'], result['left'][:2]):
            self.assertEqual(exact_action(endpoint[name].word),
                             exact_action(g + root.word + inverse_word(g)))
        terms = result['remaining_c13_half_lantern']
        self.assertEqual(exact_action(product(terms)),
                         exact_action(result['remaining_c13_complement'].word))
        self.assertEqual(exact_action(result['negative_pair_support'].word),
                         exact_action(replace(terms[2], power=1).word))
        self.assertEqual(result['c13_root_lift_homology'],
                         tuple(tuple(-x for x in row) for row in IDENTITY))
        self.assertTrue(sphere_inner_certificate(result['c13_squared_disk_discrepancy'])['certified'])
        self.assertEqual(homology_action(result['c13_squared_disk_discrepancy']), IDENTITY)
        residual = result['residual_root_lantern']
        self.assertTrue(residual['sphere_certificate']['certified'])
        self.assertFalse(residual['sphere_certificate']['disk_identity'])
        self.assertEqual(homology_action(residual['disk_discrepancy']), IDENTITY)
        self.assertFalse(residual['applied_to_endpoint'])

    def test_new_prefix_exposes_a_sphere_genus_two_lantern_but_not_a_disk_step(self):
        result = three_root_prefix_lantern()
        before, after = result['stages']
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertEqual(len(before['factors']), 15)
        self.assertEqual(len(after['factors']), 14)
        self.assertTrue(after['sphere_certificate']['certified'])
        self.assertFalse(after['sphere_certificate']['disk_identity'])
        self.assertEqual(homology_action(after['disk_discrepancy']), IDENTITY)
        self.assertTrue(sphere_inner_certificate(product(after['factors']))['certified'])
        self.assertEqual(homology_action(product(after['factors'])), IDENTITY)
        self.assertEqual([enclosed_boundaries(f.mapping_class, 6) for f in after['local_after']],
                         [(4, 5), (1, 2)])
        self.assertEqual(sum(f.points == 3 and f.power % 2 == 1 for f in after['factors']), 4)
        # These positive records belong to a different disk chart, so an exact
        # disk-only workspace must reject them despite the valid sphere lift.
        with self.assertRaisesRegex(ValueError, 'Exact disk action verification failed'):
            import_factors(json.loads(json.dumps(export_factors(after['factors']))))

    def test_half_lantern_removes_the_temporary_negative_pair(self):
        result = three_root_lantern_reduction()
        self.assertFalse(result['complete_structural_derivation_found'])
        previous = None
        saw_negative = False
        for stage in result['stages']:
            state = stage['factors']
            saw_negative |= any(f.sign < 0 for f in state)
            self.assertEqual(homology_action(product(state)), IDENTITY)
            if stage['kind'] == 'disk_hurwitz':
                a, b = sorted((stage['source'], stage['target']))
                self.assertEqual(b - a, 1)
                self.assertEqual(exact_action(product(previous[a:b + 1])),
                                 exact_action(product(state[a:b + 1])))
                self.assertEqual(previous[stage['source']], state[stage['target']])
            elif stage['kind'].startswith('disk_'):
                self.assertEqual(exact_action(product(stage['local_before'])),
                                 exact_action(product(stage['local_after'])))
            elif stage['kind'] == 'sphere_rewrite':
                self.assertTrue(stage['sphere_certificate']['certified'])
                self.assertFalse(stage['sphere_certificate']['disk_identity'])
                self.assertEqual(homology_action(stage['disk_discrepancy']), IDENTITY)
                if 'root_before' in stage:
                    self.assertEqual(len(stage['removed_factors']), 1)
                    self.assertEqual(stage['component_lift_homology'],
                                     tuple(tuple(-x for x in row) for row in IDENTITY))
            previous = state
        self.assertTrue(saw_negative)
        self.assertTrue(result['final_all_factors_positive'])
        self.assertEqual(len(previous), 18)
        self.assertTrue(all(f.sign == 1 for f in previous))
        self.assertEqual(result['remaining_odd_root_ids'], ('F10.2', 'F12.root+F12'))
        root_chart = result['residual_root_chart']
        by_id = {f.id: f for f in previous}
        for name, model in zip(result['remaining_odd_root_ids'], result['residual_root_models']):
            self.assertEqual(exact_action(by_id[name].word),
                             exact_action(root_chart + model.word + inverse_word(root_chart)))
        self.assertEqual(result['stages'][-1]['kind'], 'disk_cancel')
        self.assertEqual(result['stages'][-1]['local_before'][0].sign, -1)
        self.assertEqual(result['stages'][-1]['local_before'][1].power, 2)
        self.assertEqual(result['stages'][-1]['local_after'][0].power, 1)
        self.assertTrue(result['final_sphere_certificate']['certified'])

    def test_residual_lantern_uses_actual_root_order_and_cancels_the_prefix_pair(self):
        result = three_root_residual_lantern()
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertEqual(result['final_lefschetz_counts'], (24, 3))
        self.assertEqual(result['remaining_odd_root_ids'], ())
        self.assertTrue(result['final_all_factors_positive'])
        previous = None
        sphere_steps = []
        for stage in result['stages']:
            state = stage['factors']
            self.assertEqual(homology_action(product(state)), IDENTITY)
            if stage['kind'] == 'disk_hurwitz':
                a, b = sorted((stage['source'], stage['target']))
                self.assertEqual(b - a, 1)
                self.assertEqual(exact_action(product(previous[a:b + 1])),
                                 exact_action(product(state[a:b + 1])))
                self.assertEqual(previous[stage['source']], state[stage['target']])
            elif stage['kind'].startswith('disk_'):
                self.assertEqual(exact_action(product(stage['local_before'])),
                                 exact_action(product(stage['local_after'])))
            elif stage['kind'] == 'sphere_rewrite':
                sphere_steps.append(stage)
                self.assertTrue(stage['sphere_certificate']['certified'])
                self.assertFalse(stage['sphere_certificate']['disk_identity'])
                self.assertEqual(homology_action(stage['disk_discrepancy']), IDENTITY)
            previous = state
        self.assertEqual(len(sphere_steps), 2)
        lantern, rechart = sphere_steps
        self.assertEqual([f.id for f in lantern['local_before']],
                         ['F10.2', 'F12.root+F12.1'])
        self.assertEqual([f.sign for f in lantern['local_after']], [1, 1, -1])
        self.assertEqual(rechart['local_before'][0].id, 'residual.Q.complement')
        self.assertEqual(sphere_curve_action((), supported_class(rechart['local_before'][0].mapping_class)),
                         sphere_curve_action((), supported_class(rechart['local_after'][0].mapping_class)))
        last = result['stages'][-1]
        self.assertEqual(last['kind'], 'disk_cancel')
        self.assertEqual([f.sign for f in last['local_before']], [1, -1])
        self.assertEqual(last['local_before'][0].id, 'prefix.P12')
        self.assertEqual(last['local_after'], ())
        self.assertEqual(len(previous), 18)
        self.assertTrue(all(f.sign == 1 for f in previous))
        self.assertTrue(all(f.half or f.points == 2 or f.points == 3 and f.power % 2 == 0
                            for f in previous))
        self.assertTrue(result['final_sphere_certificate']['certified'])

    def test_reverse_half_lantern_compression_keeps_the_uncancelled_inverse(self):
        result = three_root_half_lantern_compression()
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertFalse(result['final_all_factors_positive'])
        previous = None
        for stage in result['stages']:
            state = stage['factors']
            self.assertEqual(homology_action(product(state)), IDENTITY)
            if stage['kind'] == 'disk_hurwitz':
                a, b = sorted((stage['source'], stage['target']))
                self.assertEqual(b - a, 1)
                self.assertEqual(exact_action(product(previous[a:b + 1])),
                                 exact_action(product(state[a:b + 1])))
                self.assertEqual(previous[stage['source']], state[stage['target']])
            elif stage['kind'] == 'disk_half_lantern':
                self.assertEqual(len(stage['local_before']), 6)
                self.assertEqual(exact_action(product(stage['local_before'])),
                                 exact_action(product(stage['local_after'])))
                self.assertEqual([f.sign for f in stage['local_after']], [1, -1])
            previous = state
        self.assertEqual(len(previous), 14)
        self.assertEqual([f.id for f in previous if f.sign == -1], ['inverse.P15'])
        self.assertEqual(result['signed_counts'], dict(positive_nonseparating=14,
            negative_nonseparating=2, positive_separating=4, net_nonseparating=12))
        self.assertEqual(sum(f.power * (1 if f.half else 2) for f in previous
                             if f.points == 2 and f.sign > 0), 14)
        self.assertTrue(result['final_sphere_certificate']['certified'])
        # Omitting the inverse would produce a different closed lift; a net
        # count is not a positive (12,4) relation or a license to drop a factor.
        self.assertNotEqual(homology_action(product(previous[:-1])), IDENTITY)
        self.assertEqual(len(result['positive_equation_left']), 13)
        self.assertEqual(result['positive_equation_target'].sign, 1)
        self.assertEqual(homology_action(product(result['positive_equation_left'])),
                         homology_action(result['positive_equation_target'].word))
        crossing = result['target_crossing_witness']
        self.assertEqual(crossing['factor_id'], 'F3')
        self.assertNotEqual(crossing['target_support'], crossing['image_support'])
        attempts = result['direct_cancellation_attempts']
        self.assertEqual(len(attempts), 5)
        self.assertEqual({a['target_id'] for a in attempts},
                         {'prefix.P45', 'new.P34', 'new.P26', 'residual.P34', 'residual.P26'})
        self.assertTrue(all(not a['matches'] for a in attempts))
        self.assertTrue(all(a['transported_inverse_support'] != a['positive_support']
                            for a in attempts))

    def test_complementary_rose_exchanges_the_separator_and_cancels_the_inverse(self):
        result = three_root_petal_exchange()
        self.assertFalse(result['complete_structural_derivation_found'])
        self.assertTrue(result['final_all_factors_positive'])
        self.assertEqual(result['final_lefschetz_counts'], (24, 3))
        previous = None
        sphere_steps = []
        for stage in result['stages']:
            state = stage['factors']
            self.assertEqual(homology_action(product(state)), IDENTITY)
            if stage['kind'] == 'disk_hurwitz':
                a, b = sorted((stage['source'], stage['target']))
                self.assertEqual(b - a, 1)
                self.assertEqual(exact_action(product(previous[a:b + 1])),
                                 exact_action(product(state[a:b + 1])))
                self.assertEqual(previous[stage['source']], state[stage['target']])
            elif stage['kind'].startswith('disk_'):
                self.assertEqual(exact_action(product(stage['local_before'])),
                                 exact_action(product(stage['local_after'])))
            elif stage['kind'] == 'sphere_rewrite':
                sphere_steps.append(stage)
                self.assertTrue(stage['sphere_certificate']['certified'])
                self.assertFalse(stage['sphere_certificate']['disk_identity'])
                self.assertEqual(homology_action(stage['disk_discrepancy']), IDENTITY)
            previous = state
        self.assertEqual(len(sphere_steps), 1)
        rechart = sphere_steps[0]
        self.assertEqual(rechart['local_before'][0].power, 2)
        self.assertEqual(enclosed_boundaries(rechart['local_before'][0].mapping_class, 6), (2, 4, 6))
        self.assertEqual(enclosed_boundaries(rechart['local_after'][0].mapping_class, 6), (1, 3, 5))
        self.assertEqual(result['complement_unit_lift_homology'],
                         tuple(tuple(-x for x in row) for row in IDENTITY))
        self.assertTrue(result['complement_unit_sphere_certificate']['certified'])
        self.assertEqual(len(previous), 17)
        self.assertEqual(sum(f.half for f in previous), 4)
        self.assertEqual(sum(f.points == 3 for f in previous), 3)
        self.assertNotIn('F5', {f.id for f in previous})
        self.assertIn('C13.recombined', {f.id for f in previous})
        self.assertTrue(all(f.sign == 1 for f in previous))
        self.assertEqual(result['stages'][-1]['local_after'], ())
        self.assertTrue(result['final_sphere_certificate']['certified'])
        lantern = result['prepared_cluster_lantern']
        self.assertFalse(lantern['applied_to_endpoint'])
        self.assertTrue(lantern['sphere_certificate']['certified'])
        self.assertFalse(lantern['sphere_certificate']['disk_identity'])
        self.assertEqual(homology_action(lantern['disk_discrepancy']), IDENTITY)
        self.assertTrue(lantern['second_root_sphere_certificate']['certified'])
        self.assertEqual(homology_action(lantern['second_root_disk_discrepancy']), IDENTITY)
        two = result['prepared_two_lantern_consequence']
        self.assertFalse(two['applied_to_endpoint'])
        self.assertEqual(two['left'], previous[-6:])
        self.assertEqual(two['disk_exponent_sum'], 20)
        self.assertTrue(two['sphere_certificate']['certified'])
        self.assertEqual(homology_action(two['disk_discrepancy']), IDENTITY)
        self.assertEqual([f.sign for f in two['right']], [1, 1, -1, -1])
        self.assertNotEqual(sphere_curve_action((), supported_class(two['right'][2].mapping_class)),
                            sphere_curve_action((), supported_class(two['right'][3].mapping_class)))

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
