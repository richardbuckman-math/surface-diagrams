"""One explicit squared-pair transport rounds F11 and reorders its target."""
from collections import Counter
from dataclasses import replace
import json
from pathlib import Path
import unittest
from surface_diagrams.fifty_decomposition import round_f11_half_twist
from surface_diagrams.six_seven_structure import SignedResearchFactor
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.sphere_actions import sphere_chain_certificate

class F11RoundingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        cls.saved=json.loads((cls.folder/'certificate.json').read_text())
        cls.source=tuple(SignedResearchFactor(**dict(f,conjugator=tuple(f['conjugator']))) for f in cls.saved['f9_unwinding']['factors'])
        cls.route=round_f11_half_twist(cls.source)

    def test_disk_transport_and_round_presentation_preserve_the_boundary(self):
        r=self.route;expected=exact_action((1,2,3,4)*10,strands=5)
        self.assertEqual([s['kind'] for s in r['stages']],['start','disk_hurwitz','disk_presentation'])
        for stage in r['stages']:
            self.assertEqual(exact_action(product(stage['factors']),strands=5),expected)
            self.assertLessEqual(max(len(supported_class(f.mapping_class,strands=5)) for f in stage['factors']),8)
            if stage['kind']!='start':
                discrepancy=reduce_word(product(stage['local_before'])+inverse_word(product(stage['local_after'])))
                self.assertEqual(homology_action(discrepancy),IDENTITY)
                self.assertTrue(sphere_chain_certificate(discrepancy)['certified'])
        self.assertEqual(r['stages'][1]['factors'][14],self.source[15])
        f=r['factors'][-1]
        self.assertEqual((f.id,f.conjugator,f.first,f.half),('F11',(),1,True))
        self.assertEqual(r['before_score'],dict(max_support_word=8,total_support_word=52,braid_letters=80))
        self.assertEqual(r['after_score'],dict(max_support_word=6,total_support_word=46,braid_letters=72))
        self.assertEqual(r['f11_support_lengths'],(8,2))
        self.assertEqual(r['sphere_move_count'],0)

    def test_only_f11_changes_and_target_order_is_explicit(self):
        r=self.route;old={f.id:f for f in self.source};new={f.id:f for f in r['factors']}
        for identity in old:
            if identity!='F11':self.assertEqual(exact_action(old[identity].word,strands=5),exact_action(new[identity].word,strands=5))
        self.assertEqual(Counter((f.points,f.power,f.half,f.sign) for f in self.source),Counter((f.points,f.power,f.half,f.sign) for f in r['factors']))
        target=r['reordered_target']
        self.assertEqual(target['order'],('F6','last.P12.square','F11'))
        self.assertEqual(exact_action(product(target['local_before']),strands=5),exact_action(product(target['local_after']),strands=5))
        self.assertTrue(target['requires_gathering']);self.assertFalse(target['applied_to_replay'])
        self.assertNotEqual(exact_action(product((new['F6'],new['F11'],new['last.P12.square'])),strands=5),exact_action(product(target['local_after']),strands=5))

    def test_focused_petal_frame_is_exact_but_not_adopted(self):
        target=self.route['next_petal_target']
        self.assertEqual(target['frame'],(-2,-1))
        self.assertEqual(target['framed_score'],dict(max_support_word=8,total_support_word=54,braid_letters=70))
        self.assertEqual(exact_action(target['f9_after'].word*2,strands=5),exact_action(target['daisy_petal'].word,strands=5))
        self.assertTrue(target['curve_unchanged'])
        self.assertFalse(target['applied_to_replay'])
        self.assertTrue(target['requires_further_benefit'])

    def test_published_extension_and_wrong_sources(self):
        r=self.route
        self.assertEqual(json.loads(json.dumps(r,default=lambda f:f.__dict__)),self.saved['f11_rounding'])
        d=json.loads((self.folder/'display.json').read_text());self.assertEqual(len(d['routes']['transport']),28)
        for stage,shown in zip(r['stages'][1:],d['routes']['transport'][26:]):
            for f,index in zip(stage['factors'],shown['factors']):
                self.assertFalse(d['rows'][index]['sphere_rechart'])
                self.assertEqual(exact_action(f.word,strands=5),exact_action(d['rows'][index]['word'],strands=5))
        for bad in (self.source[:-1],(replace(self.source[0],sign=-1),)+self.source[1:],self.source[:-2]+(self.source[-1],self.source[-2])):
            with self.assertRaises(ValueError):round_f11_half_twist(bad)

if __name__=='__main__':unittest.main()
