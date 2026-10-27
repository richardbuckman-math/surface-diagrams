import json
from pathlib import Path
import unittest
from dataclasses import replace
from surface_diagrams.early_alternative_closure import close_alternative_boundary
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.hyperelliptic_homology import homology_action, IDENTITY
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD


class AlternativeClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks'
        cls.saved = json.loads((cls.folder / 'certificate.json').read_text(encoding='utf-8'))
        cls.source = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator'])))
                           for f in cls.saved['early_alternative_exterior']['factors'])
        cls.route = close_alternative_boundary(cls.source)

    def test_every_state_and_retained_neighbor_is_positive_disk_exact_and_bounded(self):
        r = self.route
        self.assertEqual((r['graphical_steps'], r['adjacent_checks']), (23, 28))
        expected = exact_action(BOUNDARY_WORD * 4, 5)
        peak = 0
        for s in r['stages']:
            for a in (s,) + s.get('atomic_steps', ()):
                fs = a['factors']
                self.assertTrue(all(not f.half and f.power > 0 for f in fs))
                self.assertEqual(exact_action(product(fs), 5), expected)
                self.assertEqual(homology_action(product(fs)), IDENTITY)
                peak = max(peak, max(len(supported_class(f.mapping_class, 5)) for f in fs))
                self.assertNotIn('sphere', a.get('kind', ''))
        self.assertEqual(peak, 16)
        self.assertEqual(r['actual_peak_support_word'], peak)

    def test_actual_root_return_and_two_outer_alignment_are_not_endpoint_guesses(self):
        s = self.route['stages']
        self.assertEqual(s[2]['factors'][2].id, 'alternative.returned.R145')
        # The rose returns the transported loan; its exact matches retain
        # all three actual factors and the necessary internal interchange.
        w = s[2]['named_pattern_witness']
        self.assertEqual(len(w['retained_interchanges']), 1)
        self.assertEqual(len(w['individual_matches']), 3)
        by_id = {f.id: f for f in s[5]['factors']}
        a, b, o, n = (by_id[k] for k in ('alternative.second.I35', 'alternative.return.2',
                                        'alternative.residual.O1234', 'alternative.returned.N'))
        k = b.word + a.word
        self.assertEqual(exact_action(k + o.word + inverse_word(k), 5), exact_action(n.word, 5))
        self.assertNotEqual(exact_action(o.word, 5), exact_action(n.word, 5))

    def test_named_patterns_keep_all_inputs_and_every_internal_hurwitz_check(self):
        patterns = [s for s in self.route['stages'] if s['kind'] in ('disk_pc_rose', 'disk_pc_daisy')]
        self.assertEqual(len(patterns), 4)
        internal = []
        for s in patterns:
            w = s['named_pattern_witness']
            for match in w['individual_matches']:
                self.assertTrue(match['exact_disk_equal'])
                self.assertEqual(exact_action(match['actual'].word, 5), exact_action(match['pattern'].word, 5))
            previous = w.get('canonical')
            for move in w.get('retained_interchanges', ()):
                self.assertEqual(exact_action(product(previous), 5), exact_action(product(move['factors']), 5))
                previous = move['factors']
                internal.append(move)
            self.assertEqual(exact_action(product(s['local_before']), 5), exact_action(product(s['local_after']), 5))
            wanted = tuple(sum(f.power for f in s['local_before'] if i in enclosed_boundaries(f.mapping_class, 5)) - sum(f.power for f in s['local_after'] if i in enclosed_boundaries(f.mapping_class, 5)) for i in range(1, 6))
            self.assertEqual(s['framed_balance_before_minus_after'], wanted)
        self.assertEqual(len(internal), 13)  # rose1 + first daisy3 + second daisy9
        for s in patterns[-2:]:
            wrong = s['local_before'][:1] + tuple(reversed(s['local_before'][1:]))
            self.assertNotEqual(exact_action(product(wrong), 5), exact_action(product(s['local_after']), 5))

    def test_cyclic_starts_are_literal_conjugations_without_source_centrality(self):
        stages = self.route['stages']
        cycles = 0
        for i, s in enumerate(stages[1:], 1):
            if s['kind'] == 'disk_cyclic_start':
                g = s['frame']; cycles += 1
                self.assertEqual(reduce_word(g + product(stages[i - 1]['factors']) + inverse_word(g)), reduce_word(product(s['factors'])))
            if s['kind'] == 'global_conjugation':
                for a, b in zip(stages[i - 1]['factors'], s['factors']):
                    self.assertEqual(exact_action(s['frame'] + a.word + inverse_word(s['frame']), 5), exact_action(b.word, 5))
        self.assertEqual(cycles, 2)

    def test_four_exteriors_remain_visible_and_complete_join_includes_two_frame_eliminations(self):
        r = self.route
        self.assertEqual(r['factors'], tuple(Factor(f.id, (), 1, 5) for f in r['factors']))
        self.assertEqual(len(r['factors']), 4)
        self.assertEqual(r['sphere_move_count'], 0)
        self.assertEqual(r['exterior_caps'], 0)
        self.assertEqual(r['after_score'], dict(max_support_word=5, total_support_word=20, braid_letters=80))
        summary = self.saved['named_full_route']['summary']
        self.assertEqual(summary['unshortened_route_parts'], [17, 51, 8, 23, 1, 1])
        self.assertEqual((summary['graphical_steps'], summary['mathematical_steps_saved']), (90, 1))
        self.assertEqual((summary['sphere_moves'], summary['action_only_boundary_recognitions']), (4, 0))

    def test_public_disk_supports_and_source_validation(self):
        d = json.loads((self.folder / 'display-pure.json').read_text(encoding='utf-8'))
        shown = d['routes']['earlyaltclosed']
        self.assertEqual(len(shown), 24)
        for s, state in zip(self.route['stages'], shown):
            for f, i in zip(s['factors'], state['factors']):
                row = d['rows'][i]
                self.assertFalse(row['sphere_rechart'])
                self.assertEqual(exact_action(f.word, 5), exact_action(row['word'], 5))
        for wrong in (self.source[:-1], (replace(self.source[0], power=2),) + self.source[1:]):
            with self.assertRaises(ValueError): close_alternative_boundary(wrong)


if __name__ == '__main__': unittest.main()
