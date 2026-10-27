import json
from dataclasses import replace
from pathlib import Path
import unittest

from surface_diagrams.early_alternative import expose_alternative_early_daisy
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.hyperelliptic_homology import homology_action
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD


class EarlyAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks'
        rows = json.loads((cls.folder / 'certificate.json').read_text())['early_boundary']['chart']['factors']
        cls.source = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator']))) for f in rows)
        cls.route = expose_alternative_early_daisy(cls.source)

    def test_all_reached_states_are_positive_disk_exact_and_keep_the_original_halves(self):
        r = self.route
        self.assertEqual((r['graphical_steps'], r['lantern_operations'], r['adjacent_checks']), (7, 6, 1))
        expected = exact_action(BOUNDARY_WORD * 4, 5)
        halves = tuple(f for f in self.source if f.half)
        for stage in r['stages']:
            for record in (stage,) + stage.get('atomic_steps', ()):
                fs = record['factors']
                self.assertEqual(exact_action(product(fs), 5), expected)
                self.assertEqual(homology_action(product(fs)), homology_action(BOUNDARY_WORD * 4))
                self.assertEqual(tuple(f for f in fs if f.half), halves)
                self.assertLessEqual(max(len(supported_class(f.mapping_class, 5)) for f in fs), 16)
            if stage['kind'] != 'disk_cyclic_start' and 'local_before' in stage:
                self.assertEqual(exact_action(product(stage['local_before']), 5),
                                 exact_action(product(stage['local_after']), 5))
        self.assertFalse(r['replacement_for_full_proof'])
        self.assertFalse(r['complete_named_derivation'])
        self.assertEqual((r['half_twists_introduced'], r['half_twists_remaining'], r['sphere_move_count']), (0, 4, 0))

    def test_cyclic_start_is_an_explicit_conjugation_without_source_centrality_assumption(self):
        stage = self.route['stages'][3]
        before, after = product(stage['local_before']), product(stage['local_after'])
        frame = stage['frame']
        self.assertEqual(exact_action(after, 5), exact_action(frame + before + inverse_word(frame), 5))
        self.assertEqual(stage['factors'][0].id, 'alternative.S2')

    def test_cabled_lantern_has_a_generic_pattern_and_individual_exact_chart_matches(self):
        witness = self.route['lantern_witness']
        self.assertEqual(witness['frame'], (-4, -4))
        move = witness['retained_interchange']
        self.assertFalse(move['disk_word_certificate']['discrepancy'])
        self.assertEqual((move['source'], move['target']), (1, 2))
        self.assertEqual(exact_action(product(witness['canonical_before']), 5),
                         exact_action(product(witness['canonical_after']), 5))
        for check in witness['individual_matches']:
            self.assertTrue(check['exact_disk_equal'])
            self.assertEqual(exact_action(check['actual'].word, 5), exact_action(check['pattern'].word, 5))
        before = self.route['stages'][5]['local_before']
        wrong = before[:1] + before[2:] + before[1:2]
        self.assertNotEqual(exact_action(product(wrong), 5),
                            exact_action(product(self.route['stages'][5]['local_after']), 5))

    def test_actual_q14_t12_square_and_next_p35_supplier_are_kept_distinct(self):
        r = self.route
        self.assertEqual(exact_action(r['actual_q14'].word, 5),
                         exact_action(Factor('q', (-4, 1, 2, 3), 4, 2).word, 5))
        square = next(f for f in r['factors'] if f.id == 'alternative.T12.square')
        self.assertEqual(square, Factor('alternative.T12.square', (), 1, 2, power=2))
        target = r['next_p35']
        self.assertFalse(target['applied'])
        self.assertFalse(target['half_match_claimed'])
        self.assertEqual(exact_action(product(target['daisy_terms']), 5), exact_action(target['source_root'].word, 5))
        self.assertEqual(exact_action(target['daisy_terms'][0].word, 5), exact_action(target['actual_p35'].word, 5))
        for stage in r['stages']:
            if stage['kind'] in ('disk_cluster_lantern', 'disk_pc_daisy'):
                sets = [[enclosed_boundaries(f.mapping_class, 5) for f in stage[k]]
                        for k in ('local_before', 'local_after')]
                self.assertEqual(stage['framed_balance_before_minus_after'], tuple(
                    sum(i in b for b in sets[0]) - sum(i in b for b in sets[1]) for i in range(1, 6)))

    def test_remaining_q14_half_target_is_exact_but_not_applied(self):
        target = self.route['next_half_target']
        self.assertFalse(target['applied'])
        self.assertFalse(target['current_already_matched'])
        self.assertTrue(target['requires_transport'])
        self.assertEqual(target['source_alternative_step'], 6)
        self.assertEqual(target['preparation_operations'], 5)
        a, b, q = target['current_f3'], target['current_f9'], target['required_conjugator']
        self.assertNotEqual(exact_action(a.word, 5), exact_action(b.word, 5))
        self.assertEqual(exact_action(q.word + a.word + inverse_word(q.word), 5), exact_action(b.word, 5))
        for stage in target['stages']:
            self.assertEqual(stage['half_twists'], 4)
            self.assertLessEqual(stage['score']['max_support_word'], 20)
            self.assertNotIn('sphere', stage['kind'])

    def test_invalid_source_cannot_produce_a_route(self):
        with self.assertRaises(ValueError): expose_alternative_early_daisy(self.source[:-1])
        with self.assertRaises(ValueError): expose_alternative_early_daisy((replace(self.source[0], power=2),) + self.source[1:])

    def test_published_alternative_is_separate_from_the_complete_named_proof(self):
        c = json.loads((self.folder / 'certificate.json').read_text())
        d = json.loads((self.folder / 'display-pure.json').read_text())
        self.assertEqual(len(d['routes']['earlyalternate']), 8)
        for a, b in zip(self.route['stages'], d['routes']['earlyalternate']):
            self.assertEqual(a['kind'], b['kind'])
            self.assertEqual(len(a['factors']), len(b['factors']))
            for f, i in zip(a['factors'], b['factors']):
                self.assertEqual(exact_action(f.word), exact_action(d['rows'][i]['word']))
        self.assertEqual(c['named_full_route']['summary']['graphical_steps'], 89)
        self.assertEqual(len(d['routes']['namedfull']), 90)
        self.assertFalse(c['early_alternative_lantern']['replacement_for_full_proof'])
        self.assertFalse(any(s['kind'] == 'sphere_rewrite' for s in d['routes']['earlyalternate']))


if __name__ == '__main__':
    unittest.main()
