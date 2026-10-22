"""Replay checks for the shorter independent (6,7) boundary certificate."""
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import unittest

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import homology_action, IDENTITY
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.puncture_boundary import early_boundary_derivation
from surface_diagrams.sphere_actions import sphere_chain_certificate
from surface_diagrams.sphere_support_compact import half_endpoints


class EarlyBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.route=early_boundary_derivation()
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'

    def test_each_transition_and_every_sphere_step(self):
        r=self.route;stages=r['stages']
        self.assertEqual((len(stages),r['graphical_steps'],r['atomic_moves'],r['sphere_move_count']),(20,19,25,4))
        for before,after in zip(stages,stages[1:]):
            with self.subTest(title=after['title']):
                if after['kind']=='sphere_rewrite':
                    self.assertTrue(after['sphere_certificate']['certified'])
                    self.assertEqual(after['lift_homology'],IDENTITY)
                    self.assertTrue(after['disk_discrepancy'])
                    whole=reduce_word(product(before['factors'])+inverse_word(product(after['factors'])))
                    self.assertTrue(sphere_chain_certificate(whole)['certified'])
                    self.assertEqual(homology_action(whole),IDENTITY)
                elif after['kind']=='global_conjugation':
                    g=after['frame']
                    self.assertEqual(exact_action(product(after['factors'])),
                        exact_action(g+product(before['factors'])+inverse_word(g)))
                else:
                    self.assertEqual(exact_action(product(before['factors'])),
                                     exact_action(product(after['factors'])))
        self.assertEqual(len(r['atomic_stages']),26)
        block=next(s for s in stages if s['kind']=='disk_hurwitz_block')
        self.assertEqual((block['adjacent_moves'],len(block['atomic_steps'])),(7,7))
        self.assertFalse(stages[-1]['factors'])
        self.assertFalse(r['uses_source_identity_as_hypothesis'])
        self.assertFalse(r['complete_named_derivation'])

    def test_incident_halves_are_gone_before_exteriorization(self):
        stages=self.route['stages'];prefix=stages[-6]['factors']
        self.assertEqual(len(prefix),14)
        endpoints={p for f in prefix if f.half for p in half_endpoints(f.mapping_class)}
        self.assertNotIn(2,endpoints)
        self.assertEqual(self.route['fixed_point_in_working_chart'],2)
        self.assertEqual(self.route['chart']['normalized_boundary_power'],4)
        self.assertEqual(self.route['chart']['boundary_correction_power'],6)
        # The six corrections and their removal are different visible states.
        self.assertEqual(stages[-4]['factors'][0].power,6)
        self.assertNotIn('boundary.corrections',[f.id for f in stages[-3]['factors']])
        self.assertEqual(stages[-2]['factors'][0].power,4)

    def test_specific_next_lantern_is_exact_but_not_silently_applied(self):
        t=self.route['next_relations']
        self.assertFalse(t['applied_to_replay'])
        self.assertEqual(exact_action(product(t['local_before']),5),exact_action(product(t['local_after']),5))
        a=t['root_transport'];b=a['moving_root'];source=a['changed_root']
        self.assertEqual(exact_action(inverse_word(b.word)+source.word+b.word,5),exact_action(a['shortened_root'].word,5))
        self.assertEqual((a['before_support_length'],a['after_support_length']),(7,3))

    def test_saved_graphics_are_disk_exact_and_loaded_separately(self):
        saved=json.loads((self.folder/'certificate.json').read_text())
        self.assertEqual(saved['early_boundary'],json.loads(json.dumps(self.route,default=asdict)))
        base_bytes=(self.folder/'display.json').read_bytes()
        # This new phase must not increase the existing startup payload.
        self.assertEqual(len(base_bytes),943823)
        self.assertEqual(sha256(base_bytes).hexdigest()[:16],'05e6c888cf352a48')
        base=json.loads(base_bytes);early=json.loads((self.folder/'display-early.json').read_text())
        self.assertNotIn('early',base['routes'])
        self.assertEqual(len(early['routes']['early']),20)
        for actual,shown in zip(self.route['stages'],early['routes']['early']):
            for f,i in zip(actual['factors'],shown['factors']):
                row=early['rows'][i]
                self.assertFalse(row['sphere_rechart'])
                self.assertEqual(exact_action(f.word),exact_action(row['word']))
        joint=json.loads((self.folder/'early-sphere-cut-certificate.json').read_text())
        self.assertEqual((joint['points'],len(joint['arcs']),joint['boundary_power']),(6,5,4))
        self.assertTrue(joint['joint_verified']);self.assertFalse(joint['source_identity_assumed'])
        self.assertEqual(tuple(tuple(w) for w in joint['actual_disk_images_embedded'][:-1]),
                         self.route['chart']['normalized_disk_action'])


if __name__=='__main__': unittest.main()
