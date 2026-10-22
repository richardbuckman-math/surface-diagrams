"""A specific squared-pair transport unwinds F9 without a sphere move."""
from collections import Counter
from dataclasses import replace
import json
from pathlib import Path
import unittest
from surface_diagrams.fifty_decomposition import unwind_f9_pair_square
from surface_diagrams.six_seven_structure import SignedResearchFactor
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.sphere_actions import sphere_chain_certificate

class F9UnwindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        cls.saved=json.loads((cls.folder/'certificate.json').read_text())
        cls.source=tuple(SignedResearchFactor(**dict(f,conjugator=tuple(f['conjugator'])))
                         for f in cls.saved['f6_alignment']['factors'])
        cls.route=unwind_f9_pair_square(cls.source)

    def test_each_move_preserves_the_disk_action_and_fixed_dragged_factor(self):
        expected=exact_action((1,2,3,4)*10,strands=5);r=self.route
        self.assertEqual(len(r['stages']),5)
        self.assertEqual(Counter(s['kind'] for s in r['stages'][1:]),{'disk_hurwitz':3,'disk_presentation':1})
        dragged=self.source[-1]
        for stage in r['stages']:
            self.assertEqual(exact_action(product(stage['factors']),strands=5),expected)
            self.assertLessEqual(max(len(supported_class(f.mapping_class,strands=5)) for f in stage['factors']),10)
            self.assertEqual(next(f for f in stage['factors'] if f.id==dragged.id),dragged)
            if stage['kind']=='disk_hurwitz':
                discrepancy=reduce_word(product(stage['local_before'])+inverse_word(product(stage['local_after'])))
                self.assertEqual(discrepancy,())
                self.assertTrue(sphere_chain_certificate(discrepancy)['certified'])
                self.assertEqual(homology_action(discrepancy),IDENTITY)
        self.assertEqual(r['sphere_move_count'],0)

    def test_only_f9_support_changes_and_all_positive_types_survive(self):
        r=self.route;old={f.id:f for f in self.source};new={f.id:f for f in r['factors']}
        for identity in old:
            if identity!='F9':self.assertEqual(exact_action(old[identity].word,strands=5),exact_action(new[identity].word,strands=5))
        self.assertEqual(r['before_score'],dict(max_support_word=10,total_support_word=58,braid_letters=84))
        self.assertEqual(r['after_score'],dict(max_support_word=8,total_support_word=52,braid_letters=80))
        self.assertEqual(r['f9_support_lengths'],(10,4))
        self.assertEqual((new['F9'].conjugator,new['F9'].first),((-4,1,2,-3),2))
        self.assertEqual(Counter((f.points,f.power,f.half,f.sign) for f in r['factors']),
                         Counter((f.points,f.power,f.half,f.sign) for f in self.source))
        self.assertTrue(r['aligned_target_preserved'])
        self.assertFalse(r['is_shorter_identity_proof'])

    def test_saved_replay_is_exactly_the_checked_extension(self):
        r=self.route
        self.assertEqual(json.loads(json.dumps(r,default=lambda f:f.__dict__)),self.saved['f9_unwinding'])
        d=json.loads((self.folder/'display.json').read_text())
        self.assertEqual(len(d['routes']['transport']),28)
        for stage,shown in zip(r['stages'][1:],d['routes']['transport'][22:]):
            for factor,index in zip(stage['factors'],shown['factors']):
                row=d['rows'][index]
                self.assertFalse(row['sphere_rechart'])
                self.assertEqual(exact_action(row['word'],strands=5),exact_action(factor.word,strands=5))
        for bad in (self.source[:-1],(replace(self.source[0],sign=-1),)+self.source[1:],
                    self.source[:-1]+(replace(self.source[-1],power=1),)):
            with self.assertRaises(ValueError):unwind_f9_pair_square(bad)

if __name__=='__main__':unittest.main()
