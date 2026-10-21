"""Exact geometric F6 alignment, with an honest separated-target status."""
from collections import Counter
from dataclasses import replace
import json
from pathlib import Path
import unittest
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.factorization_explorer import product,simplify_factor
from surface_diagrams.fifty_decomposition import align_f6_half_lantern
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.six_seven_structure import SignedResearchFactor,research_hurwitz_move
from surface_diagrams.projected_relations import pc_half_lantern_terms


class F6AlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        cls.saved=json.loads((cls.folder/'certificate.json').read_text())
        cls.source=tuple(SignedResearchFactor(**dict(f,conjugator=tuple(f['conjugator'])))
                         for f in cls.saved['half_lantern_transport']['factors'])
        cls.route=align_f6_half_lantern(cls.source)

    def test_all_nine_moves_preserve_the_exact_disk_product_and_readability_bound(self):
        r=self.route;expected=exact_action((1,2,3,4)*10,strands=5)
        self.assertEqual(len(r['stages']),12)
        self.assertEqual(Counter(s['kind'] for s in r['stages'][1:]),
                         {'disk_hurwitz':9,'disk_presentation':2})
        for step in r['stages']:
            self.assertEqual(exact_action(product(step['factors']),strands=5),expected)
            self.assertLessEqual(max(len(supported_class(f.mapping_class,strands=5))
                                     for f in step['factors']),20)
            if step['kind']=='disk_hurwitz':
                self.assertEqual(reduce_word(product(step['local_before'])+
                    inverse_word(product(step['local_after']))),())
        self.assertEqual(r['peak_support_word'],20)
        self.assertEqual(r['sphere_move_count'],0)

    def test_both_good_endpoints_and_the_exact_nonadjacent_target(self):
        r=self.route
        self.assertEqual(r['unwound_score'],dict(max_support_word=10,total_support_word=56,braid_letters=88))
        self.assertEqual(r['after_score'],dict(max_support_word=10,total_support_word=58,braid_letters=84))
        by_id={f.id:f for f in r['factors']}
        self.assertEqual((by_id['F3'].conjugator,by_id['F3'].first),((),4))
        self.assertEqual((by_id['F6'].conjugator,by_id['F6'].first),((-2,-2),1))
        target=r['aligned_target']
        self.assertEqual(exact_action(product(target['local_before']),strands=5),
                         exact_action(product(target['local_after']),strands=5))
        self.assertTrue(target['requires_gathering'])
        self.assertFalse(target['applied_to_replay'])
        self.assertEqual(Counter((f.points,f.power,f.half,f.sign) for f in r['factors']),
                         Counter((f.points,f.power,f.half,f.sign) for f in self.source))

    def test_rejected_gather_is_valid_but_not_a_complexity_improvement(self):
        r=self.route;state=r['factors'];probe=r['rejected_gather_probe']
        for a,b in probe['moves']:state=research_hurwitz_move(state,a,b)['factors']
        root=r['aligned_target']['local_after'][0]
        self.assertEqual(exact_action(product(state[12:15]),strands=5),exact_action(root.word,strands=5))
        terms=tuple(replace(root,conjugator=t.conjugator,first=t.first,points=t.points,
            power=t.power,half=t.half) for t in pc_half_lantern_terms(root.mapping_class))
        end=tuple(simplify_factor(f) for f in state[:12]+terms+state[15:])
        self.assertEqual(max(len(supported_class(f.mapping_class,strands=5)) for f in end),20)
        self.assertEqual(sum(len(supported_class(f.mapping_class,strands=5)) for f in end),90)
        self.assertEqual(len(product(end)),114)
        self.assertFalse(probe['applied_to_replay'])

    def test_published_route_is_linked_and_invalid_source_rejected(self):
        self.assertEqual(json.loads(json.dumps(self.route,default=lambda f:f.__dict__)),self.saved['f6_alignment'])
        d=json.loads((self.folder/'display.json').read_text())
        self.assertEqual(len(d['routes']['transport']),26)
        for state,shown in zip(self.route['stages'][1:],d['routes']['transport'][11:]):
            for f,i in zip(state['factors'],shown['factors']):
                self.assertFalse(d['rows'][i]['sphere_rechart'])
                self.assertEqual(exact_action(f.word,strands=5),exact_action(d['rows'][i]['word'],strands=5))
        for bad in (self.source[:-1],(replace(self.source[0],sign=-1),)+self.source[1:]):
            with self.assertRaises(ValueError):align_f6_half_lantern(bad)


if __name__=='__main__':unittest.main()
