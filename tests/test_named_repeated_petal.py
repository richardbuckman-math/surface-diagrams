from dataclasses import asdict, replace
from pathlib import Path
import json
import unittest
from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.named_repeated_petal import repeated_petal_daisy, shorten_repeated_petal_daisy
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.sphere_actions import sphere_chain_certificate
from tests import test_named_positive_frame as positive_frame_source


class NamedRepeatedPetalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        positive_frame_source.NamedPositiveFrameTests.setUpClass()
        cls.old=positive_frame_source.NamedPositiveFrameTests.r
        cls.r=shorten_repeated_petal_daisy(cls.old['stages'])
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'

    def test_generic_rule_for_multiple_disks_petals_multiplicities_and_frames(self):
        for n in (3,4,5):
            for chart in ((),(1,-2),(4,4,-3)):
                for index in range(1,n):
                    for m in (2,3,4):
                        outer=Factor('outer',chart,1,n)
                        r=repeated_petal_daisy(outer,index,m)
                        self.assertEqual(exact_action(product(r['inputs']),5),exact_action(product(r['outputs']),5))
                        self.assertEqual(r['outputs'][1].power,m-1)
                        self.assertTrue(r['retained_power_split']['exact_free_word_equality'])
                        self.assertTrue(all(f.power>0 and not f.half for f in r['inputs']+r['outputs']))
                        for move in r['retained_spare_transports']:
                            self.assertEqual(reduce_word(product(move['local_before'])),reduce_word(product(move['local_after'])))

    def test_actual_powered_input_uses_all_individual_named_matches(self):
        stage=self.r['repeated_petal_certificate'];w=stage['named_pattern_witness'];p=w['repeated_petal_pattern']
        self.assertEqual([f.power for f in stage['local_before']],[1,1,2,1,1])
        self.assertFalse(w['actual_powered_petal_split']);self.assertEqual(w['actual_extra_petal_transports'],0)
        self.assertTrue(w['every_actual_input_matched'])
        self.assertEqual(len(w['individual_matches']),5)
        for match in w['individual_matches']:
            self.assertEqual(exact_action(match['actual'].word,5),exact_action(match['pattern'].word,5))
        self.assertEqual((len(p['retained_daisy_interchanges']),len(p['retained_spare_transports'])),(4,2))
        self.assertEqual(p['multiplicity'],2)
        self.assertEqual(p['spare_presentation_match'][0]['pattern'].power,1)
        self.assertEqual(exact_action(product(stage['local_before']),5),exact_action(product(stage['local_after']),5))

    def test_suffix_order_and_inverse_are_necessary(self):
        p=repeated_petal_daisy(Factor('outer',(),1,5),1,3)
        q=replace(p['basis'][1],power=2)
        wrong=replace(q,conjugator=reduce_word(p['suffix']+q.conjugator))
        self.assertNotEqual(exact_action(wrong.word,5),exact_action(p['outputs'][1].word,5))
        wrong_order=p['inputs'][1:2]+p['inputs'][:1]+p['inputs'][2:]
        self.assertNotEqual(exact_action(product(wrong_order),5),exact_action(product(p['outputs']),5))

    def test_literal_join_preserves_prefix_suffix_and_four_visible_exteriors(self):
        r=self.r;first,last=r['source_interval']
        self.assertEqual((r['previous_whole_named_steps'],r['whole_named_steps'],r['graphical_steps']),(89,86,67))
        self.assertTrue(r['literal_rejoin']);self.assertEqual(r['stages'][:first+1],self.old['stages'][:first+1])
        self.assertEqual(r['stages'][first+1]['factors'],self.old['stages'][last]['factors'])
        self.assertEqual(r['stages'][first+2:],self.old['stages'][last+1:])
        self.assertEqual((r['previous_adjacent_checks'],r['adjacent_checks'],r['added_internal_spare_transports']),(108,106,2))
        self.assertEqual(r['actual_peak_support_word'],20)
        self.assertEqual(len(r['factors']),4)
        self.assertTrue(all(f==Factor(f.id,(),1,5) for f in r['factors']))

    def test_local_disk_sphere_lift_framing_and_complete_kernels(self):
        s=self.r['repeated_petal_certificate'];w=s['named_pattern_witness']
        self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
        self.assertEqual(exact_action(product(s['factors']),5),exact_action(BOUNDARY_WORD*4,5))
        self.assertEqual(homology_action(product(s['factors'])),IDENTITY)
        self.assertTrue(sphere_chain_certificate(product(s['factors']))['certified'])
        for f,split in zip(w['normalized_actual'][1:],w['petal_point_pushing']):
            self.assertFalse(split.shadow_word)
            self.assertEqual(exact_action(f.word,5),exact_action(split.reconstructed_word,5))
        expected=tuple(sum(f.power for f in s['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in s['local_after'] if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
        self.assertEqual(s['framed_balance_before_minus_after'],expected)

    def test_saved_public_proof_is82_and_historical_component_is_unchanged(self):
        c=json.loads((self.folder/'certificate.json').read_text())
        metadata={k:v for k,v in self.r.items() if k not in ('stages','factors')}
        self.assertEqual(json.loads(json.dumps(metadata,default=asdict)),c['named_repeated_petal_shortening'])
        self.assertEqual(c['named_positive_frame_shortening']['whole_named_steps'],89)
        summary=c['named_full_route']['summary']
        self.assertEqual((summary['graphical_steps'],summary['sphere_moves'],summary['action_only_boundary_recognitions']),(82,4,0))
        self.assertEqual(summary['route_parts'],[17,63,1,1]);self.assertFalse(summary['complete_under_twenty_derivation'])
        d=json.loads((self.folder/'display-pure.json').read_text())
        self.assertEqual(len(d['routes']['namedfull']),83)
        stage=d['routes']['namedfull'][77]
        self.assertIn('squared petal',stage['title'])
        self.assertTrue(stage['repeated_petal_daisy']);self.assertEqual(stage['internal_spare_transports'],2)
        html=(self.folder/'index.html').read_text(encoding='utf-8')
        self.assertIn('82 retained steps',html);self.assertIn('EXACT DISK REPEATED-PETAL PC DAISY',html)

    def test_invalid_multiplicities_nonpetals_and_source_routes_are_rejected(self):
        outer=Factor('outer',(),1,5)
        for m in (True,1,0,-1,2.5):
            with self.assertRaises(ValueError):repeated_petal_daisy(outer,2,m)
        for index in (True,0,-1,5):
            with self.assertRaises(ValueError):repeated_petal_daisy(outer,index,2)
        for bad in (replace(outer,half=True),replace(outer,power=2),replace(outer,points=2)):
            with self.assertRaises(ValueError):repeated_petal_daisy(bad,1,2)
        with self.assertRaises(ValueError):shorten_repeated_petal_daisy(self.old['stages'][:-1])


if __name__=='__main__':
    unittest.main()
