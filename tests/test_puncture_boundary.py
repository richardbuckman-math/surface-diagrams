"""Independent algebra and framing checks for the fixed-puncture chart."""
from dataclasses import replace
import json
from pathlib import Path
import unittest

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.puncture_boundary import (
    BOUNDARY_WORD, FOUR_POINT_WORD, fixed_puncture_word,
    puncture_chart_generators, puncture_to_boundary,
)
from surface_diagrams.six_seven_structure import SignedResearchFactor


class PunctureBoundaryTests(unittest.TestCase):
    def test_every_schreier_edge_retains_sphere_and_lift_certificate(self):
        records = puncture_chart_generators()
        self.assertEqual(len(records), 30)
        self.assertEqual(sum(not r['disk_equal'] for r in records), 5)
        for r in records:
            self.assertTrue(r['sphere_certificate']['certified'])
            self.assertEqual(r['lift_homology'], IDENTITY)
            if not r['disk_equal']:
                self.assertTrue(r['disk_discrepancy'])
                self.assertNotEqual(exact_action(r['before']), exact_action(r['after']))
        self.assertEqual(fixed_puncture_word((5, 5))['word'], FOUR_POINT_WORD)

    def test_mixed_braid_relations_and_homomorphism(self):
        # The nontrivial type-B relation, plus its commuting generators,
        # independently checks the image assigned to the exterior strand loop.
        t = (5, 5)
        left, right = t + (4,) + t + (4,), (4,) + t + (4,) + t
        self.assertEqual(exact_action(left), exact_action(right))
        a = fixed_puncture_word(left)['word']; b = fixed_puncture_word(right)['word']
        self.assertEqual(exact_action(a, 5), exact_action(b, 5))
        for i in (1, 2, 3):
            self.assertEqual(exact_action(FOUR_POINT_WORD + (i,), 5),
                             exact_action((i,) + FOUR_POINT_WORD, 5))
        u = (3, -2, 5, 5, 2, -3)
        v = (-4, 5, 5, 4, 1, 2, -1)
        f = lambda w: fixed_puncture_word(w)['word']
        self.assertEqual(exact_action(f(u + v), 5), exact_action(f(u) + f(v), 5))
        self.assertEqual(exact_action(f(inverse_word(u)), 5), exact_action(inverse_word(f(u)), 5))
        for invalid in ((5,), (6,), (True,), ('1',)):
            with self.assertRaises(ValueError): fixed_puncture_word(invalid)

    def test_complement_formula_including_odd_root_deck_sign(self):
        for size in (2, 3, 4, 5, 6):
            factor = Factor('T', (), 7-size, size)
            r = puncture_to_boundary((factor,))
            self.assertEqual(r['boundary_correction_power'], size-2)
            self.assertEqual(r['joint_rechart_preserves_lift'], size % 2 == 0)
            c = r['factor_certificates'][0]
            self.assertTrue(c['disk_framing_equal'])
            if size <= 4: self.assertEqual(r['factors'][0].points, 6-size)
            else: self.assertFalse(r['factors'])
        inverse = SignedResearchFactor('inverse', (), 4, 3, sign=-1)
        r = puncture_to_boundary((inverse,))
        self.assertEqual(r['boundary_correction_power'], -1)
        self.assertEqual(r['factors'][0].sign, -1)
        even_half = Factor('sigma5 squared', (), 5, 2, power=2, half=True)
        r = puncture_to_boundary((even_half,))
        self.assertEqual((r['factors'][0].points,r['factors'][0].half),(4,False))
        self.assertEqual(exact_action(product(r['factors']),5),exact_action(FOUR_POINT_WORD,5))
        with self.assertRaisesRegex(ValueError, 'odd half twist'):
            puncture_to_boundary((replace(even_half,power=1),))

    def test_every_interval_and_puncture_position_uses_exact_framing(self):
        for first in range(1,6):
            for size in range(2,8-first):
                for puncture_position in range(1,7):
                    with self.subTest(first=first,size=size,position=puncture_position):
                        r=tuple(range(5,puncture_position-1,-1))
                        result=puncture_to_boundary((Factor('T',r,first,size),),simplify=False)
                        self.assertTrue(result['factor_certificates'][0]['disk_framing_equal'])

    def test_disk_chart_does_not_assume_source_identity(self):
        r = puncture_to_boundary((Factor('H12',(),1,2,half=True),))
        self.assertIsNone(r['normalized_boundary_power'])
        self.assertFalse(r['normalized_boundary_action_verified'])
        with self.assertRaises(ValueError): puncture_to_boundary(())
        with self.assertRaises(ValueError): fixed_puncture_word((),marked_point=True)

    def test_early_fourth_boundary_relation_and_its_framing(self):
        path = Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-compact/source-route.json'
        saved = json.loads(path.read_text())
        factors = tuple(SignedResearchFactor(**dict(f,conjugator=tuple(f['conjugator'])))
                        for f in saved['prefix_lantern']['stages'][-1]['factors'])
        r = puncture_to_boundary(factors,marked_point=3)
        self.assertEqual(len(r['factors']),14)
        self.assertEqual(r['normalized_boundary_power'],4)
        self.assertEqual(r['boundary_correction_power'],6)
        self.assertEqual(r['framed_boundary_power'],10)
        self.assertEqual(r['global_frame'],(5,4,3))
        self.assertTrue(r['joint_rechart_preserves_lift'])
        self.assertEqual(r['joint_lift_homology'],IDENTITY)
        self.assertEqual(r['normalized_disk_action'],exact_action(BOUNDARY_WORD*4,5))
        self.assertEqual(r['score'],dict(max_support_word=16,total_support_word=114,braid_letters=210))
        actual = fixed_puncture_word(product(factors),marked_point=3)['word']
        self.assertEqual(exact_action(actual,5),exact_action(BOUNDARY_WORD*10,5))
        self.assertFalse(r['complete_named_derivation'])
        self.assertEqual(sum(not c['is_individual_lift_equality'] for c in r['factor_certificates']),2)


if __name__ == '__main__': unittest.main()
