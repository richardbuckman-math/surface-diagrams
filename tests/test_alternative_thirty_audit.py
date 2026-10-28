import json
from dataclasses import asdict, replace
from pathlib import Path
import unittest
from unittest.mock import patch

from surface_diagrams.alternative_thirty_audit import audit_alternative_thirty, pure_linking_certificate
from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action, VerificationLimitError
from surface_diagrams.peripheral_sphere import five_point_cap_certificate
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.braid_actions import free_homotopy_key
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.sphere_support_compact import half_endpoints


class AlternativeThirtyAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.public = json.loads((cls.root / 'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
        cls.source = tuple(Factor(**dict(x, conjugator=tuple(x['conjugator']))) for x in cls.public['early_alternative_exterior']['factors'])
        cls.report = audit_alternative_thirty(cls.source)

    def test_two_sphere_moves_are_separate_and_retain_full_discrepancies(self):
        r = self.report
        self.assertEqual((r['audit_transitions'], r['sphere_move_count'], r['cap_stage'], r['complement_stage']), (5, 2, 3, 4))
        sphere = [s for s in r['stages'] if s['kind'] == 'sphere_rewrite']
        self.assertEqual([s['disk_writhe_discrepancy'] for s in sphere], [40, 10])
        for s in sphere:
            self.assertIn('SPHERE MOVE', s['title'])
            self.assertFalse(s['disk_equal'])
            self.assertTrue(s['sphere_certificate']['certified'])
            self.assertTrue(s['local_sphere_certificate']['certified'])
            self.assertEqual(homology_action(s['disk_discrepancy']), IDENTITY)
            self.assertEqual(homology_action(s['local_disk_discrepancy']), IDENTITY)
            self.assertNotEqual(exact_action(product(s['local_before']), 6), exact_action(product(s['local_after']), 6))
        self.assertEqual([s['kind'] for s in r['stages'][:3]], ['start', 'disk_hurwitz_block', 'disk_combine'])
        self.assertEqual(r['stages'][1]['adjacent_moves'], 3)

    def test_paired_cap_keeps_the_lift_that_single_caps_would_change(self):
        r = self.report
        cap = r['stages'][r['cap_stage']]
        self.assertEqual(len(cap['local_before']), 1)
        f = cap['local_before'][0]
        self.assertEqual(f, Factor('sphere.thirty.double-exterior', (), 1, 5, 2))
        self.assertEqual(cap['local_after'], ())
        self.assertTrue(five_point_cap_certificate(2)['lift_preserving'])
        self.assertFalse(five_point_cap_certificate(1)['lift_preserving'])
        self.assertEqual(r['capped_exterior_power'], 2)

    def test_complement_is_the_actual_26_curve_not_an_endpoint_guess(self):
        s = self.report['stages'][self.report['complement_stage']]
        a, b = s['local_before'][0], s['local_after'][0]
        self.assertEqual((a.points, a.first, b.points, b.first), (4, 1, 2, 5))
        self.assertEqual(a.conjugator, b.conjugator)
        self.assertEqual(half_endpoints(b.mapping_class), (2, 6))
        self.assertEqual(s['local_disk_discrepancy'], reduce_word(a.word + inverse_word(b.word)))
        self.assertIn(5, tuple(abs(x) for x in b.word))

    def test_every_ordered_pair_expansion_is_disk_exact_and_ending_has_positive_lift(self):
        r = self.report
        self.assertEqual((len(r['pairs']), len(r['factors']), r['retained_pair_expansions']), (14, 30, 14))
        self.assertTrue(all(f.half and f.power == 1 and f.points == 2 for f in r['factors']))
        self.assertEqual(reduce_word(product(r['pairs'])), reduce_word(product(r['factors'])))
        for split in r['stages'][-1]['factor_splits']:
            self.assertFalse(split['disk_discrepancy'])
            self.assertFalse(reduce_word(product(split['local_before']) + inverse_word(product(split['local_after']))))
        self.assertEqual(homology_action(product(r['factors'])), IDENTITY)
        self.assertTrue(r['sphere_certificate']['certified'])
        self.assertEqual(r['endpoint_component_sizes'], (6,))
        self.assertEqual(sum(1 if x > 0 else -1 for x in product(r['factors'])), 30)

    def test_linking_spectrum_excludes_even_half_hurwitz_and_disk_global_frames(self):
        r = self.report
        actual = r['disk_linking']['linking_matrix']
        self.assertEqual(r['disk_linking']['off_diagonal_spectrum'], ((0, 4), (1, 7), (2, 4)))
        self.assertEqual(r['standard_disk_linking']['off_diagonal_spectrum'], ((1, 15),))
        self.assertEqual(actual[1], (2, 0, 2, 2, 2, 1))
        self.assertEqual(actual[5], (0, 1, 0, 0, 0, 0))
        for src, dst in ((3, 4), (4, 3)):
            m = research_hurwitz_move(r['factors'], src, dst)
            self.assertFalse(m['disk_word_certificate']['discrepancy'])
            self.assertNotEqual(tuple(half_endpoints(f.mapping_class) for f in m['factors']), r['endpoint_edges'])
            self.assertEqual(pure_linking_certificate(product(m['factors']))['linking_matrix'], actual)
        for frame in ((1,), (2, 3), (5, 4, -2)):
            moved = frame + product(r['factors']) + inverse_word(frame)
            self.assertEqual(pure_linking_certificate(moved)['off_diagonal_spectrum'], ((0, 4), (1, 7), (2, 4)))
        self.assertTrue(r['disk_only_hurwitz_and_global_conjugation_excluded'])
        self.assertTrue(r['sphere_hurwitz_equivalence_unknown'])

    def test_linking_tracker_counts_labeled_crossings_and_rejects_nonpure_or_unknown(self):
        self.assertEqual(pure_linking_certificate((1, 1), 3)['linking_matrix'], ((0, 1, 0), (1, 0, 0), (0, 0, 0)))
        self.assertEqual(pure_linking_certificate((-1, -1), 2)['linking_matrix'], ((0, -1), (-1, 0)))
        self.assertEqual(pure_linking_certificate((1, 2) * 3, 3)['off_diagonal_spectrum'], ((1, 3),))
        self.assertEqual(pure_linking_certificate((1, 2, 1, -2, -1, -2), 3)['off_diagonal_spectrum'], ((0, 3),))
        for word, n in [((1,), 3), ((0,), 3), ((True,), 3), ((3,), 3), ((), True)]:
            with self.assertRaises(ValueError): pure_linking_certificate(word, n)
        with self.assertRaises(VerificationLimitError): pure_linking_certificate((1, 1), max_letters=1)
        with self.assertRaises(ValueError): pure_linking_certificate((), max_letters=False)

    def test_uncertified_sphere_or_wrong_lift_never_succeeds(self):
        with patch('surface_diagrams.alternative_thirty_audit.sphere_chain_certificate', return_value={'certified': False}):
            with self.assertRaises(VerificationLimitError): audit_alternative_thirty(self.source)
        negative = homology_action((1, 2, 3, 4) * 5)
        with patch('surface_diagrams.alternative_thirty_audit.homology_action', return_value=negative):
            with self.assertRaises(ValueError): audit_alternative_thirty(self.source)
        with self.assertRaises(ValueError): audit_alternative_thirty(self.source[:-1])

    def test_eight_unchanged_point_star_candidates_retain_nonabelian_failures(self):
        r = self.report
        p = r['point_star_probe']
        self.assertEqual((p['tested_candidates'], p['matched_candidates']), (8, 0))
        self.assertFalse(p['applied'])
        self.assertTrue(p['unchanged_subsequences_only'])
        self.assertNotEqual(p['canonical_lift_homology'], IDENTITY)
        self.assertTrue(p['canonical_sphere_certificate']['certified'])
        frame = p['global_frame']
        for candidate in p['candidates']:
            selected = tuple(replace(r['pairs'][i], power=1) for i in candidate['indices'])
            split = split_fixed_last_strand(frame + product(selected) + inverse_word(frame), 6)
            self.assertEqual(split.kernel_loop, candidate['kernel_loop'])
            self.assertEqual(exact_action(split.shadow_word, 5), exact_action((), 5))
            self.assertNotEqual(free_homotopy_key(split.kernel_loop), free_homotopy_key((1, 2, 3, 4, 5)))

    def test_coupled_positive_star_swap_is_certified_but_not_reached(self):
        r = self.report
        s = r['point_star_probe']['next_peripheral_star_substitution']
        self.assertEqual(s['kind'], 'sphere_relation_target')
        self.assertFalse(s['applied'])
        self.assertTrue(s['requires_transport'])
        self.assertIn('TARGET ONLY', s['title'])
        self.assertIn('SPHERE', s['title'])
        self.assertEqual((len(s['local_before']), len(s['local_after'])), (5, 5))
        self.assertTrue(all(not f.half and f.power == 1 for f in s['local_before'] + s['local_after']))
        self.assertEqual(s['source_lift_homology'], s['target_lift_homology'])
        self.assertNotEqual(s['source_lift_homology'], IDENTITY)
        self.assertEqual(s['lift_homology'], IDENTITY)
        self.assertTrue(s['sphere_certificate']['certified'])
        self.assertEqual(s['disk_writhe_discrepancy'], 0)
        a, b = s['source_linking']['linking_matrix'], s['target_linking']['linking_matrix']
        self.assertNotEqual(a, b)
        fixed = tuple(tuple(r['disk_linking']['linking_matrix'][i][j] - a[i][j] + b[i][j] for j in range(6)) for i in range(6))
        self.assertEqual(fixed, r['standard_disk_linking']['linking_matrix'])
        # Fixing abelianization is only a target, never a full word match.
        self.assertTrue(r['sphere_hurwitz_equivalence_unknown'])

    def test_saved_audit_is_reproducible_and_does_not_claim_a_new_proof(self):
        saved = json.loads((self.root / 'docs/proofs/six-seven-alternative-thirty.json').read_text(encoding='utf-8'))
        self.assertEqual(saved, json.loads(json.dumps(self.report, default=asdict)))
        self.assertFalse(self.report['applied_to_public_replay'])
        self.assertFalse(self.report['replacement_for_full_proof'])
        self.assertFalse(self.report['complete_named_derivation'])
        self.assertEqual(self.public['named_full_route']['summary']['graphical_steps'], 82)
        self.assertEqual(self.public['early_alternative_exterior']['graphical_steps'], 8)


if __name__ == '__main__': unittest.main()
