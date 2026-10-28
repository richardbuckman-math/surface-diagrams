from dataclasses import asdict, replace
from pathlib import Path
import json,unittest
from tests import test_named_repeated_petal as historical_source
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.named_early_powered_daisy import partial_powered_daisy,shorten_early_powered_daisy
from surface_diagrams.puncture_boundary import BOUNDARY_WORD


class EarlyPoweredDaisyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        historical_source.NamedRepeatedPetalTests.setUpClass()
        cls.old=historical_source.NamedRepeatedPetalTests.r
        cls.r=shorten_early_powered_daisy(cls.old['stages'])
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'

    def test_generic_partial_power_rule_for_multiple_disks_charts_and_powers(self):
        for n in (3,4,5):
            for chart in ((),(1,-2),(4,4,-3)):
                for power in (2,3,4):
                    c=Factor('C',chart,1,n,power)
                    r=partial_powered_daisy(c)
                    self.assertEqual(r['outputs'][0].power,power-1)
                    self.assertEqual(exact_action(c.word,5),exact_action(product(r['outputs']),5))
                    self.assertTrue(r['retained_power_decomposition']['exact_free_word_equality'])
                    self.assertFalse(r['actual_standalone_power_split'])
                    self.assertTrue(all(not f.half and f.power>0 for f in r['outputs']))
                    for x in r['output_point_pushing']:
                        self.assertEqual(exact_action(x['factor'].word,5),exact_action(x['split'].reconstructed_word,5))

    def test_actual_early_parent_and_every_petal_have_full_individual_matches(self):
        s=self.r['replacement_interval'][1];w=s['named_pattern_witness'];p=w['partial_powered_daisy']
        self.assertEqual([f.power for f in s['local_before']],[2])
        self.assertEqual([f.points for f in s['local_after']],[3,2,2,2])
        self.assertEqual(p['internal_frame'],(1,1,1,1))
        for m in p['parent_match']+p['powered_input_match']+p['individual_petal_matches']:
            self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
        self.assertTrue(w['every_actual_input_matched']);self.assertTrue(w['sphere_certificate']['certified'])
        self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
        expected=tuple(sum(f.power for f in s['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in s['local_after'] if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
        self.assertEqual(s['framed_balance_before_minus_after'],expected)

    def test_all_changed_configurations_and_five_square_crossings_are_retained(self):
        r=self.r;states=[a for s in r['replacement_interval'] for a in (s,)+tuple(s.get('atomic_steps',()))]
        self.assertEqual(len(states),22)
        self.assertEqual(len(r['changed_state_sphere_lift_certificates']),22)
        for s,c in zip(states,r['changed_state_sphere_lift_certificates']):
            fs=s['factors'];self.assertEqual(exact_action(product(fs),5),exact_action(BOUNDARY_WORD*4,5))
            self.assertTrue(all(f.power>0 for f in fs));self.assertLessEqual(max(len(supported_class(f.mapping_class,5)) for f in fs),17)
            self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
        square=r['replacement_interval'][4];self.assertEqual(square['adjacent_moves'],5)
        crossed=[]
        for a in square['atomic_steps']:
            crossed.extend(f.id for f in a['local_before'] if f.id.startswith('alternative.next.'))
            self.assertEqual(reduce_word(product(a['local_before'])),reduce_word(product(a['local_after'])))
        self.assertEqual(set(crossed),{'alternative.next.0','alternative.next.1','alternative.next.2'})

    def test_explicit_cyclic_frame_and_literal_join_preserve_the_rest_of_the_proof(self):
        r=self.r;first,last=r['source_interval'];cycle=r['replacement_interval'][3]
        self.assertEqual(reduce_word(cycle['frame']+product(cycle['local_before'])+inverse_word(cycle['frame'])),reduce_word(product(cycle['local_after'])))
        self.assertEqual(r['stages'][:first+1],self.old['stages'][:first+1])
        self.assertEqual(r['stages'][first+8]['factors'],self.old['stages'][last]['factors'])
        self.assertEqual(r['stages'][first+9:],self.old['stages'][last+1:])
        self.assertTrue(r['literal_rejoin'])
        for m in r['late_individual_petal_matches']:
            self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
        for x in r['late_petal_point_pushing']:
            self.assertEqual(exact_action(x['factor'].word,5),exact_action(x['split'].reconstructed_word,5))

    def test_count_honesty_and_four_exteriors(self):
        r=self.r
        self.assertEqual((r['previous_whole_named_steps'],r['whole_named_steps'],r['graphical_steps']),(86,85,66))
        self.assertEqual((r['previous_operations'],r['replacement_operations']),(9,8))
        self.assertEqual((r['previous_adjacent_checks'],r['adjacent_checks']),(106,108))
        self.assertEqual((r['extension_peak_support_word'],r['actual_peak_support_word']),(17,20))
        self.assertEqual(len(r['factors']),4)
        self.assertTrue(all(f==Factor(f.id,(),1,5) for f in r['factors']))
        self.assertEqual((r['sphere_moves'],r['exterior_caps'],r['action_only_boundary_recognitions']),(0,0,0))

    def test_saved_public_proof_is79_with_truthful_partial_power_scope(self):
        c=json.loads((self.folder/'certificate.json').read_text(encoding='utf-8'))
        metadata={k:v for k,v in self.r.items() if k not in ('stages','factors')}
        self.assertEqual(json.loads(json.dumps(metadata,default=asdict)),c['named_early_powered_daisy_shortening'])
        self.assertEqual(c['named_repeated_petal_shortening']['whole_named_steps'],86)
        s=c['named_full_route']['summary'];self.assertEqual((s['graphical_steps'],s['sphere_moves'],s['action_only_boundary_recognitions']),(79,4,0))
        self.assertEqual(s['route_parts'],[14,63,1,1]);self.assertFalse(s['complete_under_twenty_derivation'])
        d=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['routes']['namedfull']),80)
        self.assertTrue(d['routes']['namedfull'][32]['partial_powered_daisy'])
        html=(self.folder/'index.html').read_text(encoding='utf-8')
        self.assertIn('79 retained steps',html);self.assertIn('EXACT DISK PARTIAL-POWER PC DAISY',html)

    def test_invalid_powers_nonstabilizing_frames_and_changed_source_are_rejected(self):
        for power in (True,1,0,-1,2.5):
            with self.assertRaises(ValueError):partial_powered_daisy(Factor('C',(),1,3,power))
        with self.assertRaises(ValueError):partial_powered_daisy(Factor('C',(),1,3,2),internal_frame=(3,))
        with self.assertRaises(ValueError):partial_powered_daisy(Factor('C',(),1,3,2,True))
        with self.assertRaises(ValueError):shorten_early_powered_daisy(self.old['stages'][:-1])


if __name__=='__main__':unittest.main()
