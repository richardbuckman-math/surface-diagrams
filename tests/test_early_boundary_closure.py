"""The named boundary closure: actual PC patterns, not whole-product recognition."""
import json
from pathlib import Path
import unittest
from dataclasses import replace

from surface_diagrams.early_boundary_closure import close_round_boundary
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.hyperelliptic_homology import homology_action
from surface_diagrams.projected_relations import pc_rose_terms, pc_daisy_terms
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD


class EarlyBoundaryClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks'
        saved = json.loads((cls.folder / 'certificate.json').read_text())
        cls.source = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator'])))
                           for f in saved['round_four_point_reconstruction']['factors'])
        cls.route = close_round_boundary(cls.source)

    def test_every_local_move_and_explicit_frame_proves_the_replay(self):
        r = self.route
        expected, lift = exact_action(BOUNDARY_WORD * 4, 5), homology_action(BOUNDARY_WORD * 4)
        for i, stage in enumerate(r['stages']):
            for state in (stage,) + stage.get('atomic_steps', ()):
                self.assertTrue(all(not f.half and f.power == 1 for f in state['factors']))
                self.assertEqual(exact_action(product(state['factors']), 5), expected)
                self.assertEqual(homology_action(product(state['factors'])), lift)
                self.assertLessEqual(max(len(supported_class(f.mapping_class, 5)) for f in state['factors']), 14)
            if not i:
                continue
            before, after = product(r['stages'][i - 1]['factors']), product(stage['factors'])
            if stage['kind'] in ('global_conjugation', 'disk_cyclic_start'):
                frame = stage['frame']
                # This check does NOT assume before is central or an identity.
                self.assertEqual(exact_action(after, 5),
                                 exact_action(frame + before + inverse_word(frame), 5))
            else:
                self.assertEqual(exact_action(before, 5), exact_action(after, 5))
            if stage['kind'] in ('disk_pc_rose', 'disk_pc_daisy', 'disk_cluster_lantern'):
                a, b = stage['local_before'], stage['local_after']
                self.assertEqual(exact_action(product(a), 5), exact_action(product(b), 5))
                sets = [[enclosed_boundaries(f.mapping_class, 5) for f in fs] for fs in (a, b)]
                balance = tuple(sum(j in block for block in sets[0]) - sum(j in block for block in sets[1])
                                for j in range(1, 6))
                self.assertEqual(balance, stage['framed_balance_before_minus_after'])

    def test_four_point_rose_uses_actual_named_lantern_and_daisy(self):
        states = self.route['phases']['earlyrose']
        self.assertEqual([s['kind'] for s in states[1:]],
                         ['disk_cluster_lantern', 'disk_hurwitz_block', 'disk_pc_daisy'])
        generic = pc_rose_terms(Factor('root', (-3, -3, -1), 2, 3).mapping_class)
        for f, t in zip(states[1]['local_before'], (generic[2], generic[0], generic[1])):
            self.assertEqual(exact_action(f.word, 5), exact_action(t.word, 5))
        generic = tuple(replace(t, conjugator=(2, 3) + t.conjugator)
                        for t in pc_daisy_terms(Factor('outer', (), 1, 4).mapping_class))
        for f, t in zip(states[-1]['local_before'], generic):
            self.assertEqual(exact_action(f.word, 5), exact_action(t.word, 5))

    def test_eight_actual_petals_match_two_daisies_and_every_exterior_stays_visible(self):
        r = self.route
        self.assertEqual((r['graphical_steps'], r['adjacent_checks']), (18, 29))
        self.assertEqual(r['phase_operations'], dict(earlycollect=9, earlyrose=3, earlypetals=2, earlyclosed=4))
        self.assertEqual(r['petal_crossing_route'], ())
        self.assertEqual(r['bypassed_noncentral_petal_interchanges'], 21)
        self.assertEqual(r['graphical_steps_saved'], 15)
        self.assertTrue(r['boundary_closure_under_twenty'])
        self.assertEqual(len(r['canonical_petal_checks']), 8)
        for check in r['canonical_petal_checks']:
            self.assertTrue(check['exact_disk_equal'])
            self.assertEqual(exact_action(check['actual'].word, 5), exact_action(check['canonical'].word, 5))
        self.assertEqual(len(r['daisy_witnesses']), 2)
        for witness in r['daisy_witnesses']:
            generic = pc_daisy_terms(Factor('outer', witness['frame'], 1, 5).mapping_class)
            for actual, term in zip(witness['actual'], generic):
                self.assertEqual(exact_action(actual.word, 5), exact_action(term.word, 5))
            unframed = pc_daisy_terms(Factor('outer', (), 1, 5).mapping_class)
            self.assertFalse(all(exact_action(a.word, 5) == exact_action(b.word, 5)
                                 for a, b in zip(witness['actual'], unframed)))
            wrong = witness['actual'][:1] + tuple(reversed(witness['actual'][1:]))
            self.assertNotEqual(exact_action(product(wrong), 5), exact_action(Factor('outer', (), 1, 5).word, 5))
        tail = r['stages'][12:]
        self.assertEqual([s['kind'] for s in tail[1:]], ['disk_hurwitz_block', 'disk_pc_daisy',
            'disk_hurwitz_block', 'disk_hurwitz_block', 'disk_hurwitz_block', 'disk_pc_daisy'])
        # Only T1234 and central exteriors are dragged, never an individual petal.
        for stage in tail[1:]:
            for atomic in stage.get('atomic_steps', ()):
                dragged = atomic['local_before'][0 if atomic['source'] < atomic['target'] else 1]
                self.assertIn(dragged.points, (4, 5))
        self.assertEqual(len(r['factors']), 4)
        self.assertTrue(all(f.points == 5 and not f.conjugator for f in r['factors']))
        self.assertTrue(r['complete_named_boundary_derivation'])
        self.assertFalse(r['complete_under_twenty_derivation'])
        self.assertEqual(r['sphere_move_count'], 0)
        self.assertTrue(r['exterior_not_capped'])
        self.assertEqual(r['after_score'], dict(max_support_word=5, total_support_word=20, braid_letters=80))

    def test_public_graphical_states_keep_actual_disk_supports(self):
        shown = json.loads((self.folder / 'display-pure.json').read_text())
        for name, states in self.route['phases'].items():
            self.assertEqual(len(states), len(shown['routes'][name]))
            for actual, display in zip(states, shown['routes'][name]):
                self.assertEqual(display['kind'], actual['kind'])
                for f, j in zip(actual['factors'], display['factors']):
                    row = shown['rows'][j]
                    self.assertFalse(row['sphere_rechart'])
                    self.assertEqual(exact_action(f.word), exact_action(row['word']))
        self.assertEqual(len((self.folder / 'display.json').read_bytes()), 943823)



    def test_complete_named_route_retains_four_sphere_moves_without_action_recognition(self):
        saved = json.loads((self.folder / 'certificate.json').read_text())['named_full_route']
        summary, stages = saved['summary'], saved['stages']
        self.assertEqual(summary['graphical_steps'], 79)
        self.assertTrue(summary['complete_named_derivation'])
        self.assertFalse(summary['complete_under_twenty_derivation'])
        self.assertEqual(summary['action_only_boundary_recognitions'], 0)
        sphere = [s for s in stages if s['kind'] == 'sphere_rewrite']
        self.assertEqual(len(sphere), 4)
        for s in sphere:
            self.assertTrue(s['sphere_certificate']['certified'])
            self.assertTrue(s['disk_discrepancy'])
            self.assertEqual(homology_action(tuple(s['disk_discrepancy'])), homology_action(()))
        def word(records):
            return tuple(x for f in records for x in Factor(**{k: tuple(v) if k == 'conjugator' else v
                for k, v in f.items() if k != 'sign'}).word)
        for i, stage in enumerate(stages):
            if not i:
                continue
            before = stages[i - 1]['factors']
            if stage['kind'] == 'disk_cyclic_start':
                g = tuple(stage['frame'])
                rotated = stage.get('cyclic_before_disk_presentations', stage['factors'])
                self.assertEqual(reduce_word(g + word(before) + inverse_word(g)), reduce_word(word(rotated)))
                if 'cyclic_before_disk_presentations' in stage:
                    self.assertEqual([f['id'] for f in rotated], [f['id'] for f in stage['factors']])
                    self.assertEqual(len(stage['rejoin_individual_presentations']), len(rotated))
                    for a, b in zip(rotated, stage['factors']):
                        self.assertEqual(exact_action(word((a,)),5), exact_action(word((b,)),5))
            if stage['kind'] == 'global_conjugation':
                g = tuple(stage['frame'])
                for a, b in zip(before, stage['factors']):
                    self.assertEqual(a['id'], b['id'])
                    self.assertEqual(exact_action(word((b,))), exact_action(g + word((a,)) + inverse_word(g)))
        self.assertEqual(stages[-2]['kind'], 'disk_combine')
        self.assertEqual(stages[-2]['factors'][0]['power'], 4)
        self.assertEqual(stages[-1]['factors'], [])
        public = json.loads((self.folder / 'display-pure.json').read_text())['routes']['namedfull']
        self.assertEqual(len(public), 80)
        self.assertEqual(sum(s['kind'] == 'sphere_rewrite' for s in public), 4)
        self.assertFalse(any(s['kind'] == 'disk_boundary_relation' for s in public))


if __name__ == '__main__':
    unittest.main()
