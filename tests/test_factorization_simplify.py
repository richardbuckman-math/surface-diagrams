import unittest
import json
from pathlib import Path

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import Factor,initial_factors,product,parse_factors,checked_global_frame
from surface_diagrams.factorization_simplify import six_seven_simplification,replay_simplification,apply_simplification
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action,supported_class


class FactorizationSimplifyTests(unittest.TestCase):
    def test_checked_route_keeps_the_same_six_seven(self):
        route=six_seven_simplification();stages=route['stages']
        self.assertEqual(stages[0]['score'],(44,7,59,10))
        self.assertEqual(stages[-1]['score'],(32,6,46,6))
        self.assertEqual(len(stages),8)  # Also retains the initial disk presentation normalization.
        self.assertEqual(sum(s['kind']=='disk_hurwitz' for s in stages),3)
        self.assertEqual(sum(s['kind']=='global_conjugation' for s in stages),3)
        self.assertEqual(route['sphere_moves'],0)
        for stage in stages:
            fs=stage['factors']
            self.assertEqual(sum(f.half for f in fs),6)
            self.assertEqual(sum(not f.half and f.points==3 and f.power==2 for f in fs),7)
            for n in stage.get('disk_normalizations',[]):
                self.assertEqual(supported_class(n['before'].mapping_class),supported_class(n['after'].mapping_class))
        frame=route['frame'];expected=frame+product(initial_factors())+inverse_word(frame)
        self.assertEqual(exact_action(product(stages[-1]['factors'])),exact_action(expected))
        self.assertEqual(homology_action(product(stages[-1]['factors'])),IDENTITY)
        saved=json.loads((Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-compact/simplified-six-seven.json').read_text())
        restored=parse_factors(saved)
        self.assertEqual([f.word for f in restored],[f.word for f in stages[-1]['factors']])
        self.assertEqual(tuple(saved['global_conjugator']),frame)
        self.assertEqual(checked_global_frame(restored,frame),restored)

    def test_cyclic_neighbor_retains_the_rotation_and_the_local_disk_certificate(self):
        fs=initial_factors()
        for pair in ((11,12),(12,11)):
            r=apply_simplification(fs,'cyclic_hurwitz',(1,*pair))
            c=r['certificate'];g=c['frame']
            self.assertEqual(c['rotation']['factors'],fs[1:]+fs[:1])
            self.assertEqual(c['rotation']['word_certificate'],())
            self.assertEqual(c['hurwitz']['disk_word_certificate']['discrepancy'],())
            self.assertEqual(exact_action(product(r['factors'])),
                             exact_action(g+product(fs)+inverse_word(g)))

    def test_an_improving_circular_neighbor_has_a_replayable_global_frame(self):
        fs=(Factor('a',(),1,2,half=True),Factor('b',(),5,2,half=True),
            Factor('c',(1,),2,2,half=True))
        route=replay_simplification(fs,(('cyclic_hurwitz',(1,2,1)),))
        self.assertEqual(route['stages'][-1]['score'][0],0)
        self.assertEqual(route['frame'],(-1,))
        self.assertEqual(route['sphere_moves'],0)
        final=route['stages'][-1]['factors'];g=route['frame']
        self.assertEqual(exact_action(product(final)),exact_action(g+product(fs)+inverse_word(g)))

    def test_a_move_that_does_not_improve_or_changes_scope_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'does not improve'):
            replay_simplification(initial_factors(),(('global_conjugation',()),))
        with self.assertRaisesRegex(ValueError,'Only disk'):
            replay_simplification(initial_factors(),(('sphere_rewrite',()),))


if __name__=='__main__':unittest.main()
