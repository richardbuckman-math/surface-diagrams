"""The positive exterior extraction, independently of the missing-C target."""
import json
from pathlib import Path
import unittest

from surface_diagrams.early_exterior_lantern import extract_positive_exterior, contract_exterior_petals, contract_transported_cluster, contract_second_exterior
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.disk_intersection import disk_curve_intersection
from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.hyperelliptic_homology import homology_action
from surface_diagrams.framed_boundary_relations import enclosed_boundaries


class EarlyExteriorLanternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks'
        saved = json.loads((cls.folder / 'certificate.json').read_text())
        cls.source = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator'])))
                           for f in saved['pure_cluster_contractions']['factors'])
        cls.route = extract_positive_exterior(cls.source)

    def test_every_operation_and_adjacent_check_is_positive_disk_exact(self):
        r = self.route
        self.assertEqual((r['graphical_steps'], r['adjacent_checks'], r['actual_peak_support_word']), (6, 11, 18))
        self.assertEqual(r['sphere_move_count'], 0)
        expected = exact_action(BOUNDARY_WORD * 4, 5)
        for stage in r['stages']:
            for state in (stage,) + stage.get('atomic_steps', ()):
                self.assertEqual(exact_action(product(state['factors']), 5), expected)
                self.assertTrue(all(not f.half and f.power > 0 for f in state['factors']))
                self.assertLessEqual(max(len(supported_class(f.mapping_class, 5)) for f in state['factors']), 18)
            if 'local_before' in stage:
                self.assertEqual(exact_action(product(stage['local_before']), 5),
                                 exact_action(product(stage['local_after']), 5))
        self.assertFalse(r['complete_named_derivation'])

    def test_one_unit_supplies_the_actual_lantern_in_its_checked_order(self):
        stages = self.route['stages']
        changed = next(f for f in stages[2]['factors'] if f.id == 'early.F13.1')
        self.assertEqual(exact_action(changed.word, 5), exact_action(self.route['matched_middle'].word, 5))
        shift = stages[3]['cyclic_shift']
        before = stages[2]['factors']
        self.assertEqual(stages[3]['factors'], before[shift:] + before[:shift])
        local = stages[-1]['local_before']
        self.assertEqual([f.id for f in local], ['early.F13.1', 'early.F12.1', 'pure.O1234'])
        self.assertNotEqual(exact_action(product(local), 5),
                            exact_action(product((local[1], local[0], local[2])), 5))

    def test_exterior_stays_visible_and_remaining_third_power_is_not_claimed_closed(self):
        r = self.route
        factors = r['factors']
        outside = [f for f in factors if f.points == 5]
        self.assertEqual(outside, [Factor('exterior.boundary', (), 1, 5)])
        rest = tuple(f for f in factors if f.id != 'exterior.boundary')
        self.assertEqual(exact_action(product(rest), 5), exact_action(BOUNDARY_WORD * 3, 5))
        self.assertTrue(r['exterior_not_capped'])
        self.assertTrue(r['exterior_twist_retained'])
        self.assertEqual(r['after_score'], dict(max_support_word=18, total_support_word=146, braid_letters=224))
        crossings = [disk_curve_intersection(a.mapping_class, b.mapping_class, strands=5)
                     for i, a in enumerate(factors) for b in factors[:i]]
        self.assertEqual((max(crossings), sum(crossings)), (38, 1412))
        public = json.loads((self.folder / 'display-pure.json').read_text())
        shown = public['routes']['earlyexterior']
        self.assertEqual(len(shown), 9)
        for actual, display in zip(r['stages'], shown):
            self.assertEqual(len(actual['factors']), len(display['factors']))
            for f, index in zip(actual['factors'], display['factors']):
                self.assertFalse(public['rows'][index]['sphere_rechart'])
                self.assertEqual(exact_action(f.word), exact_action(public['rows'][index]['word']))

    def test_residual_pc_lantern_is_reached_and_preserves_the_visible_exterior(self):
        r = contract_exterior_petals(self.route['factors'])
        self.assertEqual((r['graphical_steps'], r['adjacent_checks']), (2, 2))
        for s in r['stages']:
            for state in (s,) + s.get('atomic_steps', ()):
                self.assertEqual(exact_action(product(state['factors']), 5), exact_action(BOUNDARY_WORD * 4, 5))
                self.assertTrue(all(not f.half and f.power == 1 for f in state['factors']))
                self.assertLessEqual(max(len(supported_class(f.mapping_class, 5)) for f in state['factors']), 18)
        self.assertEqual([sum(f.points == k for f in r['factors']) for k in (2, 3, 5)], [12, 6, 1])
        rest = tuple(f for f in r['factors'] if f.points != 5)
        self.assertEqual(exact_action(product(rest), 5), exact_action(BOUNDARY_WORD * 3, 5))
        self.assertEqual(r['after_score'], dict(max_support_word=18, total_support_word=139, braid_letters=212))
        self.assertFalse(r['complete_named_derivation'])
        target = r['next_root_alignment']
        self.assertFalse(target['applied_to_replay'])
        self.assertTrue(target['requires_transport'])
        w = target['conjugating_word']
        self.assertEqual(exact_action(w + target['source'].word + inverse_word(w), 5),
                         exact_action(target['target'].word, 5))
        cluster = r['next_cluster_lantern']
        self.assertFalse(cluster['applied_to_replay'])
        self.assertTrue(cluster['requires_transport'])
        self.assertEqual(exact_action(product(cluster['local_before']), 5),
                         exact_action(product(cluster['local_after']), 5))
        a, b, required = cluster['local_before']
        actual = cluster['actual_petal']
        self.assertNotEqual(exact_action(required.word, 5), exact_action(actual.word, 5))
        self.assertEqual([disk_curve_intersection(f.mapping_class, actual.mapping_class, strands=5)
                          for f in (a, b)], [14, 10])
        self.assertEqual([disk_curve_intersection(f.mapping_class, required.mapping_class, strands=5)
                          for f in (a, b)], [2, 2])
        supplier = cluster['supplier'].word
        self.assertEqual(exact_action(supplier + actual.word + inverse_word(supplier), 5),
                         exact_action(required.word, 5))
        shown = json.loads((self.folder / 'display-pure.json').read_text())
        for actual, display in zip(r['stages'], shown['routes']['earlyexterior'][6:]):
            self.assertEqual(len(actual['factors']), len(display['factors']))
            for f, i in zip(actual['factors'], display['factors']):
                self.assertEqual(exact_action(f.word), exact_action(shown['rows'][i]['word']))


    def test_three_local_swaps_reach_the_next_actual_cluster_lantern(self):
        residual = contract_exterior_petals(self.route['factors'])
        r = contract_transported_cluster(residual['factors'])
        self.assertEqual((r['graphical_steps'], r['adjacent_checks'], r['sphere_move_count']), (6, 6, 0))
        expected = exact_action(BOUNDARY_WORD * 4, 5)
        for stage in r['stages']:
            for s in (stage,) + stage.get('atomic_steps', ()):
                self.assertEqual(exact_action(product(s['factors']), 5), expected)
                self.assertTrue(all(not f.half and f.power == 1 for f in s['factors']))
                self.assertLessEqual(max(len(supported_class(f.mapping_class, 5)) for f in s['factors']), 18)
        self.assertEqual([s.get('adjacent_moves') for s in r['stages'][1:4]], [1, 1, 1])
        target = residual['next_cluster_lantern']['local_before'][-1]
        self.assertEqual(exact_action(r['actual_required_petal'].word, 5), exact_action(target.word, 5))
        self.assertEqual(exact_action(product(r['stages'][4]['local_before']), 5),
                         exact_action(product(r['stages'][4]['local_after']), 5))
        self.assertEqual(r['after_score'], dict(max_support_word=14, total_support_word=117, braid_letters=184))
        self.assertEqual([sum(f.points == k for f in r['factors']) for k in (2, 3, 4, 5)], [12, 4, 1, 1])
        counts = [disk_curve_intersection(a.mapping_class, b.mapping_class, strands=5)
                  for i, a in enumerate(r['factors']) for b in r['factors'][:i]]
        self.assertEqual((max(counts), sum(counts)), (34, 774))
        self.assertFalse(r['complete_named_derivation'])
        self.assertTrue(r['exterior_not_capped'])
        public = json.loads((self.folder / 'display-pure.json').read_text())
        for actual, display in zip(r['stages'], public['routes']['earlysecond']):
            for f, j in zip(actual['factors'], display['factors']):
                self.assertEqual(exact_action(f.word), exact_action(public['rows'][j]['word']))
                self.assertFalse(public['rows'][j]['sphere_rechart'])



    def test_two_matched_lanterns_reach_a_second_exterior_in_five_operations(self):
        residual = contract_exterior_petals(self.route['factors'])
        source = contract_transported_cluster(residual['factors'])['factors']
        r = contract_second_exterior(source)
        self.assertEqual((r['graphical_steps'], r['adjacent_checks'], r['sphere_move_count']), (5, 4, 0))
        expected = exact_action(BOUNDARY_WORD * 4, 5)
        lift = homology_action(BOUNDARY_WORD * 4)
        for stage in r['stages']:
            for state in (stage,) + stage.get('atomic_steps', ()):
                self.assertEqual(exact_action(product(state['factors']), 5), expected)
                self.assertEqual(homology_action(product(state['factors'])), lift)
                self.assertTrue(all(not f.half and f.power == 1 for f in state['factors']))
                self.assertLessEqual(max(len(supported_class(f.mapping_class, 5)) for f in state['factors']), 14)
        self.assertEqual([sum(f.points == k for f in r['factors']) for k in (2, 3, 4, 5)], [11, 3, 0, 2])
        exteriors = tuple(f for f in r['factors'] if f.points == 5)
        self.assertEqual([f.id for f in exteriors], ['exterior.boundary', 'second.exterior'])
        rest = tuple(f for f in r['factors'] if f.points != 5)
        self.assertEqual(exact_action(product(rest), 5), exact_action(BOUNDARY_WORD * 2, 5))
        self.assertTrue(r['exterior_not_capped'])
        self.assertFalse(r['complete_named_derivation'])
        self.assertEqual(r['after_score'], dict(max_support_word=12, total_support_word=101, braid_letters=160))
        counts = [disk_curve_intersection(a.mapping_class, b.mapping_class, strands=5)
                  for i, a in enumerate(r['factors']) for b in r['factors'][:i]]
        self.assertEqual((max(counts), sum(counts)), (28, 440))
        public = json.loads((self.folder / 'display-pure.json').read_text())
        self.assertEqual(len(public['routes']['earlytwo']), 6)
        for actual, display in zip(r['stages'], public['routes']['earlytwo']):
            self.assertEqual(display['kind'], actual['kind'])
            for f, j in zip(actual['factors'], display['factors']):
                self.assertEqual(exact_action(f.word), exact_action(public['rows'][j]['word']))
                self.assertFalse(public['rows'][j]['sphere_rechart'])

    def test_cluster_order_and_framed_corrections_are_explicit(self):
        residual = contract_exterior_petals(self.route['factors'])
        source = contract_transported_cluster(residual['factors'])['factors']
        r = contract_second_exterior(source)
        for stage, correction in ((r['stages'][3], (0, 0, 1, 1, 0)),
                                  (r['stages'][5], (0, 1, 0, 0, 1))):
            before, after = stage['local_before'], stage['local_after']
            self.assertEqual(exact_action(product(before), 5), exact_action(product(after), 5))
            self.assertNotEqual(exact_action(product(before), 5),
                                exact_action(product((before[1], before[0], before[2])), 5))
            before_sets = [enclosed_boundaries(f.mapping_class, 5) for f in before]
            after_sets = [enclosed_boundaries(f.mapping_class, 5) for f in after]
            difference = tuple(sum(i in block for block in before_sets) -
                               sum(i in block for block in after_sets) for i in range(1, 6))
            self.assertEqual(difference, correction)
            self.assertEqual(stage['framed_inner_corrections'], correction)
        # The two gathers labeled as commutations really leave both classes fixed.
        for step in (2, 4):
            before = {f.id: exact_action(f.word, 5) for f in r['stages'][step - 1]['factors']}
            after = {f.id: exact_action(f.word, 5) for f in r['stages'][step]['factors']}
            self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
