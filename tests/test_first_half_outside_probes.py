from dataclasses import asdict
import json
import unittest
from pathlib import Path

from examples.analyze_first_half_outside_probes import report, equal
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.hyperelliptic_homology import IDENTITY


class FirstHalfOutsideProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = report()

    def test_fixed_frame_failure_has_individual_join_and_preserves_its_scope(self):
        f = self.r['frame_merge']
        self.assertEqual([s['peak'] for s in f['states']],[66,66,50,22,22,22])
        self.assertFalse(f['applied'])
        self.assertFalse(f['literal_join'])
        self.assertTrue(all(m['exact_disk_equal'] and equal(m['left'],m['right'])
                            for m in f['individual_join_matches']))

    def test_reached_two_operation_route_keeps_every_disk_state_and_both_halves(self):
        r = self.r['reached_outside_route']
        self.assertEqual((r['graphical_operations'],r['adjacent_checks']),(2,3))
        self.assertEqual(r['after_score'],dict(max_support_word=19,total_support_word=110,braid_letters=232))
        self.assertTrue(all(m['exact_disk_equal'] for m in r['original_half_matches']))
        states = [a for s in r['stages'] for a in (s,)+tuple(s.get('atomic_steps',()))]
        self.assertEqual(len(states),6)
        for state in states:
            fs = state['factors']
            self.assertEqual(len(fs),17)
            self.assertEqual(sum(f.half for f in fs),4)
            self.assertTrue(all(f.power>0 for f in fs))
            self.assertEqual(exact_action(product(fs),5),exact_action(BOUNDARY_WORD*4,5))
        for c in r['state_sphere_lift_certificates']:
            self.assertTrue(c['sphere_certificate']['certified'])
            self.assertEqual(c['chosen_lift'],IDENTITY)

    def test_wrong_donors_have_exact_positive_intersections_not_just_missing_chart_matches(self):
        audits = [self.r['reached_outside_route']['donor'],
                  self.r['rejected_opposite_route']['donor']]
        audits += [x['donor'] for x in self.r['hypothetical_unit_transports']]
        self.assertEqual([a['intersection_certificate']['intersection_number'] for a in audits],[4,8,8,8])
        for audit in audits:
            self.assertFalse(audit['commutes'])
            self.assertTrue(audit['intersection_certificate']['exact'])
            self.assertFalse(any(audit['canonical_petal_matches']['daisy']))
            self.assertFalse(any(audit['canonical_petal_matches']['rose']))
        rejected = self.r['rejected_opposite_route']
        self.assertEqual(rejected['completed_operations'],1)
        self.assertTrue(rejected['rejected_configuration']['not_a_reached_state'])
        self.assertEqual(rejected['rejected_configuration']['score']['max_support_word'],25)
        self.assertTrue(all(not x['applied'] and x['requires_transport']
                            for x in self.r['hypothetical_unit_transports']))

    def test_source_halves_keep_the_nonabelian_kernels_in_the_actual_outer_chart(self):
        splits = self.r['source_outer_chart_splits']
        self.assertEqual([x['split'].kernel_loop for x in splits],
                         [(-4,1,-3,4),(1,-4,-3,4),()])
        for x in splits:
            self.assertEqual(exact_action(x['factor'].word,5),
                             exact_action(x['split'].reconstructed_word,5))

    def test_saved_research_is_exact_and_claims_no_new_public_route(self):
        path = Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-first-half-outside-probes.json'
        self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),json.loads(path.read_text(encoding='utf-8')))
        for flag in ('public_graphical_payloads_changed','complete_shorter_derivation','half_lantern_applied'):
            self.assertFalse(self.r[flag])
        self.assertEqual(self.r['sphere_moves'],0)


if __name__=='__main__':
    unittest.main()
