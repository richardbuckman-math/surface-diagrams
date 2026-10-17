"""Full braid and framing checks for non-composite boundary relations."""

import json
from pathlib import Path
import unittest

from surface_diagrams.double_boundary_catalog import canonical_blocks
from surface_diagrams.framed_boundary_relations import (
    enclosed_boundaries, five_boundary_lifts, five_boundary_mixed_lantern,
    five_boundary_mixed_lantern_states, five_boundary_type31_lantern,
    five_boundary_type28_lantern, five_boundary_type28_lantern_states,
    five_boundary_type21_lantern, five_boundary_type21_lantern_states,
    five_boundary_type31_lantern_states, five_boundary_type32_lantern,
    five_boundary_type32_lantern_states, four_triple_relations,
    framed_outer_certificate, short_inverse_lantern_matches,
)
from surface_diagrams.mapping_classes import ConjugatedTwist, exact_action
from surface_diagrams.projected_relations import pc_daisy_terms, pc_rose_terms


DATA = Path(__file__).resolve().parents[1] / 'docs' / 'boundary-factorizations' / 'data'


class FramedBoundaryRelationTests(unittest.TestCase):
    def test_lantern_and_daisy_calibrate_framing_convention(self):
        outer3 = ConjugatedTwist((), 1, 3)
        outer4 = ConjugatedTwist((), 1, 4)
        self.assertEqual(framed_outer_certificate(3, pc_rose_terms(outer3), 1),
                         (1, 1, 1))
        self.assertEqual(framed_outer_certificate(4, pc_daisy_terms(outer4), 1),
                         (1, 1, 1, 2))

    def test_seed_and_lantern_expansions_cover_all_three_open_n4_types(self):
        patterns = json.loads((DATA / '4-double.json').read_text(encoding='utf-8'))['patterns']
        actual = []
        for relation in four_triple_relations():
            factors = relation['factors']
            supports = tuple(enclosed_boundaries(factor, 4) for factor in factors)
            kind = canonical_blocks(4, supports)
            index = next(index for index, pattern in enumerate(patterns)
                         if kind == tuple(tuple(block) for block in pattern['blocks']))
            actual.append(index)
            self.assertEqual(tuple(relation['inner_powers']),
                             framed_outer_certificate(4, factors, 2))
        self.assertEqual(actual, [3, 4, 6])
        self.assertEqual([len(relation['factors']) for relation in four_triple_relations()],
                         [4, 6, 8])

    def test_published_direct_rows_replay_and_have_exact_support_images(self):
        root = DATA.parent
        patterns = json.loads((DATA / '4-double.json').read_text(encoding='utf-8'))['patterns']
        self.assertEqual([index for index, row in enumerate(patterns) if row.get('direct')],
                         [3, 4, 6])
        for row in patterns:
            direct = row.get('direct')
            if direct is None:
                continue
            factors = tuple(ConjugatedTwist(tuple(factor['conjugator']),
                                             factor['first'], factor['points'])
                            for factor in direct['factors'])
            self.assertEqual(list(framed_outer_certificate(4, factors, 2)),
                             direct['inner_powers'])
            self.assertEqual(canonical_blocks(4, [enclosed_boundaries(factor, 4)
                                                  for factor in factors]),
                             tuple(tuple(block) for block in row['blocks']))
            for factor, saved in zip(factors, direct['factors']):
                self.assertEqual(list(enclosed_boundaries(factor, 4)), saved['support'])
                picture = root / saved['svg']
                self.assertTrue(picture.is_file())
                self.assertIn('<svg ', picture.read_text(encoding='utf-8'))

    def test_every_local_lantern_expansion_preserves_exact_disk_braid(self):
        seed = four_triple_relations()[0]['factors']
        for factor in seed[2:]:
            replacement = pc_rose_terms(factor)
            word = tuple(letter for term in replacement for letter in term.word)
            self.assertEqual(exact_action(word, 4), exact_action(factor.word, 4))

    def test_five_boundary_daisy_lifts_certify_three_new_types(self):
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        outer5 = ConjugatedTwist((), 1, 5)
        prefix, *petals = pc_daisy_terms(outer5)
        petal_word = tuple(letter for factor in petals for letter in factor.word)
        self.assertEqual(framed_outer_certificate(5, (prefix, *petals), 1),
                         (1, 1, 1, 1, 3))
        self.assertEqual(exact_action(prefix.word + petal_word, 5),
                         exact_action(petal_word + prefix.word, 5))
        actual = []
        for relation in five_boundary_lifts():
            factors = relation['factors']
            core_length = relation['core_factor_count']
            self.assertEqual(tuple(factors[core_length:]), tuple(petals) * 2)
            self.assertEqual(tuple(relation['inner_powers']),
                             framed_outer_certificate(5, factors, 2))
            kind = canonical_blocks(5, [enclosed_boundaries(factor, 5)
                                        for factor in factors])
            index = next(index for index, pattern in enumerate(patterns)
                         if kind == tuple(tuple(block) for block in pattern['blocks']))
            self.assertIsNone(patterns[index]['composition'])
            actual.append(index)
        self.assertEqual(actual, [24, 29, 33])

    def test_published_five_boundary_lifts_replay_and_have_exact_images(self):
        root = DATA.parent
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        self.assertEqual([i for i, row in enumerate(patterns) if row.get('direct')],
                         [20, 24, 25, 27, 29, 30, 31, 33])
        for index in (20, 24, 25, 27, 29, 30, 31, 33):
            direct = patterns[index]['direct']
            factors = tuple(ConjugatedTwist(tuple(row['conjugator']),
                                             row['first'], row['points'])
                            for row in direct['factors'])
            self.assertEqual(list(framed_outer_certificate(5, factors, 2)),
                             direct['inner_powers'])
            if index in (20, 25, 27, 30, 31):
                self.assertEqual(direct['hurwitz_positions'],
                                 {20: [5, 6, 7, 8], 25: [4, 5, 6], 27: [6, 7, 9, 8],
                                  30: [6, 7, 8], 31: [5, 6, 7]}[index])
                self.assertEqual(direct['lantern_support'],
                                 {20: [2, 3, 5], 25: [2, 3, 5], 27: [2, 4, 5],
                                  30: [2, 3, 5], 31: [3, 4, 5]}[index])
            else:
                self.assertEqual(len(factors), direct['core_factor_count'] + 8)
            for factor, row in zip(factors, direct['factors']):
                self.assertEqual(list(enclosed_boundaries(factor, 5)), row['support'])
                self.assertTrue((root / row['svg']).is_file())

    def test_mixed_hurwitz_lantern_gives_new_five_boundary_type(self):
        source = five_boundary_lifts()[1]
        result = five_boundary_mixed_lantern()
        self.assertEqual(result['hurwitz_positions'], (4, 5, 6))
        self.assertEqual(result['inner_powers'], (3, 3, 3, 4, 5))
        self.assertEqual(len(result['factors']), 12)
        source_word = tuple(letter for factor in source['factors']
                            for letter in factor.word)
        result_word = tuple(letter for factor in result['factors']
                            for letter in factor.word)
        self.assertEqual(exact_action(source_word, 5), exact_action(result_word, 5))
        self.assertEqual(result['factors'][6], ConjugatedTwist((-4,), 2, 3))
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        kind = canonical_blocks(5, [enclosed_boundaries(factor, 5)
                                    for factor in result['factors']])
        self.assertEqual(kind, tuple(map(tuple, patterns[25]['blocks'])))
        self.assertIsNone(patterns[25]['composition'])

    def test_bounded_inverse_lantern_search_checks_full_action(self):
        marked = pc_rose_terms(ConjugatedTwist((), 1, 3))
        self.assertEqual(short_inverse_lantern_matches(marked, 3),
                         ((0, (1, 2, 3), ConjugatedTwist((), 1, 3)),))
        before_combining = five_boundary_mixed_lantern_states()[3]
        self.assertIn((6, (2, 3, 5), ConjugatedTwist((-4,), 2, 3)),
                      short_inverse_lantern_matches(before_combining, 5))

        # F8–F10 of the expanded lift contain precisely the three pairs
        # 34, 45, 35. Their route is not the three-hole lantern product.
        # Counting pairs alone would incorrectly claim a new relation.
        expanded = five_boundary_lifts()[2]['factors']
        self.assertEqual(set(enclosed_boundaries(factor, 5)
                             for factor in expanded[7:10]),
                         {(3, 4), (3, 5), (4, 5)})
        self.assertFalse(any(start == 7 for start, _, _ in
                             short_inverse_lantern_matches(expanded, 5, 4)))

    def test_type31_hurwitz_lantern_route_is_exact_and_framed(self):
        source = five_boundary_lifts()[2]['factors']
        states = five_boundary_type31_lantern_states()
        relation = five_boundary_type31_lantern()
        self.assertEqual([len(state) for state in states], [16, 16, 16, 16, 14])
        self.assertEqual(states[0], source)
        self.assertEqual(states[-1], relation['factors'])
        self.assertEqual(relation['hurwitz_positions'], (6, 7, 8))
        self.assertEqual(relation['inner_powers'], (4, 3, 4, 5, 5))
        action = exact_action(tuple(letter for factor in source
                                    for letter in factor.word), 5)
        for state in states:
            self.assertEqual(exact_action(tuple(letter for factor in state
                                                for letter in factor.word), 5), action)
            self.assertEqual(framed_outer_certificate(5, state, 2),
                             (4, 3, 4, 5, 5) if len(state) == 14 else
                             (4, 4, 5, 5, 6))
        matches = short_inverse_lantern_matches(states[-2], 5)
        self.assertIn((8, (2, 3, 5), ConjugatedTwist((-4,), 2, 3)), matches)
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        self.assertEqual(canonical_blocks(5, [enclosed_boundaries(factor, 5)
                                               for factor in relation['factors']]),
                         tuple(map(tuple, patterns[30]['blocks'])))

    def test_graphical_mixed_lantern_states_replay_exactly(self):
        stories = ((five_boundary_mixed_lantern_states(), 'mixed', 30, 26, 3),
                   (five_boundary_type31_lantern_states(), 'type31', 34, 31, 5),
                   (five_boundary_type32_lantern_states(), 'type32', 34, 32, None),
                   (five_boundary_type28_lantern_states(), 'type28', 32, 28, None),
                   (five_boundary_type21_lantern_states(), 'type21', 28, 21, 4))
        for states, slug, source, target, moving in stories:
            saved = json.loads((DATA / f'{slug}-lantern-states.json').read_text(
                encoding='utf-8'))
            self.assertEqual((saved['source_pattern'], saved['target_pattern']),
                             (source, target))
            if moving is not None:
                self.assertEqual(saved['moving_factor'], f'F{moving + 1}')
            self.assertEqual(len(saved['stages']), len(states))
            for index, (state, stage) in enumerate(zip(states, saved['stages'])):
                with self.subTest(target=target, stage=index):
                    self.assertEqual(list(framed_outer_certificate(5, state, 2)),
                                     stage['inner_powers'])
                    self.assertEqual(len(stage['rows']), len(state))
                    if index < len(states) - 1 and moving is not None:
                        self.assertEqual(stage['rows'][moving + index]['id'],
                                         saved['moving_factor'])
                        self.assertEqual(state[moving + index], states[0][moving])
                    for factor, row in zip(state, stage['rows']):
                        self.assertEqual((list(factor.conjugator), factor.first,
                                          factor.points),
                                         (row['conjugator'], row['first'], row['points']))
                        self.assertEqual(list(enclosed_boundaries(factor, 5)),
                                         row['support'])
                        self.assertTrue((DATA.parent / row['svg']).is_file())

    def test_type32_inverse_and_forward_hurwitz_moves_expose_lantern(self):
        states = five_boundary_type32_lantern_states()
        relation = five_boundary_type32_lantern()
        self.assertEqual(relation['hurwitz_directions'], (-1, 1, 1))
        self.assertEqual(relation['inner_powers'], (4, 4, 4, 4, 5))
        self.assertEqual(states[1][4], states[0][5])  # F6 dragged upward unchanged.
        self.assertEqual(states[2][6], states[1][5])  # Altered F5 dragged downward.
        self.assertEqual(states[3][7], states[2][6])
        action = exact_action(tuple(letter for factor in states[0]
                                    for letter in factor.word), 5)
        for state in states:
            self.assertEqual(exact_action(tuple(letter for factor in state
                                                for letter in factor.word), 5), action)
            self.assertEqual(framed_outer_certificate(5, state, 2),
                             (4, 4, 4, 4, 5) if len(state) == 14 else
                             (4, 4, 5, 5, 6))
        self.assertIn((7, (3, 4, 5), ConjugatedTwist((), 3, 3)),
                      short_inverse_lantern_matches(states[-2], 5))
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        self.assertEqual(canonical_blocks(5, [enclosed_boundaries(factor, 5)
                                               for factor in relation['factors']]),
                         tuple(map(tuple, patterns[31]['blocks'])))
        saved = json.loads((DATA / 'type32-lantern-states.json').read_text(encoding='utf-8'))
        self.assertEqual(saved['moves'][:3], ['F6 up past F5', 'F5 down past F7',
                                              'F5 down past F8'])
        self.assertEqual(saved['lantern_pair_supports'], [[3, 4], [4, 5], [3, 5]])

    def test_type28_reuses_type32_and_preserves_each_exact_move(self):
        states = five_boundary_type28_lantern_states()
        relation = five_boundary_type28_lantern()
        self.assertEqual(states[0], five_boundary_type32_lantern()['factors'])
        self.assertEqual([len(state) for state in states], [14] * 5 + [12])
        self.assertEqual(relation['inner_powers'], (4, 3, 4, 3, 4))
        action = exact_action(tuple(letter for factor in states[0]
                                    for letter in factor.word), 5)
        for state in states:
            self.assertEqual(exact_action(tuple(letter for factor in state
                                                for letter in factor.word), 5), action)
            self.assertEqual(framed_outer_certificate(5, state, 2),
                             (4, 3, 4, 3, 4) if len(state) == 12 else
                             (4, 4, 4, 4, 5))
        self.assertEqual(states[-1][8], ConjugatedTwist((1, 1, 2), 3, 3))
        saved = json.loads((DATA / 'type28-lantern-states.json').read_text(encoding='utf-8'))
        self.assertEqual(saved['moves'][:4], ['F7 up past F6', 'F8 up past F6',
                                              'F10 up past F9', 'F6 down past F10'])
        self.assertEqual(saved['lantern_pair_supports'], [[2, 4], [2, 5], [4, 5]])
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        self.assertEqual(canonical_blocks(5, [enclosed_boundaries(factor, 5)
                                               for factor in relation['factors']]),
                         tuple(map(tuple, patterns[27]['blocks'])))

    def test_type21_reuses_type28_and_replaces_the_exact_routed_lantern(self):
        states = five_boundary_type21_lantern_states()
        relation = five_boundary_type21_lantern()
        self.assertEqual(states[0], five_boundary_type28_lantern()['factors'])
        self.assertEqual([len(state) for state in states], [12] * 5 + [10])
        self.assertEqual(relation['inner_powers'], (4, 2, 3, 3, 3))
        action = exact_action(tuple(letter for factor in states[0]
                                    for letter in factor.word), 5)
        for state in states:
            self.assertEqual(exact_action(tuple(letter for factor in state
                                                for letter in factor.word), 5), action)
            self.assertEqual(framed_outer_certificate(5, state, 2),
                             (4, 2, 3, 3, 3) if len(state) == 10 else
                             (4, 3, 4, 3, 4))
        self.assertIn((8, (2, 3, 5), ConjugatedTwist((-4,), 2, 3)),
                      short_inverse_lantern_matches(states[-2], 5))
        patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
        self.assertEqual(canonical_blocks(5, [enclosed_boundaries(factor, 5)
                                               for factor in relation['factors']]),
                         tuple(map(tuple, patterns[20]['blocks'])))

    def test_wrong_factor_order_or_target_power_is_rejected(self):
        factors = four_triple_relations()[0]['factors']
        with self.assertRaisesRegex(ValueError, 'action'):
            framed_outer_certificate(4, (factors[1], factors[0], *factors[2:]), 2)
        with self.assertRaisesRegex(ValueError, 'Pair winding'):
            framed_outer_certificate(4, factors, 1)


if __name__ == '__main__':
    unittest.main()
