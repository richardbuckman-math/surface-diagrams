"""The actual fifty has an explicit twenty block, but not a standalone W1."""
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import unittest

from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.factorization_explorer import product
from surface_diagrams.fifty_decomposition import (extract_twenty_block,unit_factors,permutation_orbits,
    recognize_thirty_boundary,working_seed_to_legacy_chart,compact_thirty_boundary_chart)
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.six_seven_structure import SignedResearchFactor
from surface_diagrams.sphere_actions import sphere_chain_certificate
from surface_diagrams.standard_block_routes import standard_block_factors
from surface_diagrams.sphere_support_compact import check_support_replacement
from surface_diagrams.curves import Arc
from surface_diagrams.normal_cut_engine import calculate_cut_system
from surface_diagrams.factorization_explorer import initial_factors


class FiftyDecompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-compact/source-route.json'
        data=json.loads(path.read_text())['positive_sphere_expansion']['stages'][-1]['factors']
        cls.source=tuple(SignedResearchFactor(**dict(f,conjugator=tuple(f['conjugator']))) for f in data)
        cls.route=extract_twenty_block(cls.source)
        cls.thirty=recognize_thirty_boundary(cls.route['thirty_factors'])

    def test_seven_disk_moves_and_one_explicit_sphere_rechart_replay(self):
        r=self.route
        self.assertEqual(len(r['stages']),9)
        self.assertEqual(sum(s['kind']=='disk_hurwitz' for s in r['stages']),7)
        self.assertEqual(r['sphere_move_count'],1)
        self.assertEqual(r['stages'][0]['factors'],self.source)
        for before,after in zip(r['stages'],r['stages'][1:]):
            self.assertEqual(len(before['factors']),len(after['factors']))
            if after['kind']=='disk_hurwitz':
                self.assertEqual(after['disk_word_certificate']['discrepancy'],())
                self.assertEqual(reduce_word(product(before['factors'])+inverse_word(product(after['factors']))),())
            else:
                self.assertIn('SPHERE MOVE',after['title'])
                self.assertFalse(after['disk_equality'])
                self.assertNotEqual(after['disk_discrepancy'],())
                self.assertTrue(sphere_chain_certificate(after['disk_discrepancy'])['certified'])
                self.assertEqual(homology_action(after['disk_discrepancy']),IDENTITY)

    def test_the_twenty_is_a_disk_conjugate_of_w0_and_closes_independently(self):
        r=self.route;word=product(r['twenty_factors']);g=r['standard_twenty_frame']
        self.assertEqual(len(r['twenty_units']),20)
        self.assertEqual(word,r['twenty_word'])
        self.assertEqual(exact_action(word),exact_action(g+product(standard_block_factors('W0'))+inverse_word(g)))
        self.assertTrue(sphere_chain_certificate(word)['certified'])
        self.assertEqual(homology_action(word),IDENTITY)
        self.assertEqual(r['twenty_telescope'],())
        cap=r['twenty_closure']
        self.assertEqual(cap['local_before'],r['twenty_factors'])
        self.assertEqual(cap['local_after'],())
        self.assertEqual(cap['factors'],r['thirty_factors'])
        self.assertIn('SPHERE MOVE',cap['title'])
        self.assertEqual(cap['disk_discrepancy'],word)
        self.assertTrue(cap['sphere_certificate']['certified'])
        self.assertEqual(cap['lift_homology'],IDENTITY)

    def test_thirty_remains_positive_but_cannot_be_w1_by_hurwitz_moves_alone(self):
        r=self.route;thirty=r['thirty_factors']
        self.assertEqual(len(r['thirty_units']),30)
        self.assertTrue(all(f.sign==1 and f.points==2 for f in thirty))
        self.assertEqual(permutation_orbits(thirty),((1,3,4),(2,5),(6,)))
        self.assertEqual(permutation_orbits(standard_block_factors('W1')),((1,2,3,4,5,6),))
        self.assertTrue(r['thirty_permutation_obstruction_to_w1'])
        self.assertFalse(r['thirty_alone_hurwitz_equivalent_to_w1'])
        self.assertFalse(r['thirty_standard_block_identified'])
        self.assertFalse(r['complete_structural_derivation_found'])
        self.assertTrue(sphere_chain_certificate(product(thirty))['certified'])
        self.assertEqual(homology_action(product(thirty)),IDENTITY)

    def test_unit_expansion_and_invalid_inputs(self):
        self.assertEqual(len(unit_factors(self.source)),50)
        for source in (self.source[:-1],tuple(replace(f,id='wrong') for f in self.source),
                       (replace(self.source[0],sign=-1),)+self.source[1:]):
            with self.assertRaises(ValueError):extract_twenty_block(source)
        false=list(self.source);false[9]=replace(false[9],conjugator=(),first=1)
        with self.assertRaises(ValueError):extract_twenty_block(false)

    def test_thirty_has_an_independent_double_boundary_proof(self):
        r=self.thirty
        self.assertTrue(r['independent_sphere_identity_proof'])
        self.assertFalse(r['uses_source_identity_as_hypothesis'])
        self.assertFalse(r['hurwitz_equivalence_to_w1_claimed'])
        self.assertEqual(r['disk_core_length'],40)
        five=product(r['five_point_factors']);boundary=r['boundary']
        self.assertTrue(all(abs(g)<=4 for g in five))
        self.assertEqual(exact_action(five,strands=5),exact_action(boundary.word,strands=5))
        for stage in r['stages']:
            if stage['kind']=='sphere_rewrite':
                self.assertIn('SPHERE MOVE',stage['title'])
                self.assertTrue(sphere_chain_certificate(stage['disk_discrepancy'])['certified'])
                self.assertEqual(homology_action(stage['disk_discrepancy']),IDENTITY)
        self.assertEqual(r['stages'][-2]['kind'],'disk_boundary_relation')
        self.assertEqual(r['stages'][-1]['factors'],())
        self.assertEqual(homology_action(boundary.word),IDENTITY)
        self.assertNotEqual(homology_action(replace(boundary,power=1).word),IDENTITY)
        false=list(self.route['thirty_factors']);false[0],false[1]=false[1],false[0]
        with self.assertRaisesRegex(ValueError,'ordered five-point factorization'):
            recognize_thirty_boundary(false)

    def test_working_seed_is_connected_to_the_saved_route_with_no_sphere_moves(self):
        r=working_seed_to_legacy_chart()
        self.assertEqual(len(r['stages']),6)
        self.assertEqual(len(product(r['stages'][0]['factors'])),154)
        self.assertEqual(r['stages'][-1]['factors'],initial_factors())
        self.assertEqual(r['sphere_move_count'],0)
        self.assertEqual(sum(s['kind']=='disk_hurwitz' for s in r['stages']),3)
        self.assertEqual(sum(s['kind']=='global_conjugation' for s in r['stages']),1)

    def test_compact_boundary_chart_preserves_each_disk_support_and_the_central_product(self):
        old=self.thirty['five_point_factors'];r=compact_thirty_boundary_chart(old)
        self.assertEqual(r['frame'],(-2,-3,-4,1))
        self.assertEqual(r['before_score'],dict(max_support_word=28,total_support_word=156,braid_letters=150))
        self.assertEqual(r['after_score'],dict(max_support_word=16,total_support_word=86,braid_letters=126))
        self.assertEqual([s['kind'] for s in r['stages']],
                         ['start','global_conjugation','disk_presentation','disk_boundary_relation','sphere_rewrite'])
        self.assertEqual(r['sphere_move_count'],1)
        local=r['next_local_relation']
        self.assertFalse(local['applied_to_replay'])
        self.assertTrue(local['introduces_temporary_negative'])
        self.assertEqual(local['local_before'],r['factors'][1:7])
        self.assertEqual(exact_action(product(local['local_before']),strands=5),exact_action(product(local['local_after']),strands=5))
        self.assertTrue(all(f.sign==1 for f in r['factors']))
        self.assertEqual(exact_action(product(old),strands=5),exact_action(product(r['factors']),strands=5))
        for before,after in zip(r['stages'][1]['factors'],r['factors']):
            self.assertEqual(exact_action(before.word,strands=5),exact_action(after.word,strands=5))
            self.assertEqual((before.id,before.points,before.power,before.half),(after.id,after.points,after.power,after.half))
        self.assertEqual(r['stages'][-1]['factors'],())
        self.assertTrue(r['stages'][-1]['sphere_certificate']['certified'])
        self.assertEqual(r['stages'][-1]['lift_homology'],IDENTITY)
        false=list(old);false[0],false[1]=false[1],false[0]
        with self.assertRaises(ValueError):compact_thirty_boundary_chart(false)
        with self.assertRaises(ValueError):compact_thirty_boundary_chart((replace(old[0],sign=-1),)+old[1:])

    def test_published_replay_is_linked_to_the_actual_source_and_certifies_display_recharts(self):
        root=Path(__file__).resolve().parents[1]
        source=root/'docs/proofs/six-seven-compact/source-route.json'
        folder=root/'docs/proofs/six-seven-fifty-blocks'
        saved=json.loads((folder/'certificate.json').read_text())
        display=json.loads((folder/'display.json').read_text())
        self.assertEqual(saved['source_sha256'],sha256(source.read_bytes()).hexdigest())
        self.assertEqual(saved['source'],json.loads(json.dumps([f.__dict__ for f in self.source])))
        self.assertEqual(len(display['states']),9)
        for state in display['states']:
            self.assertEqual(sum(display['rows'][i]['units'] for i in state['factors']),50)
        for record in saved['display_recharts']:
            old=SignedResearchFactor(**record['source']);new=SignedResearchFactor(**record['displayed'])
            check=check_support_replacement(old.mapping_class,new.mapping_class,max_cuts=40)
            self.assertEqual(check['disk_equal'],record['certificate']['disk_equal'])
            self.assertEqual(tuple(record['certificate']['disk_discrepancy']),check['disk_discrepancy'])
        self.assertEqual({k:len(v) for k,v in display['routes'].items()},dict(extract=9,thirty=20,working=6,compact=5,overview=7))
        self.assertEqual(display['routes']['thirty'][0]['factors'],display['routes']['extract'][-1]['factors'])
        self.assertIn('SPHERE MOVE',display['routes']['thirty'][1]['title'])
        self.assertTrue(saved['independent_sphere_identity_certificate'])
        self.assertFalse(saved['explicit_w0_w1_hurwitz_route'])
        cut=json.loads((folder/'boundary-cut-certificate.json').read_text())
        self.assertEqual(cut['actual_images'],cut['expected_images'])
        arcs=tuple(Arc(**dict(a,cuts=tuple(a['cuts']))) for a in cut['arcs'])
        self.assertEqual(len(calculate_cut_system(arcs,points=5).paths),5)
        data=(folder/'display.json').read_text();version=sha256(data.encode()).hexdigest()[:16]
        expected=(root/'examples/fifty_twenty_extraction.html').read_text(encoding='utf-8').replace('VERSION',version)
        self.assertEqual((folder/'index.html').read_text(encoding='utf-8'),expected)

    def test_unified_overview_retains_all_atomic_moves_and_every_sphere_discrepancy(self):
        root=Path(__file__).resolve().parents[1]
        folder=root/'docs/proofs/six-seven-fifty-blocks'
        display=json.loads((folder/'display.json').read_text())
        source=root/'docs/proofs/six-seven-compact/source-route.json'
        route=display['routes']['overview'];summary=display['overview_summary']
        self.assertEqual(summary['source_sha256'],sha256(source.read_bytes()).hexdigest())
        self.assertEqual([len(s['moves']) for s in route[1:]],[5,145,8,17,1,1])
        self.assertEqual(summary['atomic_moves'],177)
        self.assertFalse(summary['is_shorter_derivation'])
        spheres=[m for s in route[1:] for m in s['moves'] if m['kind']=='sphere_rewrite']
        self.assertEqual(len(spheres),28)
        self.assertTrue(all(m['disk_discrepancy'] for m in spheres))
        phases=display['routes']
        self.assertEqual([s['factors'] for s in route],
            [phases['working'][0]['factors'],phases['working'][-1]['factors'],
             phases['extract'][0]['factors'],phases['extract'][-1]['factors'],
             phases['thirty'][-3]['factors'],phases['thirty'][-2]['factors'],phases['thirty'][-1]['factors']])
        legacy=json.loads(source.read_text())
        atoms=[s for phase in legacy.values() if isinstance(phase,dict) and 'stages' in phase for s in phase['stages'][1:]]
        self.assertEqual([(m['title'],m['kind']) for m in route[2]['moves']],[(s['title'],s['kind']) for s in atoms])


if __name__=='__main__':unittest.main()
