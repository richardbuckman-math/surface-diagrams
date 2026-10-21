"""Closed finite orbits certify exclusions; allowed residues stay inconclusive."""
import json
from pathlib import Path
import unittest

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.homology_orbits import modular_homology_orbit, modular_pairing_obstruction
from surface_diagrams.hyperelliptic_homology import half_twist_class, homology_action
from surface_diagrams.mapping_classes import VerificationLimitError, exact_action
from surface_diagrams.factorization_explorer import product
from surface_diagrams.six_seven_structure import SignedResearchFactor, research_hurwitz_move


class HomologyOrbitTests(unittest.TestCase):
    def test_complete_closure_includes_inverse_generators_and_generator_iterators(self):
        v = (1, 0, 0, 0)
        orbit = modular_homology_orbit(v, iter(((2,),)), 5)
        self.assertEqual(len(orbit), 5)
        self.assertEqual(orbit, modular_homology_orbit(v, ((-2,),), 5))
        self.assertEqual(modular_homology_orbit(v, (), 5), (v,))
        self.assertEqual(modular_homology_orbit((-1, 0, 0, 0), (), 5), ((4, 0, 0, 0),))

    def test_bound_returns_unknown_by_exception_and_rejects_invalid_inputs(self):
        with self.assertRaises(VerificationLimitError):
            modular_homology_orbit((1, 0, 0, 0), ((2,),), 5, max_states=4)
        for v, words, modulus, cap in (((1, 2, 3), (), 4, 4),
                ((True, 0, 0, 0), (), 4, 4), ((1, 0, 0, 0), ((6,),), 4, 4),
                ((1, 0, 0, 0), (), True, 4), ((1, 0, 0, 0), (), 1, 4),
                ((1, 0, 0, 0), (), 4, 0)):
            with self.assertRaises(ValueError):
                modular_homology_orbit(v, words, modulus, cap)

    def test_orientation_and_real_half_lantern_are_not_falsely_excluded(self):
        left, right = half_twist_class((), 3), half_twist_class((2, 2), 3)
        words = ((3,), (2, 2, 3, -2, -2), (2,)*4)
        for sign in (1, -1):
            r = modular_pairing_obstruction(left, tuple(sign*x for x in right), words, modulus=5)
            self.assertFalse(r['obstructed'])
            self.assertFalse(r['positive_result_proves_equivalence'])
            self.assertEqual(r['target_residues'], (2, 3))
        r = modular_pairing_obstruction((1, 0, 0, 0), (0, 0, 1, 0), (), 2)
        self.assertTrue(r['obstructed'])
        with self.assertRaises(ValueError):
            modular_pairing_obstruction(left, right, words, -1)

    def test_compact_tail_exclusion_and_unresolved_alternative(self):
        path = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-tail-obstruction.json'
        d = json.loads(path.read_text())
        published = json.loads((path.parent / 'six-seven-fifty-blocks/certificate.json').read_text())
        self.assertEqual(d['source_tail'], published['compact_boundary_chart']['factors'][9:])
        fs = tuple(SignedResearchFactor(**dict(f, conjugator=tuple(f['conjugator']))) for f in d['source_tail'])
        def check(i, j, stored):
            a, b = fs[i], fs[j]
            r = modular_pairing_obstruction(half_twist_class(a.conjugator, a.first),
                half_twist_class(b.conjugator, b.first), (f.word for f in fs))
            self.assertEqual(json.loads(json.dumps(r)), {k:stored[k] for k in r})
            return r
        a = check(0, 3, d['f3_f9'])
        self.assertTrue(a['obstructed'])
        self.assertEqual((len(a['left_orbit']), len(a['right_orbit'])), (2, 2))
        self.assertEqual(a['pairing_residues'], (0,))
        b = check(1, 4, d['f6_f11'])
        self.assertFalse(b['obstructed'])
        self.assertEqual((len(b['left_orbit']), len(b['right_orbit'])), (4, 8))
        self.assertEqual(b['pairing_residues'], (0, 2))
        # Explicit Hurwitz transports stay inside the original group orbit.
        for source, target in ((0, 1), (1, 2), (3, 2), (4, 3), (5, 4), (2, 3)):
            fs = research_hurwitz_move(fs, source, target)['factors']
            by_id = {f.id:f for f in fs}
            for name, orbit in (('F3', a['left_orbit']), ('F9', a['right_orbit'])):
                f = by_id[name]
                v = tuple(x % 4 for x in half_twist_class(f.conjugator, f.first))
                self.assertIn(v, orbit)
        # The allowed alternative has an exact local target, but not a route.
        target = d['local_target']
        mk = lambda f: SignedResearchFactor(**dict(f, conjugator=tuple(f['conjugator'])))
        self.assertEqual(exact_action(product(tuple(mk(f) for f in target['before'])), strands=5),
                         exact_action(product(tuple(mk(f) for f in target['after'])), strands=5))
        self.assertFalse(target['route_found'])
        self.assertFalse(target['f6_already_matches'])
        self.assertFalse(target['applied_to_replay'])

    def test_global_symplectic_frame_preserves_obstruction(self):
        words = ((1, 1), (3, 3))
        v, w = half_twist_class((), 1), half_twist_class((), 3)
        original = modular_pairing_obstruction(v, w, words)
        frame = (2, 3, -4, 1)
        m = homology_action(frame)
        transform = lambda v: tuple(sum(m[i][j]*v[j] for j in range(4)) for i in range(4))
        moved = modular_pairing_obstruction(transform(v), transform(w),
            (frame + word + inverse_word(frame) for word in words))
        self.assertTrue(original['obstructed'])
        self.assertEqual(moved['pairing_residues'], original['pairing_residues'])
        self.assertEqual(moved['obstructed'], original['obstructed'])


if __name__ == '__main__':
    unittest.main()
