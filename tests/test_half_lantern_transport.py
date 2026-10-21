"""A temporary local relation simplifies supports and is then reexpanded."""
from collections import Counter
from dataclasses import replace
import json
from pathlib import Path
import unittest

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import product
from surface_diagrams.fifty_decomposition import transport_round_half_lantern
from surface_diagrams.hyperelliptic_homology import IDENTITY
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.six_seven_structure import SignedResearchFactor


class HalfLanternTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        cls.saved=json.loads((cls.folder/'certificate.json').read_text())
        cls.source=tuple(SignedResearchFactor(**dict(f,conjugator=tuple(f['conjugator'])))
                         for f in cls.saved['compact_boundary_chart']['factors'])
        cls.route=transport_round_half_lantern(cls.source)

    def test_every_state_is_the_same_exact_disk_double_boundary(self):
        r=self.route
        self.assertEqual(len(r['stages']),11)
        expected=exact_action((1,2,3,4)*10,strands=5)
        for stage in r['stages']:
            self.assertEqual(exact_action(product(stage['factors']),strands=5),expected)
            self.assertTrue(all(f.sign==1 for f in stage['factors']))
            self.assertLessEqual(max(len(supported_class(f.mapping_class,strands=5))
                                     for f in stage['factors']),16)
        self.assertEqual(r['sphere_move_count'],0)
        self.assertFalse(r['is_shorter_identity_proof'])

    def test_all_hurwitz_and_named_substitution_certificates_replay(self):
        moves=self.route['stages'][1:]
        self.assertEqual(Counter(s['kind'] for s in moves),
            {'disk_hurwitz':7,'disk_pc_half_lantern':2,'disk_presentation':1})
        for step in moves:
            self.assertTrue(step['disk_equality'])
            if step['kind']=='disk_hurwitz':
                self.assertEqual(reduce_word(product(step['local_before'])+
                    inverse_word(product(step['local_after']))),())
                self.assertEqual(step['disk_word_certificate']['discrepancy'],())
            else:
                self.assertEqual(exact_action(product(step['local_before']),strands=5),
                                 exact_action(product(step['local_after']),strands=5))
            if step['kind']=='disk_pc_half_lantern':
                self.assertEqual(step['lift_homology'],IDENTITY)
        self.assertEqual([s['direction'] for s in moves if s['kind']=='disk_pc_half_lantern'],
                         ['compress','expand'])

    def test_root_disappears_and_positive_factor_types_are_recovered(self):
        r=self.route;final=r['factors']
        self.assertEqual(r['before_score'],dict(max_support_word=16,total_support_word=86,braid_letters=126))
        self.assertEqual(r['after_score'],dict(max_support_word=16,total_support_word=68,braid_letters=100))
        types=lambda fs:Counter((f.points,f.power,f.half,f.sign) for f in fs)
        self.assertEqual(types(final),types(self.source))
        self.assertEqual(len(final),16)
        self.assertFalse(any(f.id=='transport.R234' for f in final))
        self.assertTrue(r['temporary_root_reexpanded'])
        by_id={f.id:f for f in final}
        self.assertEqual((by_id['F3'].conjugator,by_id['F3'].first),((4,),3))
        c=by_id['alternate.C4.rose.2']
        self.assertEqual((c.conjugator,c.first,c.points),((-4,),1,4))

    def test_published_branch_is_source_linked_and_shows_only_disk_exact_supports(self):
        raw=self.saved['half_lantern_transport']
        self.assertEqual(raw['stages'][0]['factors'],self.saved['compact_boundary_chart']['factors'])
        self.assertEqual(json.loads(json.dumps(self.route,default=lambda x:x.__dict__)),raw)
        display=json.loads((self.folder/'display.json').read_text())
        states=display['routes']['transport']
        self.assertEqual(len(states),22)
        self.assertEqual([s['temporary_root'] for s in states],
                         [False,False]+[True]*8+[False]*12)
        for stage,shown in zip(raw['stages'],states):
            for source,index in zip(stage['factors'],shown['factors']):
                row=display['rows'][index]
                self.assertFalse(row['sphere_rechart'])
                f=SignedResearchFactor(**dict(source,conjugator=tuple(source['conjugator'])))
                self.assertEqual(exact_action(f.word,strands=5),exact_action(row['word'],strands=5))

    def test_simple_four_point_curve_exposes_a_checked_daisy_and_half_lantern_target(self):
        next_relations=self.route['next_relations']
        for name in ('daisy','half_lantern'):
            relation=next_relations[name]
            self.assertFalse(relation['applied_to_replay'])
            self.assertEqual(exact_action(product(relation['local_before']),strands=5),
                             exact_action(product(relation['local_after']),strands=5))
        daisy=next_relations['daisy']['local_after']
        self.assertEqual((daisy[0].conjugator,daisy[0].first,daisy[0].points),((),1,3))
        u,x,square=next_relations['half_lantern']['local_before']
        self.assertEqual(exact_action(u.word*2,strands=5),exact_action(daisy[1].word,strands=5))
        e=replace(square,power=1)
        self.assertEqual(exact_action(e.word+u.word+inverse_word(e.word),strands=5),
                         exact_action(x.word,strands=5))
        self.assertTrue(next_relations['requires_gathering'])
        self.assertTrue(next_relations['route_to_gather_not_found'])

    def test_wrong_order_or_negative_source_is_rejected(self):
        for false in (self.source[:-1],
                (replace(self.source[0],sign=-1),)+self.source[1:],
                (self.source[1],self.source[0])+self.source[2:]):
            with self.assertRaises(ValueError):transport_round_half_lantern(false)


if __name__=='__main__':unittest.main()
