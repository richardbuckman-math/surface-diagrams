import json
from pathlib import Path
from random import Random
import unittest

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.mapping_classes import exact_action, VerificationLimitError
from surface_diagrams.point_pushing import (point_push_generator, point_push_braid,
    split_fixed_last_strand, common_shadow_obstruction)


class PointPushingTests(unittest.TestCase):
    def test_every_signed_schreier_edge_is_an_exact_disk_equality(self):
        for n in range(2, 8):
            for j in range(1, n + 1):
                r = tuple(range(1 - n, -j + 1))
                for i in range(1, n):
                    for sign in (-1, 1):
                        end = i + 1 if j == i else i if j == i + 1 else j
                        back = tuple(range(1 - n, -end + 1))
                        word = r + (sign * i,) + inverse_word(back)
                        split = split_fixed_last_strand(word, n)
                        self.assertEqual(exact_action(word, n), exact_action(split.reconstructed_word, n))

    def test_random_pure_and_mixed_shadow_reconstruction(self):
        rng = Random(273)
        for n in range(2, 7):
            choices = tuple(range(1, n)) + tuple(range(1 - n, 0))
            for _ in range(40):
                frame = tuple(rng.choice(choices) for _ in range(5))
                word = frame + (rng.randrange(1, n),) * 2 + inverse_word(frame)
                word += tuple(rng.choice(tuple(range(1, n - 1))) for _ in range(3)) if n > 2 else ()
                split = split_fixed_last_strand(word, n)
                self.assertEqual(exact_action(word, n), exact_action(split.reconstructed_word, n))
                self.assertFalse(any(abs(a) == n - 1 for a in split.shadow_word))

    def test_point_push_basis_orientation_and_anti_multiplication(self):
        for n in range(2, 7):
            for i in range(1, n):
                s = split_fixed_last_strand(point_push_generator(n, i), n)
                self.assertEqual(s.kernel_loop, (i,))
                self.assertEqual(s.shadow_word, ())
        a, b = (1, -3, 2), (4, 1, -2)
        self.assertEqual(point_push_braid(a + b, 5),
                         reduce_word(point_push_braid(b, 5) + point_push_braid(a, 5)))
        kernel = point_push_braid(a, 5)
        shadow = (2, -1, 3, 2)
        s = split_fixed_last_strand(kernel + shadow, 5)
        self.assertEqual(s.kernel_loop, a)
        self.assertEqual(s.shadow_word, shadow)

    def test_deletion_never_drops_the_point_pushing_kernel(self):
        p = point_push_generator(5, 2)
        s = split_fixed_last_strand(p, 5)
        self.assertEqual(s.shadow_word, ())
        self.assertNotEqual(exact_action(p, 5), exact_action((), 5))
        self.assertEqual(s.kernel_loop, (2,))
        boundary = Factor('outer', (), 1, 5, power=4)
        s = split_fixed_last_strand(boundary.word, 5)
        self.assertEqual(s.kernel_loop, (1, 2, 3, 4) * 4)
        self.assertEqual(exact_action(s.shadow_word, 4), exact_action(Factor('inner', (), 1, 4, power=4).word, 4))

    def test_common_frame_test_returns_an_actual_inconsistent_cycle(self):
        folder = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks'
        factors = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator']))) for f in
                        json.loads((folder / 'certificate.json').read_text())['early_boundary']['chart']['factors'])
        halves = tuple(f for f in factors if f.half)
        splits = tuple(split_fixed_last_strand(f.word, 5) for f in halves)
        result = common_shadow_obstruction(splits)
        self.assertEqual(result['status'], 'obstructed')
        self.assertNotEqual(result['cycle_sum'], 0)
        cycle = result['cycle']
        self.assertTrue(all(a['end'] == b['start'] for a, b in zip(cycle, cycle[1:] + cycle[:1])))
        self.assertEqual({halves[e['source']].id for e in cycle}, {'F3', 'F9'})
        # The other pair independently obstructs a single common frame.
        self.assertEqual(common_shadow_obstruction((splits[1], splits[3]))['status'], 'obstructed')
        total = split_fixed_last_strand(product(factors), 5)
        self.assertEqual(total.kernel_loop, (1, 2, 3, 4) * 4)
        self.assertEqual(exact_action(total.reconstructed_word, 5), exact_action(product(factors), 5))

    def test_consistency_is_unknown_and_survives_known_common_frames(self):
        rng = Random(4)
        for _ in range(30):
            loop = tuple(rng.choice((-4, -3, -2, -1, 1, 2, 3, 4)) for _ in range(4))
            frame = point_push_braid(loop, 5) + (1, -3, 2)
            words = tuple(inverse_word(frame) + (i,) + frame for i in (1, 2, 3))
            result = common_shadow_obstruction(tuple(split_fixed_last_strand(w, 5) for w in words))
            self.assertEqual(result['status'], 'inconclusive')
            self.assertFalse(result['common_conjugation_excluded'])
        self.assertEqual(common_shadow_obstruction((split_fixed_last_strand((), 5),))['status'], 'inconclusive')

    def test_saved_report_reproduces_the_actual_kernel_and_scoped_obstruction(self):
        from examples.analyze_early_point_pushing import early_point_pushing_report
        path = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-point-pushing.json'
        report = early_point_pushing_report()
        self.assertEqual(json.loads(json.dumps(report)), json.loads(path.read_text()))
        self.assertFalse(report['graphical_proof_changed'])
        self.assertEqual(report['graphical_step_count'], 106)
        self.assertFalse(report['complete_under_twenty_derivation'])

    def test_validation_and_exhaustion_never_return_partial_certificates(self):
        for n, word in ((True, ()), (1, ()), (4, (True,)), (4, (0,)), (4, (4,)), (5, (4,))):
            with self.assertRaises(ValueError): split_fixed_last_strand(word, n)
        for kwargs in (dict(max_letters=False), dict(max_letters=0), dict(max_work=True), dict(max_work=0)):
            with self.assertRaises(ValueError): split_fixed_last_strand((), 5, **kwargs)
        for kwargs in (dict(max_letters=3), dict(max_work=3)):
            with self.assertRaises(VerificationLimitError): split_fixed_last_strand((4, 4), 5, **kwargs)
        with self.assertRaises(VerificationLimitError):
            split_fixed_last_strand((1, 2, 3, 4) * 5, 5, max_work=100)
        with self.assertRaises(ValueError): common_shadow_obstruction(())
        with self.assertRaises(ValueError): common_shadow_obstruction((split_fixed_last_strand((), 4), split_fixed_last_strand((), 5)))


if __name__ == '__main__':
    unittest.main()
