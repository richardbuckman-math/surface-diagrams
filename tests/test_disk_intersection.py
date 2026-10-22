from dataclasses import replace
import json
from pathlib import Path
from random import Random
import unittest

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.disk_intersection import disk_curve_intersection, disk_intersection_certificate, _round_normal_form
from surface_diagrams.mapping_classes import ConjugatedTwist, VerificationLimitError, exact_action


class DiskIntersectionTests(unittest.TestCase):
    def test_standard_disjoint_nested_overlapping_and_peripheral_curves(self):
        t=lambda i,k:ConjugatedTwist((),i,k)
        for a,b,want in [(t(1,2),t(3,2),0),(t(1,3),t(2,2),0),
                          (t(1,2),t(2,2),2),(t(1,3),t(2,3),2),
                          (t(1,5),t(2,2),0),(t(2,2),t(2,2),0)]:
            self.assertEqual(disk_curve_intersection(a,b,strands=5),want)
            self.assertEqual(disk_curve_intersection(b,a,strands=5),want)
            self.assertEqual(disk_curve_intersection(replace(a,power=2),b,strands=5),want)

    def test_symmetry_and_independent_twist_commutation(self):
        rng=Random(42)
        for _ in range(300):
            def curve():
                points=rng.choice((2,3,4));first=rng.randrange(1,7-points)
                return ConjugatedTwist(tuple(rng.choice((-4,-3,-2,-1,1,2,3,4))
                    for _ in range(rng.randrange(7))),first,points)
            a,b=curve(),curve();number=disk_curve_intersection(a,b,strands=5)
            self.assertEqual(number,disk_curve_intersection(b,a,strands=5))
            self.assertEqual(number==0,exact_action(a.word+b.word,5)==exact_action(b.word+a.word,5))

    def test_exact_twist_growth_and_common_braid_invariance(self):
        rng=Random(63)
        for _ in range(45):
            def curve():
                return ConjugatedTwist(tuple(rng.choice((-3,-2,-1,1,2,3))
                    for _ in range(3)),rng.choice((1,2,3)),2)
            a,b=curve(),curve();number=disk_curve_intersection(a,b,strands=4)
            for power in (-1,1,2):
                word=a.word*power if power>0 else inverse_word(a.word)*(-power)
                moved=replace(b,conjugator=word+b.conjugator)
                self.assertEqual(disk_curve_intersection(moved,b,strands=4),abs(power)*number*number)
            frame=(2,-1,3)
            self.assertEqual(number,disk_curve_intersection(
                replace(a,conjugator=frame+a.conjugator),replace(b,conjugator=frame+b.conjugator),strands=4))

    def test_edge_words_cyclic_conjugation_and_outside_cancellation(self):
        z=(1,2);x=(3,)
        # Both vertex groups can reduce to their common boundary subgroup.
        words=(z+x+inverse_word(z)+inverse_word(x),
               x+z+inverse_word(x)+z,
               (1,3,2,-3,-1,-2),
               (3,1,2,-3,1,2,-1,-2))
        for w in words:
            count=len(_round_normal_form(w,1,2,4,1000))
            want=count if count>1 else 0
            for rotate in range(len(w)):
                actual=_round_normal_form(w[rotate:]+w[:rotate],1,2,4,1000)
                self.assertEqual(len(actual) if len(actual)>1 else 0,want)
            for g in ((1,2,3),(-4,1),(3,3)):
                actual=_round_normal_form(g+w+inverse_word(g),1,2,4,1000)
                self.assertEqual(len(actual) if len(actual)>1 else 0,want)

    def test_current_exterior_lantern_candidate_has_six_crossings_not_two(self):
        folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        rows=json.loads((folder/'certificate.json').read_text())['pure_cluster_contractions']['stages'][11]['factors']
        curves={f['id']:ConjugatedTwist(tuple(f['conjugator']),f['first'],f['points'],f['power'],f['half']) for f in rows}
        o,b,c=(curves[name] for name in ('pure.O1234','early.F13.1','early.F12.1'))
        self.assertEqual([disk_curve_intersection(a,b,strands=5) for a,b in ((o,b),(o,c),(b,c))],[6,2,2])
        changed=replace(b,conjugator=inverse_word(c.word)+b.conjugator)
        self.assertEqual(disk_curve_intersection(o,changed,strands=5),2)
        cert=disk_intersection_certificate(o,b,strands=5)
        self.assertEqual(len(cert['cyclic_normal_form']),6)
        self.assertTrue(cert['exact'])

    def test_saved_pure_matrices_and_diagram_complexity_scores(self):
        from examples.analyze_pure_intersections import pure_intersection_report
        report=pure_intersection_report()
        self.assertEqual([(report[k]['maximum'],report[k]['total']) for k in
            ('early_purification','pure_cluster_contractions')],[(48,1324),(36,1220)])
        self.assertEqual(report['before_square_unwind']['total'],2116)
        self.assertEqual(report['current_outer_candidate']['early.F13.1']['intersection_number'],2)
        self.assertFalse(report['next_exterior_lantern']['current_middle_already_matches'])
        self.assertEqual(report['outer_candidate']['actual_transport_support_peak'],30)
        folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        display=json.loads((folder/'display-pure.json').read_text())
        for phase,key in [('earlypure','early_purification'),('earlycontracts','pure_cluster_contractions')]:
            shown=display['routes'][phase][-1]['curve_intersections']
            self.assertEqual(shown,{k:report[key][k] for k in ('maximum','total','pairs')})

    def test_validation_and_bounds_never_claim_disjointness(self):
        a=ConjugatedTwist((),1,2);b=ConjugatedTwist((2,2,2),1,2)
        with self.assertRaises(VerificationLimitError):disk_curve_intersection(a,b,strands=4,max_letters=1)
        for args in (dict(strands=True),dict(strands=1),dict(max_letters=False),dict(max_letters=0)):
            with self.assertRaises(ValueError):disk_curve_intersection(a,b,**args)
        with self.assertRaises(ValueError):disk_curve_intersection(replace(a,half=True),b,strands=4)
        with self.assertRaises(ValueError):disk_curve_intersection(a,ConjugatedTwist((4,),1,2),strands=4)
        with self.assertRaises(ValueError):disk_curve_intersection(a,ConjugatedTwist((),3,3),strands=4)


if __name__=='__main__':unittest.main()
